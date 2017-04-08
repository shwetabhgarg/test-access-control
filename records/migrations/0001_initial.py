# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 16:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100)),
                ('owner', models.IntegerField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='records.Document')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('access_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.AccessType')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Document')),
            ],
        ),
        migrations.CreateModel(
            name='PendingApprovalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.IntegerField()),
                ('owner', models.IntegerField(db_index=True)),
                ('active', models.BooleanField(default=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shard', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='pendingapprovalrequest',
            unique_together=set([('document', 'requester')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentpermission',
            unique_together=set([('document', 'user')]),
        ),
    ]
