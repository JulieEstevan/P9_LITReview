from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Review(models.Model):
    """
    Model representing a review.
    """
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    """
    Model representing a ticket.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (600, 960)

    def resize_image(self):
        """
        Resize the image to fit within the defined maximum size while maintaining aspect ratio.
        """
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        Override the save method to resize the image before saving.
        """
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def delete(self, *args, **kwargs):
        """
        Override the delete method to remove the image file from storage.
        """
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class UserFollows(models.Model):
    """
    Model representing a user following another user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
