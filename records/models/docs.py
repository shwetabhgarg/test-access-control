# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    owner = models.IntegerField(null=False, blank=False, db_index=True)
    parent_document = models.ForeignKey('Document', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.title


class AccessType(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __unicode__(self):
        return self.name


class DocumentPermission(models.Model):
    document = models.ForeignKey(Document, null=False)
    user = models.IntegerField(null=False)
    access_type = models.ForeignKey(AccessType, null=False)

    class Meta:
        unique_together = ('document', 'user',)


class PendingApprovalRequest(models.Model):
    document = models.ForeignKey(Document, null=False)
    requester = models.IntegerField(null=False)
    owner = models.IntegerField(null=False, db_index=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        unique_together = ('document', 'requester',)
