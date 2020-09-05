from django.db import models

class Post (models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.title