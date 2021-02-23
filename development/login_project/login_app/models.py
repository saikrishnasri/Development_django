from django.db import models

class file_data(models.Model):
    image=models.FileField(upload_to='image',name='', null=True)
    video=models.FileField(upload_to='video',name='' , null=True)


class Registrations_data(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    mob=models.BigIntegerField()
    email=models.EmailField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Post(models.Model):
    title=models.CharField(max_length=500)
    content=models.TextField(max_length=100)

    def __str__(self):
        return self.title


            