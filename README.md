# Foodgram - дипломный проект курса Python Backend Developer

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Bash Script](https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

**Foodgram** — это веб-приложение на **Django REST framework и Node.js с использованием контейнеризации Docker**.<br>

Пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

-----
### База данных
Во время разработки использовалась база SQLite с последующим подключением к ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor).

-----
### API
API на ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) реализовано строго согласно спецификации из ТЗ, которую можно посмотреть (после развертывания проекта) по адресу: http://localhost/api/docs/. Запущен browsable API по адресу http://localhost/api/.

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
<details>
<summary>Страница пользователя</summary>
На странице — имя пользователя, все рецепты, опубликованные пользователем, и кнопка, чтобы подписаться или отписаться от него.
</details>

-----
<details>
<summary>Страница подписок</summary>
Только владелец аккаунта может просмотреть свою страницу подписок. Ссылка на неё находится в выпадающем меню в правом верхнем углу.
</details>

-----
<details>
<summary>Избранное</summary>
Список избранных рецептов. Добавлять рецепты в избранное может только залогиненный пользователь.
</details>

-----
<details>
<summary>Список покупок</summary>
Список избранных рецептов. Добавлять рецепты в избранное может только залогиненный пользователь.
</details>

-----
<details>
<summary>Создание и редактирование рецепта</summary>
Эта страница доступна только для залогиненных пользователей. Все поля на ней обязательны для заполнения. 
Сценарий поведения пользователя:

1. Пользователь переходит на страницу добавления рецепта, нажав на кнопку Создать рецепт в шапке сайта.
2. Пользователь заполняет все обязательные поля.
3. Пользователь нажимает кнопку Создать рецепт.

Также пользователь может отредактировать любой рецепт, который он создал.
</details>

-----
<details>
<summary>Страница смены пароля</summary>
Стандартная форма для заполнения.
</details>

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
Приложение готово к работе. <br>
http://127.0.0.1/ - проект. <br>
http://127.0.0.1/api/docs/ - API спецификация.

-----
# Примеры запросов к API:

- GET: .../api/users/ <br>
<details>
<summary>RESPONSE: </summary>

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "aaaaaaaaaaaaa@a.ru",
            "id": 5,
            "username": "aaaaaaaaa",
            "first_name": "aaaaaaaa",
            "last_name": "aaaaaa",
            "is_subscribed": false,
            "avatar": null
        },
        {
            "email": "natalie@yandex.ru",
            "id": 2,
            "username": "Natlalie",
            "first_name": "Наталья",
            "last_name": "Лилова",
            "is_subscribed": false,
            "avatar": "https://foodgramnoup.zapto.org/media/users/avatars/temp.jpeg"
        },
        {
            "email": "svetlana@svetlana.ru",
            "id": 4,
            "username": "Svetlana",
            # ...
```

</details>

- GET: ...api/recipes/?tags=lunch&limit=2 <br>
<details>
<summary>RESPONCE: </summary>
  
```
  HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 4,
    "next": "https://foodgramnoup.zapto.org/api/recipes/?limit=2&page=2&tags=lunch",
    "previous": null,
    "results": [
        {
            "id": 7,
            "tags": [
                {
                    "id": 4,
                    "name": "Десерт",
                    "slug": "dessert"
                },
                {
                    "id": 1,
                    "name": "Завтрак",
                    "slug": "breakfast"
                },
                {
                    "id": 2,
                    "name": "Обед",
                    "slug": "lunch"
                },
                {
                    "id": 3,
                    "name": "Ужин",
                    "slug": "dinner"
                }
            ],
            "author": {
                "email": "natalie@yandex.ru",
                "id": 2,
                "username": "Natlalie",
                "first_name": "Наталья",
                "last_name": "Лилова",
                "is_subscribed": false,
                "avatar": "https://foodgramnoup.zapto.org/media/users/avatars/temp.jpeg"
            },
            "ingredients": [
                {
                    "id": 21,
                    "name": "апельсиновый сок свежевыжатый",
                    "measurement_unit": "мл",
                    "amount": 250
                },
                {
                    "id": 26,
                    "name": "сахар",
                    "measurement_unit": "г",
                    "amount": 50
                },
                {
                    "id": 27,
                    "name": "кукурузный крахмал",
                    "measurement_unit": "г",
                    "amount": 25
                },
                {
                    "id": 28,
                    "name": "кокосовая стружка",
                    "measurement_unit": "г",
                    "amount": 20
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Апельсиновый десерт",
            "image": "https://foodgramnoup.zapto.org/media/recipes/b4be97183dbf11ee81bcca697c28bd51_upscaled.jpeg",
            "text": "Сегодня готовим десерт из 3-х ингредиентов, рецепт которого очень популярен в последнее время. Без яиц, молока и муки. Десерт без выпечки готовится из минимального количества продуктов и супербыстро, за 10 минут, не считая времени его застывания в холодильнике.",
            "cooking_time": 20
        },
        {
            "id": 5,
            "tags": [
                {
                    "id": 2,
                    "name": "Обед",
                    "slug": "lunch"
                }
            ],
            "author": {
                "email": "viktor@viktor.ru",
                "id": 3,
                "username": "Viktor",
                "first_name": "Виктор",
                "last_name": "Сухов",
                "is_subscribed": false,
                "avatar": "https://foodgramnoup.zapto.org/media/users/avatars/man__copy1.jpg"
            },
            "ingredients": [
                {
                    "id": 19,
                    "name": "макароны",
                    "measurement_unit": "г",
                    "amount": 200
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Макароны с копчёными колбасками в томатно-сливочном соусе",
            "image": "https://foodgramnoup.zapto.org/media/recipes/749f4c6801b5575e641f0650e7097b9f.jpg",
            "text": "Хотите рецепт идеального ужина? Он перед вами. Макароны с копчёными колбасками и приятным соусом из сливок и помидоров готовятся быстро. Благодаря соусу обычные макароны становятся нежными, сочными и очень вкусными. Копчёные колбаски, чеснок и базилик добавляют блюду аппетитный аромат, а сыр - только усиливает его сливочный вкус.",
            "cooking_time": 20
        }
    ]
}
```
</details>

- POST: ...api/auth/token/login <br>
<details>
<summary>RESPONCE:</summary>

```
 HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "auth_token": "a1fa4f81f3fde008ebf71845296e0ece4d0ad8ec"
}
```

</details>


-----
# Автор
<a href="https://github.com/NoupSange">Михаил Федосеев</a>
