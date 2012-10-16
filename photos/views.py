from cStringIO import StringIO
import os
import zipfile

from django import forms
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy, ugettext as _

from towel import modelview

from photos.models import Album, Photo, determine_cover_photo


class PhotoUploadForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label=ugettext_lazy('title'),
        required=False)

    class Meta:
        fields = ('photo', 'title')
        model = Photo


class ModelView(modelview.ModelView):
    """
    ModelView subclass holding behavior specific to the photos app.
    """

    def editing_allowed(self, request, instance):
        if request.user.is_staff or request.user == instance.created_by:
            return True
        return False

    def deletion_allowed(self, request, instance):
        if request.user.is_staff:
            return True
        if request.user == instance.created_by:
            return self.deletion_allowed_if_only(request, instance, [self.model])
        return False

    def get_form(self, request, instance=None, **kwargs):
        return super(ModelView, self).get_form(request, instance=instance,
            exclude=('created_by',))

    def save_model(self, request, instance, form, change):
        if not change:
            instance.created_by = request.user
        instance.save()


class AlbumModelView(ModelView):
    def get_query_set(self, request, *args, **kwargs):
        return super(AlbumModelView, self).get_query_set(
            request, *args, **kwargs).transform(determine_cover_photo)

    def additional_urls(self):
        return [
            (r'%(detail)s/zip/$', self.crud_view_decorator(self.zip)),
        ]

    def detail_view(self, request, *args, **kwargs):
        instance = self.get_object_or_404(request, *args, **kwargs)

        if request.method == 'POST':
            form = PhotoUploadForm(request.POST, request.FILES)

            if form.is_valid():
                photo = form.save(commit=False)
                photo.album = instance
                photo.created_by = request.user
                if not photo.title:
                    photo.title = photo.photo.name
                photo.save()
                messages.success(request, _('The photo has been successfully uploaded.'))

                return HttpResponseRedirect('.')
        else:
            form = PhotoUploadForm()

        return self.render_detail(request, {
            self.template_object_name: instance,
            'editing_allowed': self.editing_allowed(request, instance),
            'form': form,
            })

    def zip(self, request, *args, **kwargs):
        instance = self.get_object_or_404(request, *args, **kwargs)

        buf = StringIO()
        zf = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED)

        for photo in instance.photos.all():
            zf.writestr(
                os.path.basename(photo.photo.name)
                , photo.photo.read())

        zf.close()
        buf.flush()

        response = HttpResponse(buf.getvalue())
        buf.close()
        response['Content-Disposition'] = 'attachment; filename=album.zip'
        return response


class PhotoModelView(ModelView):
    def get_query_set(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.filter(Q(is_flagged=False) | Q(created_by=request.user))

    def detail_view(self, request, *args, **kwargs):
        instance = self.get_object_or_404(request, *args, **kwargs)
        return redirect(instance.album)
