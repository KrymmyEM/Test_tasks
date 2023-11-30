# Site
Для нормальной работы сайта вам нужно создать файл .env в каталоге проекта django или использовать файл .env в месте запуска проекта (например docker-compose file)

For normal work site you need make .env file in django project directory or use .env file in where project be started (for example, docker-compose file)
### Example .env file
```
SECRET_KEY_DJANGO=write_here_secret_key
SECRET_KET_STRIPE=
DEBUG=1
DJANGO_ALLOWED_HOSTS=0.0.0.0 *
DB_ENGINE=django.db.backends.sqlite3 
DB_NAME=database/db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
LANG_CODE=ru-RU
DATABASE=
```
**Внимание!**

В случае использования
```
DB_ENGINE=django.db.backends.sqlite3
```
все поля DB_, кроме *DB_NAME*, осталять пустыми

**Attention!**

In case of use
```
DB_ENGINE=django.db.backends.sqlite3
```
leave fields other than *DB_NAME* empty




