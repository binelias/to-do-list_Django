from django.db import models
# django attribute to authenticate users
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):  
    # models inherit from Model
    # one to many relationship. when user get deleted, all his items will be deleted too
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # declare title to be a string and its length
    title = models.CharField(max_length=200)
    # a box to write in
    description = models.TextField(null=True, blank=True)
    # setting complete to false in order to edit it
    complete = models.BooleanField(default=False)
    # snapshot of date and timestamp when created
    created = models.DateTimeField(auto_now_add=True)
    # string value will be name self and return title

    def __str__(self):
        return self.title
    # complete status going to bottom

    class Meta:
        ordering = ['complete']
