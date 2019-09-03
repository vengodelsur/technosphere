## Курс "Введение в анализ данных"
[Программа курса на сайте Техносферы@Mail.Ru](https://sphere.mail.ru/curriculum/program/discipline/818/)

### ДЗ 1 (сбор данных, визуализация)
`hw1_kuznetsova.ipynb`

Выкачать с помощью API ВК места, где совершаются чекины; нанести точки на карту (folium); построить графики с распределением по типам объектов и т. д. (matplotlib)

### ДЗ 2 (ускорение Python)
`hw2_kuznetsova.ipynb`

Реализации K-Means c помощью:
* numpy
* Cython

### ДЗ 3 (предсказание рейтинга выходящих скоро фильмов на кинопоиске)
`flask/`

### СР по bash
`bash_scripts/`

<details><summary>Сравнить скорость выполнения задач с помощью чистого python. pandas и bash:</summary>

1. У вас есть файлы лога с полями timestamp, IP, method (GET/POST). Поля разделены табуляциями '\t'. Имена файлов - logs_%Y-%m-%d__%h.tsv.

```
$ ls /logs/
...
logs_2017-10-31-08.tsv
logs_2017-10-31-09.tsv
logs_2017-10-31-10.tsv
logs_2017-10-31-11.tsv
logs_2017-10-31-12.tsv
...
```

Ваша задача - вывести топ-10 самых частых IP, которые выполняли метод GET с 10 до 17 часов 2017-10-31

2. Найти список всех файлов с расширением tsv, размер которых превышает 10 мб и запустить архивацию в фоновом режиме

3. В директории /data\_for\_cool\_science/ лежат файлы следующуего формата: целевой класс, табуляция, список английский слов через запятую. Ваша задача, найти уникальные слова для класса bad, которые содержатся в трёх самых больших файлах. Помните, DOG и dog - одно и то же слово

</details>

