from django.db import models


class Kinodata(models.Model):
    ad = models.CharField(max_length=100)
    il = models.CharField(max_length=20)
    reytinq =models.CharField(max_length=50)
    foto =models.CharField(max_length=50)
    dil= models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    runtime = models.CharField(max_length=50)
    melumat= models.CharField(max_length=5000)
    video_link = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    poster = models.CharField(max_length=100)
    
    def __str__(self):
        return self.ad
    def get_absolute_url(self):
        return f'/'

class Contactus(models.Model):
    message= models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    subject= models.CharField(max_length=100)
    
    def __str__(self):
        return self.message
    def get_absolute_url(self):
        return f'/'

class Comment(models.Model):
    ad = models.CharField(max_length=100)
    tarix = models.DateField(auto_now=True)
    message = models.CharField(max_length=100)
    comment_id = models.CharField(max_length=100)

class Cronsettings(models.Model):
    year = models.IntegerField()
    page = models.IntegerField()