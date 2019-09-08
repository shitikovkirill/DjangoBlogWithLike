from django.db import models
from django.contrib.auth import get_user_model
from apps.blog.repository import PostQuerySet, LikeQuerySet


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="author"
    )

    publish = models.BooleanField(default=True)
    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like = models.BooleanField(default=True)  # if True - like if False - unlike
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = LikeQuerySet.as_manager()

    def __str__(self):
        return "{name} likes this post".format(name=self.user.username)

    class Meta:
        unique_together = (("user", "post"),)
