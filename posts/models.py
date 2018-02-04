from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Post(models.Model):
    image = models.ImageField(upload_to="post_images")
    image2 = models.ImageField(upload_to="post_images", null=True, blank=True)
    image3 = models.ImageField(upload_to="post_images", null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, default=timezone.now().date())
    profilePic = models.ImageField(upload_to="post_images")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

