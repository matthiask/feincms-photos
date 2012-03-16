from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
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


class PhotoModelView(ModelView):
    pass
