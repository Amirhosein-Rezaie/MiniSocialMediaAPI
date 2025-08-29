from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import (
    ValidationError
)


class Users(AbstractUser):
    """
    Users that registerd in the social media
    """
    class Roles(models.TextChoices):
        USER = 'USER', 'user'
        ADMIN = 'ADMIN', 'admin'

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "active"
        DELETED = "DELETED", "deleted"
        SUSPENDED = "SUSPENDED", "suspended"

    first_name = models.CharField(
        verbose_name='first_name', max_length=150, null=False, blank=False
    )
    last_name = models.CharField(
        verbose_name='last_name', max_length=150, null=False, blank=False
    )
    phone = models.CharField(
        verbose_name='phone', null=False, blank=False, max_length=150
    )
    email = models.EmailField(
        verbose_name='email', null=True, blank=True, max_length=150, unique=True
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )
    role = models.CharField(
        verbose_name='role', max_length=150, choices=Roles.choices, default=Roles.USER
    )
    profile = models.ImageField(
        verbose_name='profile', upload_to='profiles/'
    )
    status = models.CharField(
        max_length=20, choices=Status, default=Status.ACTIVE, null=False, blank=False
    )

    date_joined = None
    user_permissions = None
    is_staff = None
    is_superuser = None
    last_login = None

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Texts(models.Model):
    """
    Represents text-based posts created by users in the social media platform.
    Texts can be published alone or combined with images/videos.
    """
    text = models.TextField(
        verbose_name='text', null=False, blank=False
    )
    user = models.ForeignKey(
        verbose_name='user', null=False, blank=False, to=Users, on_delete=models.DO_NOTHING,
        related_name='user_texts'
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Texts'

    def __str__(self):
        return "%s -> %s" % (self.user.username, self.text[:30])


class Videos(models.Model):
    """
    Represents video content uploaded by users.
    Videos can appear as standalone posts or together with texts/images.
    """
    video = models.FileField(
        verbose_name='video', null=False, blank=False, upload_to='posts/videos/'
    )
    user = models.ForeignKey(
        verbose_name='user', null=False, blank=False, to=Users, on_delete=models.DO_NOTHING,
        related_name='user_videos'
    )
    caption = models.TextField(
        verbose_name='caption', null=True, blank=True
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Videos'

    def __str__(self):
        return "%s -> %s" % (self.user.username, self.video.name)


class Images(models.Model):
    """
    Represents image content uploaded by users.
    Images can be posted independently or alongside texts/videos.
    """
    image = models.ImageField(
        verbose_name='image', null=False, blank=False, upload_to='posts/images/'
    )
    user = models.ForeignKey(
        verbose_name='user', null=False, blank=False, to=Users, on_delete=models.DO_NOTHING,
        related_name='user_images'
    )
    caption = models.TextField(
        verbose_name='caption', null=True, blank=True
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Images'

    def __str__(self):
        return "%s -> %s => %s" % (self.user.username, self.image.name[:30], self.caption[:30])


class Posts(models.Model):
    """
    posts that users upload to the social media
    """
    user = models.ForeignKey(
        verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING, to=Users,
        related_name='user_posts'
    )
    title = models.CharField(
        verbose_name='title', null=True, blank=True, max_length=150
    )
    text_content = models.OneToOneField(
        verbose_name='text_content', null=True, blank=True, to=Texts, on_delete=models.CASCADE,
        related_name='post_text',
    )
    video_content = models.OneToOneField(
        verbose_name='video', null=True, blank=True, to=Videos, on_delete=models.CASCADE,
        related_name='post_video'
    )
    image_content = models.OneToOneField(
        verbose_name='image', null=True, blank=True, to=Images, on_delete=models.CASCADE,
        related_name='post_image'
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Posts'

    def __str__(self):
        return "%s -> %s" % (self.user.username, self.title[:30] or "No Title")

    def save(self, *args, **kwargs):
        if not (self.text_content or self.image_content or self.video_content):
            raise ValidationError(
                "Minimum one content field is necessary."
            )
        return super().save(*args, **kwargs)
