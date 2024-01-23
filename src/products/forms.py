import uuid

from django.forms import ModelForm
from multiupload.fields import MultiFileField

from .models import Image, Product


def create_images_via_form(cleaned_data, product):
    if Image.objects.filter(product_id=product.id).count() != 0:
        image = (
            Image.objects.filter(product_id=product.id).values("image")[0].get("image")
        )
    else:
        image = None

    if image == "default_product_pict.jpg" and not cleaned_data["files"]:
        return
    elif not cleaned_data["files"] and image is None:
        Image.objects.create(product=product, image="default_product_pict.jpg")
    elif image == "default_product_pict.jpg" and cleaned_data["files"]:
        img = Image.objects.filter(product_id=product.id).first()
        img.delete()

    for each in cleaned_data["files"]:
        random_uuid = uuid.uuid4()
        each.name = f"{random_uuid}_{each.name}"
        Image.objects.create(product=product, image=each)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "category"]

    files = MultiFileField(
        min_num=1, max_num=3, max_file_size=1024 * 1024 * 5, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["title"].widget.attrs[
            "style"
        ] = "width:400px; height:40px; margin-bottom: 20px;"
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["price"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"
        self.fields["files"].widget.attrs.update({"class": "form-control-file"})

    def save(self, *args, **kwargs):
        instance = super(ProductForm, self).save()
        create_images_via_form(self.cleaned_data, instance)

        return instance


class EditForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "category"]

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["title"].widget.attrs["style"] = "width:400px; height:40px;"
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["price"].widget.attrs.update({"class": "form-control"})
        self.fields["price"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"
        self.fields["files"].widget.attrs.update({"class": "form-control-file"})
        self.fields["files"].required = False

    def save(self, *args, **kwargs):
        instance = super(EditForm, self).save()
        create_images_via_form(self.cleaned_data, instance)
        return instance
