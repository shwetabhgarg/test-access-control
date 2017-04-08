# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    owner = models.IntegerField(null=False, blank=False, db_index=True)
    title = models.CharField(max_length=100)
    parent_document = models.ForeignKey('Document', null=True, blank=True)
    data = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.data


class AccessType(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __unicode__(self):
        return self.name


class DocumentAccess(models.Model):
    docid = models.ForeignKey(Document, null=False)
    user = models.IntegerField(null=False)
    access_type = models.ForeignKey(AccessType, null=False)

    class Meta:
        unique_together = ('docid', 'user',)
        verbose_name_plural = 'DocumentAccesses'
