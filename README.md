# Дипломная работа профессии «Python-разработчик с нуля»
## Разработка API для загрузки публикаций и их фото с возможностью комментировать и ставить лайки.
<br>

**POSTS**
<br><br>
*Получение списка постов*
<br>
**GET** /api/posts/
<br>
*Получение деталей поста*
<br>
**GET** /api/posts/1/
<br>
*Создание поста*
<br>
**POST** /api/posts/
<br>
*Редактирование поста*
<br>
**PATCH** /api/posts/1/
<br>
*Удаление поста*
<br>
**DELETE** /api/posts/1/
<br><br>
**LIKES**
<br><br>
*Получение списка постов и пользователей, поставивших лайк*
<br>
**GET** /api/likes/
<br>
*Поставить лайк/дизлайк*
<br>
**POST** /api/posts/like/2/
<br><br>
**COMMENTS**
<br><br>
*Создание комментария к посту*
<br>
**POST** /api/posts/comment/1/
<br>
*Редактирование комментария*
<br>
**PATCH** /api/comments/update/2/
<br>
*Удаление комментария*
<br>
**DELETE** /api/comments/delete/2/
<br><br>
### Примеры запросов в файле requests_diplom.http
