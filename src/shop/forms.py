from django.forms import ModelForm
from multiupload.fields import MultiFileField

from .models import Image, Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})

    def save(self, *args, **kwargs):
        instance = super(ProductForm, self).save()
        for each in self.cleaned_data['files']:
            Image.objects.create(product=instance, image=each)


        return instance


class EditForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})
        self.fields["files"].widget.attrs.update({"class": "form-control-file"})
        self.fields["files"].required = False

    def save(self, *args, **kwargs):
        instance = super(EditForm, self).save()
        for each in self.cleaned_data['files']:
            Image.objects.create(product=instance, image=each)

        return instance
