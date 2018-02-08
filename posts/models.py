from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Post(models.Model):
    image = models.ImageField(upload_to="post_images")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='author')
    liked_by = models.ManyToManyField(User)
    def __int__(self):
        return self.id


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, default=timezone.now().date())
    profilePic = models.ImageField(upload_to="post_images")

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )
class Comment(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	blob = models.TextField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

