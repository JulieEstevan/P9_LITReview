from django import forms
from . import models


class TicketForm(forms.ModelForm):
    """Form for creating and updating tickets."""
    image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(forms.ModelForm):
    """Form for creating and updating reviews."""
    class Meta:
        model = models.Review
        fields = ('rating', 'headline', 'body')


class UserFollowsForm(forms.Form):
    """Form for following users."""
    username = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}))
