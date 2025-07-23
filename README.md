# Foodgram - дипломный проект курса Python Backend Developer

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

**Foodgram** — это веб-приложение на **Django REST framework и Node.js с использованием контейнеризации Docker**.<br>

Пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

-----
### База данных
Во время разработки использовалась база SQLite с последующим подключением к ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor).

-----
### API
API на ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) реализовано строго согласно спецификации из ТЗ, которую можно посмотреть (после развертывания проекта) по адресу: http://localhost/api/docs/.

-----
### Авторизация
Авторизация реализована на основе библиотеки <a href="https://djoser.readthedocs.io/en/latest/getting_started.html">Djoser</a> (Token Based Authentication).

-----
### Удаленный сервер и деплой
По заданию проект должен быть развернут на выделенном удаленном сервере. Для автоматизации деплоя используются ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white).

-----
### Админ-панель
Админ панель реализована на ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white). Применена кастомизация фильтров, поиска. Доступна по адресу: http://localhost/admin/:

-----
### Страницы проекта
Проект состоит из следующих страниц:

<details>
<summary>Главная</summary>
<img width="500px" src="https://github.com/NoupSange/NoupSange/blob/main/images/main_page.png"><br>
На данной странице настроена пагинация до 6 объектов рецепта, фильтрация по тегам. При первичном переходе на главную страницу Frontend отпарвяет get запрос к api фильтруя выборку рецептов по всем тегам:

`https://<адрес_сайта>
/api/recipes/?page=1&limit=6&tags=dessert&tags=vegeterian&tags=breakfast&tags=drink&tags=lunch&tags=salad&tags=soups&tags=dinner`

Авторизованный пользователь может добавлять рецепты в список покупок или избранное.
</details>

-----
<details>
<summary>Cтраница регистрации</summary>
<img width="500px" src="https://github.com/NoupSange/NoupSange/blob/main/images/reg_page.png"><br>
Уникальным идентификатор пользователя изменен на поле почты.
</details>

-----
<details>
<summary>Страница входа</summary>
<img width="500px" src="https://github.com/NoupSange/NoupSange/blob/main/images/enter_page.png">
</details>

-----
<details>
<summary>Cтраница рецепта</summary>

<img width="500px" src="https://github.com/NoupSange/NoupSange/blob/main/images/recipe_page.png"><br>
Авторизованный пользователь может редактировать свой рецепт, добавить рецепт в избранное или список покупок, подписаться на другого автора.
</details>

-----
- страница пользователя
- страница подписок
- избранное
- список покупок
- создание и редактирование рецепта
- страница смены пароля


-----
# Установка и запуск проекта
<details>
<summary>1. Клонирование репозитория</summary>
Клонируйте репозиторий:
  
`git clone https://github.com/NoupSange/foodgram.git`
</details>
<details>
<summary>2. Файл .env</summary>

Перейдите директорию проекта и создайте файл с переменными окружения .env:
<br>
```
cd foodgram
touch .env
```

Добавьте необходимые переменные окружения, пример:
```
DEBUG=False

POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
POSTGRES_DB=django_db

DB_HOST=db
DB_PORT=5432
```
</details>

<details>
<summary>3. Запустите docker-оркестрацию контейнеров:</summary>
  
  ```
cd infra
# запуск контейнеров в интерактивном режиме
docker compose up -d
  ```
Дождитесь создания образов и запуска контейнеров.
</details>
<details>
<summary>4. Заполните контейнеры нужными данными:</summary>
  
  ```
# выполните миграции БД
docker compose exec backend python manage.py migrate

# создайте суперпользователя для использования админ-панели django
docker compose exec backend python manage.py createsuperuser

# загрузите фикстуры
docker compose exec backend python manage.py load_data

# скопируйте статику для админ-панели
docker compose exec backend python manage.py collectstatic

# переместите статику админк-панели в общий том для nginx и backend
docker compose exec backend cp -r /app/foodgram_backend/collected_static/. /backend_static/static/

# переместите API спецификацию в общий том для nginx
docker compose exec backend cp -r /app/docs /backend_static/
  ```
Дождитесь создания образов и запуска контейнеров. В браузере откройте http://127.0.0.1/.
</details>
Все готово! 
http://127.0.0.1/ - проект. 
http://127.0.0.1/api/docs/ - API спецификация.
