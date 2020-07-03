from django.db import models
from django.utils import timezone

from users.models import User
from products.models import CategoryDb, ProductDb


class CommentsManager(models.Manager):
    def approve_comments(self, request, query):
        query.update(active=True)


class CommentsDb(models.Model):
    text = models.TextField()
    date = models.DateTimeField(timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDb, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    objects = CommentsManager()

    def __str__(self):
        return f'{self.author} le {self.date} : {self.text}'

