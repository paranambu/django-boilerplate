import csv
import os

from django.apps import apps
from django.db import transaction
from django.db.models.fields.related import ForeignKey, ManyToManyField


class CSVImporter(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path

        filename = os.path.basename(csv_path)
        app, model = filename.split('.')[:-1]

        try:
            self.Model = apps.get_model(app, model)
        except LookupError:
            raise Exception('Model {}.{} does not exist'.format(app, model))

    @transaction.atomic
    def import_csv(self):
        with open(self.csv_path) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self.import_row(row)

    def import_row(self, row):
        obj = self.get_object_or_create(row)

        m2m_data = {}
        for field_name, value in row.items():
            if isinstance(obj._meta.get_field(field_name), ForeignKey):
                if not value:
                    value = None
                else:
                    RelModel = obj._meta.get_field(field_name).remote_field.model
                    value = RelModel.objects.get(codename=value)
            elif isinstance(obj._meta.get_field(field_name), ManyToManyField):
                m2m_data[field_name] = [codename for codename in value.split(',') if codename]
                continue

            setattr(obj, field_name, value)

        obj.save()

        if m2m_data:
            self.save_m2m_data(obj, m2m_data)

    def get_object_or_create(self, row):
        obj = self.Model()
        try:
            # TODO: test Parler models
            if self.Model.__name__.endswith('Translation'):
                language_code = row['language_code']
                master_codename = row['master']
                obj = self.Model.objects.get(language_code=language_code, master__codename=master)
            elif 'codename' in row.keys():
                obj = self.Model.objects.get(codename=row['codename'])
        except self.Model.DoesNotExist:
            pass

        return obj

    def save_m2m_data(self, obj, m2m_data):
        for field_name, values in m2m_data.items():
            field = getattr(obj, field_name)
            related_objs = []
            for codename in values:
                RelModel = obj._meta.get_field(field_name).remote_field.model
                related_obj = RelModel.objects.get(codename=codename)
                related_objs.append(related_obj)
            field = getattr(obj, field_name)
            field.set(related_objs)
