
from sklearn.model_selection import KFold
import numpy as np
from urllib.request import urlopen

from sklearn.tree import DecisionTreeRegressor
import subprocess
from pickle import dump, load
import re
# from xgboost import plot_importance

DATA_DIR = 'data/'
POINTS_PATH = 'points.txt'


def oracle(array):
    url = 'https://oraclets801414828250428029.appspot.com/oracle?x1={:f}&x2={:f}&x3={:f}&x4={:f}&x5={:f}&x6={:f}&x7={:f}&x8={:f}&x9={:f}&x10={:f}'.format(
        *array)

    with urlopen(url) as response, open(POINTS_PATH, 'a') as out_file:
        data = response.read().decode('utf-8')
        out_file.write(str(array) + '\t' + data + '\n')
        parsed_data = re.split(r'^Function value = |\nAttempts left = ', data)
        if (data != 'UNDIFINED'):
            result, attempts = [np.float(number)
                                for number in parsed_data if number]

        else:
            return np.inf

    return result


class ActiveLearner:

    def __init__(self, oracle_function, steps=20, dimension=10, initial=10, learner_class=DecisionTreeRegressor, comittee_size=5):
        self.oracle_function = oracle_function
        self.steps = steps
        self.dimension = dimension
        self.initial = initial
        self.learner_class = learner_class
        self.comittee_size = comittee_size

        self.X = np.zeros(
            shape=(self.steps, self.dimension)).astype(np.float128)
        self.y = np.zeros(shape=(self.steps,)).astype(np.float128)

        self._set_initial_points()

        self.comittee = np.array([self.learner_class()
                                 for _ in range(self.comittee_size)])

    def generate_random_points(self, number):
        return 10 * np.random.random_sample((number, self.dimension))

    def _set_initial_points(self):
        self.labeled_indices = np.full(self.steps, False)
        self.labeled_indices[:self.initial] = True
        self.X[self.labeled_indices] = self.generate_random_points(
            self.initial)
        for i in np.where(self.labeled_indices)[0]:
            self.y[i] = self.oracle_function(
                self.X[i])

    def _train_comittee(self):
        kf = KFold(n_splits=self.comittee_size, shuffle=True)
        i = 0
        X_l, y_l = self.X[self.labeled_indices], self.y[self.labeled_indices]
        for train_index, test_index in kf.split(X_l):
            self.comittee[i] = self.comittee[i].fit(
                X_l[train_index], y_l[train_index])
                                                    # it would be better to
                                                    # make custom folds out of
                                                    # labeled indices so that
                                                    # no data copying is needed
            i += 1

    def _choose_point_to_label(self):
        points = self.generate_random_points(1000)
        variance = np.var([self.comittee[i].predict(points)
                          for i in range(self.comittee_size)], axis=0)
        return points[np.argmax(variance)]

    def _label(self, point):
        self.X[self.iteration] = point
        self.y[self.iteration] = self.oracle_function(point)
        self.labeled_indices[self.iteration] = True

    def add_point(self):
        self._train_comittee()
        best_point = self._choose_point_to_label()
        #print(best_point)
        self._label(best_point)

    def save_data(self):
                with open(DATA_DIR + 'X' + str(self.iteration) + '.pkl', 'wb') as f:
                    dump(self.X[self.labeled_indices], f)
                with open(DATA_DIR + 'y' + str(self.iteration) + '.pkl', 'wb') as f:
                    dump(self.y[self.labeled_indices], f)

    def learn(self):
        self.iteration = self.initial
        while self.iteration < self.steps:

            self.add_point()
            if ((self.iteration + 1) % 10 == 0):
                self.save_data()
            self.iteration += 1

        self.final_model = self.learner_class()
        self.final_model.fit(
            self.X[self.labeled_indices], self.y[self.labeled_indices])
        self.save_data()
        with open(DATA_DIR + 'model' + str(self.iteration) + '.pkl', 'wb') as f:
            dump(self.final_model, f)


#al = ActiveLearner(oracle)
#al.learn()
point = np.full((10, ), 5.0)

print(oracle(point))

"""
for i in range(10):
    point = np.full((10, ), 10.0)
    point[i] = 0
    print(oracle(point))
"""
