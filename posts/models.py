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
    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_saves'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='saved_post'
    )
    album = models.ForeignKey(
        to=Albums, verbose_name='album', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='saved_in_album'
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
    user = models.ForeignKey(
        to=Users, verbose_name='user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='user_like_post'
    )
    post = models.ForeignKey(
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='liked_post'
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
        to=Posts, verbose_name='post', null=False, blank=False, on_delete=models.DO_NOTHING,
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
