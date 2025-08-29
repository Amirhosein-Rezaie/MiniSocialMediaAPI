from django.db import models
from core.models import Users
from rest_framework.exceptions import ValidationError


class Follow(models.Model):
    """
    The model that users can follow each others
    """
    follower_user = models.ForeignKey(
        to=Users, verbose_name='follower_user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='follower_user'
    )
    followed_user = models.ForeignKey(
        to=Users, verbose_name='followed_user', null=False, blank=False, on_delete=models.DO_NOTHING,
        related_name='followed_user'
    )
    created_at = models.DateField(
        verbose_name='created_at', auto_now_add=True
    )

    class Meta:
        db_table = 'Follow'

    def __str__(self):
        return "%s -> %s" % (self.follower_user, self.followed_user)

    def save(self, *args, **kwargs):
        if self.follower_user is self.followed_user:
            raise ValidationError(
                detail="Follower user cannot follow himself."
            )
        return super().save(*args, **kwargs)


class Logins(models.Model):
    """
    The model that save login logs in itself
    """
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', 'success'
        FAIL = 'FAIL', 'fail'

    user = models.ForeignKey(
        to=Users, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='user',
        related_name='user_logins'
    )
    status = models.CharField(
        verbose_name='status', null=False, blank=False, choices=Status.choices, default=Status.SUCCESS,
        max_length=150
    )
    created_at = models.DateTimeField(
        verbose_name='created_at', auto_now_add=True
    )
    username = models.CharField(
        verbose_name='username', null=True, blank=True, max_length=150
    )

    class Meta:
        db_table = 'Logins'

    def __str__(self):
        return "%s -> %s => %s" % (self.user.username or self.username, self.created_at, self.Status)
