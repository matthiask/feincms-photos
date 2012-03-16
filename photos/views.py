from towel import modelview


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
    pass


class PhotoModelView(ModelView):
    pass
