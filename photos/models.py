from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Album(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    created_by = models.ForeignKey(User, related_name='+',
        verbose_name=_('created by'))

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    def __unicode__(self):
        return self.title


class Photo(models.Model):
    def _upload_to(instance, filename):
        return ('photos/%s/%s_%s' % (
            instance.asset.pk,
            instance.version,
            filename,
            )).lower()


    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    created_by = models.ForeignKey(User, related_name='+',
        verbose_name=_('created by'))

    album = models.ForeignKey(Album, related_name='photos',
        verbose_name=_('album'))
    title = models.CharField(_('title'), max_length=100)
    photo = models.ImageField(_('photo'), upload_to=_upload_to)

    is_flagged = models.BooleanField(_('is flagged'), default=False,
        help_text=_('Flagged photos are only shown to administrators for deletion or un-flagging.'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    def __unicode__(self):
        return self.title