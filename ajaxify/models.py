from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True,unique=True)

    objects = models.Manager()

    def __str__(self): 
        return self.name
    
    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'categories'


class Post(models.Model):
    main_image      = models.ImageField(upload_to='images/', blank=True)
    title           = models.CharField(max_length=125)
    slug            = models.SlugField(null=False, unique=True)
    summary         = models.CharField(max_length=255, null=True, blank=True)
    description     = models.TextField()
    created_on      = models.DateTimeField(auto_now_add=True)
    published_date  = models.DateTimeField(blank=True, null=True)
    last_modified   = models.DateTimeField(auto_now=True)
    categories      = models.ManyToManyField('Category', related_name='posts')
    read_time       = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0, null=True, blank=True) 
    likes           = models.ManyToManyField(User, blank=True, related_name='post_likes')
    is_featured     = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta: 
        ordering = ['-created_on']
        verbose_name_plural = 'posts'
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

   
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()