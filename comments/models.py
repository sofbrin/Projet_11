from django.db import models
from django.utils import timezone

from users.models import User
from products.models import ProductDb


class CommentsManager(models.Manager):
    """def approve(self, query):
        query.update(approved_comment=True)"""


class CommentsDb(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name='comments')
    approved_comment = models.BooleanField(default=False)
    objects = CommentsManager()

    def __str__(self):
        return f'{self.author} : {self.text}'
