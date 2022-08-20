# Проект «API YamDB»
#### API и документация для приложения YamDB.
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.
___
## Стек технологий:
- Python,
- Djando,
- DRF
- JWT - библиотека Simple JWT
___
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/ygazaryan/api_yamdb.git
```

```bash
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd api_yamdb
```

```bash
python3 manage.py migrate
```

Импорт csv файлов в модели:

```bash
python3 manage.py csv_import
```

Запустить проект:

```bash
python3 manage.py runserver
```

***
## Полная redoc документация доступна по url: (после запуска сервера):
http://localhost:8000/redoc/
***