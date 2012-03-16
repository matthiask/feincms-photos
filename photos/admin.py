from django.contrib import admin

from . import models


admin.site.register(models.Album,
    list_display=('title', 'created', 'created_by'),
    )

admin.site.register(models.Photo,
    list_display=('title', 'photo', 'is_flagged'),
    list_filter=('is_flagged',),
    )