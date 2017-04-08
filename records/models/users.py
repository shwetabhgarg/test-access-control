# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User)
    shard = models.IntegerField(null=False)
