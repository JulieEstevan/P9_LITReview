from django import forms
from . import models
from authentication import models as a_models

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ('title', 'description', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ('rating', 'headline', 'body')
