from django.db import models

# Create your models here.
# title, content, create_id, update_at
class Board(models.Model):
    title = models.CharField(max_length=20)  # input
    content = models.TextField()  # textarea
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)