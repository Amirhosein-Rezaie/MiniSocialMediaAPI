from django.db import models
from core.models import (
    Users, Posts
)


class Albums(models.Model):
    """
    The model of albums that users create and can save posts in specific album
    """
    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_albums'
    )
    title = models.CharField(
        verbose_name='title', null=False, blank=False, max_length=150
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Albums'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'title'], name='unique_user_title'
            )
        ]

    def __str__(self):
        return "%s -> %s" % (self.user.username, self.title)


class SavePosts(models.Model):
    """
    The model that users can save posts in
    """
    class Status(models.TextChoices):
        SAVED = 'SAVED', 'saved'
        UNSAVED = 'UN_SAVED', 'un_saved'

    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_saves'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.CASCADE,
        related_name='saved_post'
    )
    album = models.ForeignKey(
        to=Albums, verbose_name='album', null=False, blank=False, on_delete=models.CASCADE,
        related_name='saved_in_album'
    )
    status = models.CharField(
        verbose_name='status', null=False, blank=False, choices=Status.choices,
        default=Status.SAVED
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'SavePosts'

    def __str__(self):
        return "%s -> %s => %s" % (self.user.username, self.post.title, self.album.title)


class LikePost(models.Model):
    """
    The model that users can like posts
    """
    class Status(models.TextChoices):
        LIKED = 'LIKED', 'liked'
        DISLIKED = 'DISLIKED', 'disliked'

    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_like_post'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.CASCADE,
        related_name='liked_post'
    )
    status = models.CharField(
        verbose_name='status', null=False, blank=False, choices=Status.choices,
        default=Status.LIKED
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'LikePost'

    def __str__(self):
        return "%s %s" % (self.user.username, self.post.title)


class Comments(models.Model):
    """
    The model that user can comment in a specific post
    """
    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_comment_post'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.CASCADE,
        related_name='commented_post'
    )
    comment = models.TextField(
        verbose_name='content', null=False, blank=False
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Comments'

    def __str__(self):
        return "%s %s" % (self.user.username, self.comment[:10])


class ViewPost(models.Model):
    """
    The model that saves views of posts
    """
    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_view_post'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.CASCADE,
        related_name='viewed_post'
    )
    created_at = models.DateTimeField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'ViewPost'

    def __str__(self):
        return "%s %s" % (self.user.username, self.post.title)
