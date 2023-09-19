from django import forms
from .models import Comment, Profile, AddAnime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Email Address"
        self.fields["email"].label = ""


class AddAnimeForm(forms.ModelForm):
    anime_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nome do Anime"}
        ),
    )
    anime_image = forms.ImageField()
    anime_description = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Descricao do Anime"}
        ),
    )

    class Meta:
        model = AddAnime
        fields = ("anime_name", "anime_image", "anime_description")

    # def __init__(self, *args, **kwargs):
    #     super(
    #         AddAnimeForm,
    #         self,
    #     ).__init__(*args, **kwargs)

    #     self.fields["anime_name"].widget.attrs["class"] = "form-control"
    #     self.fields["anime_name"].widget.attrs["placeholder"] = "Nome Anime"
    #     self.fields["anime_name"].label = ""


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label="",
        widget=forms.widgets.Textarea(
            attrs={"class": "form-control", "placeholder": "Comentario"}
        ),
    )

    class Meta:
        model = Comment
        exclude = ("user", "anime")
