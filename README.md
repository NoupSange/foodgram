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
- главная
<img src="https://github.com/NoupSange/NoupSange/blob/main/images/main_page.png">
На данной странице настроена пагинация до 6 объектов рецепта, фильтрация по тегам. При первичном переходе на главную страницу Frontend отпарвяет get запрос к api фильтруя выборку рецептов по всем тегам:

`https://<адрес_сайта>
/api/recipes/?page=1&limit=6&tags=dessert&tags=vegeterian&tags=breakfast&tags=drink&tags=lunch&tags=salad&tags=soups&tags=dinner`

Авторизованный пользователь может добавлять рецепты в список покупок или избранное.
- страница входа
<img src="https://github.com/NoupSange/NoupSange/blob/main/images/enter%20page.png">

- страница регистрации,
- страница рецепта,
- страница пользователя,
- страница подписок,
- избранное,
- список покупок,
- создание и редактирование рецепта,
- страница смены пароля



Адрес сервера: 51.250.101.209
Домен: foodgramnoup.zapto.org
Админ-панель:
  логин: admin@admin.ru
  пароль: admin_2025
