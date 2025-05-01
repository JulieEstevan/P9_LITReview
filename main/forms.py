from django import forms
from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('rating', 'headline', 'body')

class UserFollowsForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrez le nom d\'utilisateur'}))

