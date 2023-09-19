import uuid

from django.forms import ModelForm
from multiupload.fields import MultiFileField

from .models import Image, Product


def create_images_via_form(cleaned_data, product):
    if not cleaned_data['files']:
        Image.objects.create(product=product, image='default_product_pict.jpg')
    else:
        img = Image.objects.get(image='default_product_pict.jpg')
        img.delete()

    for each in cleaned_data['files']:
        random_uuid = uuid.uuid4()
        each.name = f'{random_uuid}_{each.name}'
        Image.objects.create(product=product, image=each)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})

    def save(self, *args, **kwargs):
        instance = super(ProductForm, self).save()
        create_images_via_form(self.cleaned_data, instance)

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
        create_images_via_form(self.cleaned_data, instance)
        return instance
