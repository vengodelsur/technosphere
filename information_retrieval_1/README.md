## Курс "Информационный поиск. Часть 1"
[Программа курса на сайте Техносферы@Mail.Ru](https://sphere.mail.ru/curriculum/program/discipline/817/)

`information_retrieval_1/`

### ДЗ 1 (фокусировка поискового робота)
`hw1_sekitei/`
С помощью алгоритма секитей (сад камней) извлечения признаков из урлов и 
кластеризации определить, нужно ли качать входящий урл или нет. Датасет разделен на два
множества: тренировочное, три сайта, и валидационное, два сайта. Для каждого сайта нужно
будет максимально эффективно выбрать доступную квоту. (максимальное количество
урлов, которое может быть взято с данного сайта).

### ДЗ 2 (булев поиск)
`hw2_index/`
Создание поискового индекса (со сжатием последовательности документов, соотвествующей терму), и разбор булевых запросов с поиском по индексу.

### ДЗ 3 (поиск дубликатов)
`hw3_duplicates/`
Дубликаты ищутся алгоритмом Бродера (сравниваются хэшированные шинглы - идущие внахлест подпоследовательности)

### ДЗ 5 (детектирование концов предложений)
`hw5_sentences/`
Даны параграфы и индексы символов в них, нужно обучиться на размеченной выборке определять, является ли символ концом предложения.

### ДЗ 6 (исправление опечаток)
`hw6_spellchecker/`
В этой домашней работе нужно разработать систему исправления опечаток. Компоненты системы:
модель языка, модель ошибок, генератор исправлений с помощью нечеткого поиска в бора, итерации, разные типы исправлений: словарные, split, join и раскладка
