# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from records.models.users import Person
from records.models.docs import Document, DocumentAccess, AccessType


class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AccessType)
admin.site.register(Document)
admin.site.register(DocumentAccess)
