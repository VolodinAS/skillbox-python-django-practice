# 12.6 Практическая работа
## Локализация и интернационализация
* Создайте базовый шаблон, который будет использоваться для всех шаблонов вашего сайта. Добавьте туда блок header и внесите в него форму с выбором языка.
* Далее вам необходимо отнаследовать все ваши шаблоны от базового, добавив интернационализацию в любой шаблон. Не забываем, что {% load i18n %} нужно указывать во все шаблоны, в которых мы делаем интернационализацию.
* Добавьте интернационализацию во все таблицы в Django админ панели.
* Добавьте русскую локализацию ко всем таблицам в Django админ панели.
* Добавьте интернационализацию во все столбцы моделей Django.
* Добавьте русскую локализацию во все столбцы моделей Django.
##### Примечание разработчика:
- Наконец-то добавил файл `requirements.txt`
- Локализация шаблонов:
  - `готово` `base_template/base_template.html`
  - `готово` `auth_template/index.html`
  - `готово` `auth_template/buttons/blog_buttons.html`
  - `готово` `auth_template/buttons/news_buttons.html`
  - `готово` `general/locales.html`
  - `готово` `pages/auth/auth.html`
  - `готово` `pages/auth/reg.html`
  - `готово` `app_users` > `profile/index.html`
  - `готово` `pages/blog/add/add.html`
  - `готово` `pages/blog/add/import.html`
  - `готово` `pages/blog/detail/detail.html`
  - `готово` `pages/blog/index/index.html`
  - `готово` `pages/blog/myblog/myblog.html`
  - `готово` `pages/moder/verify_news_list.html`
  - `готово` `pages/moder/verify_users.html`
  - `готово` `pages/news/add.html`
  - `готово` `pages/news/detail.html`
  - `готово` `pages/news/index.html`
  - `готово` `pages/news/my.html`
  - `готово` `pages/news/news_item.html`
  - `готово` `pages/news/tag_search.html`
  - `готово` `utils_template/avatar.html`
- Локализация forms.py
  - `готово` app_users > UserLoginForm
  - `готово` app_users > RegForm
  - `готово` app_users > EditProfileForm
  - `готово` app_blog > BlogAddForm
  - `готово` app_news > NewsItemForm
  - `готово` app_comments > CommentForm
  - `готово` app_news > SearchTag
- Локализация views.py
  - `готово` app_blogs
  - `готово` app_news
  - `готово` app_users
- Локализация models.py
  - `готово` app_blogs
  - `готово` app_comments
  - `готово` app_news
  - `готово` app_users
- Локализация apps.py
  - `готово` app_blogs
  - `готово` app_comments
- **Побочные задачи**
  - `http://127.0.0.1:8000/verifyme/` - перевести название группы
  - Интернационализация дат
  - Нормализация вида админки (поля)