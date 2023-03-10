# Проект «БИБЛИОТЕКА»
##### Разработчик [@oncologist63](https://t.me/oncologist63)

### Описание
Получение авторов и книг онлайн-библиотеки

### Среда разработки
###### Python 3.10

### Использованные библиотеки (requirements.txt)
* Django==4.1.4
* loguru==0.6.0
* requests==2.28.1
* pytz==2022.6
* Pillow==9.3.0
* djangorestframework==3.14.0
* Markdown==3.4.1
* django-filter==22.1
* drf-yasg==1.21.4

### Установка
1. Установить библиотеки: `pip install -r requirements.txt`
2. Создать миграции: `python manage.py makemigrations`
3. Применить миграции: `python manage.py migrate`
4. Запустить сервер: `python manage.py runserver`

---

## 14.6 Практическая работа
* `готово` Добавьте строки документации в приложение, реализованное в рамках домашнего задания предыдущего модуля
* `готово` Создайте файл README.md и добавьте в него информацию о проекте
* `готово` Используйте admindocs для генерации документации
* `готово` Используйте библиотеку drf-yasg для формирования openapi спецификации для разработанного API
* `готово` Проведите исследование, в котором выясните, какие еще форматы для создания спецификаций существуют и в чем их различие с форматом openapi (теоретическое задание)
  * OpenAPI (Swagger);
  * RAML;
  * API Blueprint
  * [Различия](https://medium.com/@clsource/swagger-vs-raml-vs-api-blueprint-daccab31f0f2)
---

## 13.7 Практическая работа
### Создайте api публичной библиотеки электронных книг:
* `готово` добавьте модели Автор с полями: имя, фамилия, год рождения и Книга с полями: название, isbn (международный стандартный книжный номер), год выпуска, количество страниц
* изучите страницу документации django rest framework про пагинацию
* `готово` реализуйте получение списка книг с пагинацией `/api/books`
* `готово` реализуйте получение списка авторов с пагинацией `/api/authors`
* `готово` реализуйте фильтрацию списка книг по автору и названию (поиск не по точному совпадению, а "содержит")
  * Поиск по названию: `/api/books/?title=KGBT`
  * Поиск по автору: `/api/books/?author=Бакман`
  * Поиск по автору и названию: `/api/books/?title=Вторая&author=Бакман`
* `готово` реализуйте фильтрацию списка книг по количеству страниц (больше, меньше, равно)
  * диапазон страниц: `/api/books/?pages_more=170&pages_less=320`
  * больше: `/api/books/?pages_more=170`
  * меньше: `/api/books/?pages_less=320`
  * равно: `/api/books/?pages=380`
* `готово` реализуйте фильтрацию авторов по имени
  * `/api/books/?author=Примаченко Ольга`
