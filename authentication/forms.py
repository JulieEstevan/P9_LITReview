from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
        self.fields["password1"].widget = forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
        self.fields["password2"].widget = forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"})
