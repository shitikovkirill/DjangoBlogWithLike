from django.db import models
from django.db.models import Q


class LikeQuerySet(models.QuerySet):
    def get_this_like(self, user, post):
        return self.filter(user=user, post=post).first()


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)

    def unpablished(self):
        return self.filter(publish=False)

    def get_posts_include_unpablished(self, user):
        return self.filter(Q(publish=True) | Q(publish=False, user=user))
