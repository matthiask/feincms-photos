from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from towel.managers import SearchManager
from towel.modelview import ModelViewURLs


class AlbumManager(SearchManager):
    search_fields = ('title', 'description', 'created_by__first_name',
        'created_by__last_name', 'created_by__email')


class Album(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    created_by = models.ForeignKey(User, related_name='+',
        verbose_name=_('created by'))

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)

    objects = AlbumManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('album')
        verbose_name_plural = _('albums')

    def __unicode__(self):
        return self.title

    urls = ModelViewURLs()


class PhotoManager(SearchManager):
    search_fields = ('title', 'album__title', 'album__description',
        'created_by__first_name', 'created_by__last_name', 'created_by__email')

    def active(self):
        return self.filter(is_flagged=False)


class Photo(models.Model):
    def _upload_to(instance, filename):
        return ('photos/%s/%s' % (
            instance.album_id,
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

    objects = PhotoManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    def __unicode__(self):
        return self.title

    urls = ModelViewURLs(lambda obj: {'album_id': obj.album_id, 'pk': obj.id})

    def get_absolute_url(self):
        return self.urls['detail']


def determine_cover_photo(queryset):
    """
    Transform method to attach cover photos to a list of albums

    Usage::

        Album.objects.transform(determine_cover_photo)[:20]
    """
    albums = dict((obj.id, obj) for obj in queryset)
    for photo in Photo.objects.filter(album__in=albums.keys()).reverse():
        albums[photo.album_id].cover_photo = photo
