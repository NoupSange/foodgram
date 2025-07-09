import csv
import json

from django.core.management.base import BaseCommand
from django.db import models
from django.db.transaction import atomic
from django.utils import termcolors


class Command(BaseCommand):
    data = [
        {
            'file_name': 'ingredients',
            'model': 'recipes.Ingredient',
            'fields': ['name', 'measurement_unit'],
            'type': 'csv'
        },
        {
            'file_name': 'tags',
            'model': 'recipes.Tag',
            'fields': ['name', 'slug'],
            'type': 'json'
        }
        # Добавьте другие файлы, если нужно
    ]
    help = 'Загрузка данных из CSV и JSON файлов в указанные модели'

    def __init__(self) -> None:
        super().__init__()
        self.style.NOTICE = termcolors.make_style(fg='yellow', opts=('bold',))

    def add_arguments(self, parser):
        parser.add_argument(
            'file_type',
            type=str,
            nargs='?',
            default='all',
            help='Тип файла для загрузки: csv, json, или all (все файлы)'
        )

    @atomic
    def handle(self, *args, **kwargs):
        from django.apps import apps

        file_type: str = kwargs['file_type'].lower()

        valid_file_types = {'csv', 'json', 'all'}
        if file_type not in valid_file_types:
            self.stderr.write(self.style.ERROR(
                f'Не корректный тип файла: {file_type}. Доступные варианты: csv, json, '
                'all.'
            ))
            return

        try:
            for entry in self.data:
                if file_type != 'all' and entry['type'] != file_type:
                    self.stderr.write(self.style.WARNING(
                        f'Данные {entry} не подходят для загрузки при '
                        'заданных параметрах.'
                    ))
                    continue

                file_name = entry['file_name']
                type_name = entry['type']
                model_name = entry['model']
                file_path = f'data/{file_name}.{type_name}'
                model = apps.get_model(model_name)
                fields: list = entry['fields']
                self.stdout.write(self.style.NOTICE(
                    f'Обработка файла: {file_path} для модели: '
                    f'{model_name} ({type_name})'
                ))

                if entry['type'] == 'csv':
                    self.load_csv(file_path, model, fields)
                elif entry['type'] == 'json':
                    self.load_json(file_path, model, fields)

            self.stdout.write(self.style.SUCCESS(
                f'Данные успешно загружены из: {type_name}'
            ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка загрузки данных: {e}'))

    def load_csv(self, file_path: str, model: models.Model, fields: list):
        """Обработка CSV-файла."""

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                data = {fields[i]: row[i] for i in range(len(fields))}
                model.objects.update_or_create(
                    **{fields[0]: data[fields[0]]},
                    defaults=data
                )

    def load_json(self, file_path: str, model: models.Model, fields: list):
        """Обработка JSON-файла."""

        with open(file_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                model_data = {
                    field: item[field] for field in fields if field in item
                }
                model.objects.update_or_create(
                    **{fields[0]: model_data[fields[0]]},
                    defaults=model_data
                )