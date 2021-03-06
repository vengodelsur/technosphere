## Курс "Углубленное программирование на C/C++"
[Программа курса на сайте Техносферы@Mail.Ru](https://sphere.mail.ru/curriculum/program/discipline/819/)

Копия папки `Kuznetsova/` из [репозитория курса](https://github.com/mtrempoltsev/msu_cpp_autumn_2017)

### ДЗ 2 (калькулятор рекурсивным спуском)
`02/`
Используя метод рекурсивного спуска, написать простой калькулятор. Следует использовать функции, классы и переменные разделяемые между функциями использовать нельзя. Поддерживаемые операции: умножение, деление, сложение, вычитание, унарный минус.


### ДЗ 3 (рефакторинг калькулятора (использование классов; скобки и константы в грамматике))
`03/`
Рефакторим калькулятор!

Делаем класс, теперь вместо передачи результата через функции можно использовать поля класса
Добавляем скобки ( )
Добавляем константы, например Pi

### ДЗ 4 (перегрузка операторов)
`04/`
Нужно написать класс-матрицу, тип элементов double. В конструкторе задается количество рядов и строк. Поддерживаются оперции: получить количество строк/столбцов, получить конкретный элемент, умножить на вектор (в качестве вектора использовать класс std::vector<double>), умножить на число, сравнение на равенство/неравенство. 

Чтобы реализовать семантику [][] понадобится прокси-класс. Оператор матрицы возращает другой класс, в котором тоже используется оператор [] и уже этот класс возвращает значение.

### ДЗ 5 (шаблоны, перемещение)
`05/`
Написать для класса матрицы из предыдущей работы конструкторы и операторы копирования и перемещения. Сделать класс шаблонным.

### ДЗ 6 (шаблоны свойств, классы стратегий)
`06/`
Берем уже сделанный калькулятор, делаем из него шаблон. Пишем свойства для типов int, long, double (std::numeric_limits в помощь). Пишем стратегию parse, которая из строки делает число и проверяет, что оно в допустимых пределах. Собираем все вместе, теперь калькулятор должен уметь работать с int, long, double и проверять, что в выражениях числа не больше размера используемого типа (в качестве ошибки достаточно написать в консоль сообщение).

### ДЗ 7 (обработка ошибок, умные указатели)
`07/`
Нужно переделать калькулятор из предыдущего занятия, а конкретней - добавить обработку ошибок с помощью исключений. Если где-то выделялась память в куче, переделать с использованием умных указателей.

### ДЗ 8 (STL, контейнеры)
`08/`
Написать свой контейнер Vector, аналогичный std::vector и итератор для него. Из поддерживаемых методов достаточно operator[], push_back, pop_back, empty, size, clear, begin, end, rbegin, rend, resize.

### ДЗ 9 (STL)
`09/`
Программе через аргументы командной строки передают два имени файлов. Первое имя - текстовый файл в котором слова разделены пробелами, его надо прочесть, составить частотный словарь "слово" - "сколько раз встречается". После этого надо отсортировать словарь по частоте и вывести во второй файл (его имя - второй аргумент).

### ДЗ 10 (multithreading)
`10/`
Классическая задача.

Два потока по очереди выводят в консоль сообщение. Первый выводит ping, второй выводит pong.

Вывод: ping pong ping pong ping pong …


