import os

from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from api_yamdb.settings import BASE_DIR

from ...models import Category, Genre, Title, Review, Comment

User = get_user_model()

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV files,
first delete the db.sqlite3 file to destroy the database.
Then, run `python3 manage.py migrate --run-syncdb` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from csv files: static/data/*.csv"
    model_to_csvfile = {
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
        'Title m2m Genre': 'genre_title.csv',
    }

    def _create_model_object(self, model, row):
        if model == User:
            model_object = model(
                id=row['id'],
                username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'],
                first_name=['first_name'],
                last_name=['last_name']
            )
            model_object.save()
        if model == Category:
            model_object = model(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            model_object.save()
        if model == Genre:
            model_object = model(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            model_object.save()
        if model == Title:
            model_object = model(
                id=row['id'], name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])
            )
            model_object.save()
        if model == Review:
            model_object = model(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            model_object.save()
        if model == Comment:
            model_object = model(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )
            model_object.save()
        if model == 'Title m2m Genre':
            title_object = Title.objects.get(id=row['title_id'])
            title_object.genre.add(row['genre_id'])

    def handle(self, *args, **options):
        for model in self.model_to_csvfile.keys():
            if model != 'Title m2m Genre' and model.objects.exists():
                print(
                    f'"{model.__name__} model" data already loaded...exiting.'
                )
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return

        for model, csvfile in self.model_to_csvfile.items():
            print(f"Loading {str(model)} data")
            for row in DictReader(
                    open(os.path.join(BASE_DIR, f'static/data/{csvfile}'))):
                self._create_model_object(model, row)
