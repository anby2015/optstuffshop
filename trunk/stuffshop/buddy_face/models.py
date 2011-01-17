# -*- coding: utf-8 -*-
from django.db import models

class ChineeseBuddy(models.Model):
    image = models.ImageField(upload_to='buddies/',verbose_name='Фото (231х364)')
    name = models.CharField('Имя',max_length=15)
    position = models.CharField('Род занятий и город КНР',max_length=25)
    quote = models.CharField('Мысль',max_length=100)
