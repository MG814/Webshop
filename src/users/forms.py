from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from products.models import Wishlist
from shop.models import Cart
from .models import Profile, Address, User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["email"].widget.attrs["style"] = "margin-bottom: 20px;"
        self.fields["role"].widget.attrs.update({"class": "form-control"})
        self.fields["role"].widget.attrs["style"] = "margin-bottom: 20px;"

    def save(self, *args, **kwargs):
        instance = super(UserRegisterForm, self).save()
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)
        Profile.objects.create(user=instance)

        return instance


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image"].widget.attrs.update({"class": "form-control-file"})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ["username"]:
            self.fields[fieldname].help_text = None

        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["username"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs[
            "style"
        ] = "width:200px; height:40px; margin-bottom: 20px;"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name", "surname", "locality", "street", "zip_code", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["name"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["surname"].widget.attrs.update({"class": "form-control"})
        self.fields["surname"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-left: 10px;"
        self.fields["locality"].widget.attrs.update({"class": "form-control"})
        self.fields["locality"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["street"].widget.attrs.update({"class": "form-control"})
        self.fields["street"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["zip_code"].widget.attrs.update({"class": "form-control"})
        self.fields["zip_code"].widget.attrs[
            "style"
        ] = "width:100px; height:40px; text-align: center;"
        self.fields["phone"].widget.attrs.update({"class": "form-control"})
        self.fields["phone"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"

    def save(self, *args, **kwargs):
        instance = super(AddressForm, self).save()
        return instance


class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name", "surname", "locality", "street", "zip_code", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["name"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["surname"].widget.attrs.update({"class": "form-control"})
        self.fields["surname"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-left: 10px;"
        self.fields["locality"].widget.attrs.update({"class": "form-control"})
        self.fields["locality"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["street"].widget.attrs.update({"class": "form-control"})
        self.fields["street"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"
        self.fields["zip_code"].widget.attrs.update({"class": "form-control"})
        self.fields["zip_code"].widget.attrs[
            "style"
        ] = "width:100px; height:40px; text-align: center;"
        self.fields["phone"].widget.attrs.update({"class": "form-control"})
        self.fields["phone"].widget.attrs[
            "style"
        ] = "width:300px; height:40px; margin-bottom: 20px;"

    def save(self, *args, **kwargs):
        instance = super(AddressEditForm, self).save()
        return instance
