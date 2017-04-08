# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 16:54
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User
from records.models.users import Person
from records.models.docs import AccessType, Document


def fill_data(apps, schema_editor):
    User.objects.create_superuser(username='root', password='root', email='a@b.c')
    User.objects.create_user(username='alice', password='alice')
    User.objects.create_user(username='bob', password='bob')

    Person.objects.create(user_id=2, shard=1)
    Person.objects.create(user_id=3, shard=1)

    AccessType.objects.create(name='READ')

    Document.objects.create(title='a1', data='alice record 1 data data data data data data', owner=1)
    Document.objects.create(title='a2', data='alice record 2 data data data data data data', owner=1)
    Document.objects.create(title='b1', data='bob record 1 data data data data data data', owner=2)
    Document.objects.create(title='b2', data='bob record 2 data data data data data data', owner=2)


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill_data),
    ]