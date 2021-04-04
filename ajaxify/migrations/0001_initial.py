# Generated by Django 3.1.1 on 2020-09-08 17:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(blank=True, upload_to='images/')),
                ('title', models.CharField(max_length=125)),
                ('slug', models.SlugField(unique=True)),
                ('summary', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('read_time', models.IntegerField(default=0)),
                ('number_of_views', models.IntegerField(blank=True, default=0, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(related_name='posts', to='ajaxify.Category')),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'posts',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['id'], name='id_index'),
        ),
    ]
