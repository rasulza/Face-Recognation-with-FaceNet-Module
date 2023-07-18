from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=255)
    embedding = models.BinaryField()
    time = models.IntegerField()
    waitingـtime = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()



class One_Bread_Order(models.Model):
    name = models.CharField(max_length=255)
    embedding = models.BinaryField()
    time = models.IntegerField()
    waitingـtime = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()
