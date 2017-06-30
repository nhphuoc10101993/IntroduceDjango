from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
class UserProfile(models.Model):
    user = models.CharField(max_length=10,default='abc')
    description = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
class Document(models.Model):
    description = models.CharField(max_length=255,blank=True)
    doc = models.ImageField(upload_to='photo/',help_text='Please input image dir')
    uploaded_at = models.DateTimeField(auto_now=True)
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
class FileStorage(models.Model):
    description = models.CharField(max_length=255,blank=True)
    filename = models.FileField(upload_to='files/',help_text='Please input file dir')
    images = models.ImageField(upload_to='photo/',blank=True,help_text='Please input image dir')
    uploaded_at = models.DateTimeField(auto_now=True)

#def create_profile(sender,**kwargs):
    #if kwargs['created']:
    #    user_profile = UserProfile.objects.create(user=kwargs['instance'])
#post_save.connect(create_profile,sender=User)