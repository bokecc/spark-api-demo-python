#!/usr/bin/python
#coding:utf-8
'''
video数据库对象

Author: liufh
Created on 2014-2-10
'''

from django.db import models

# Create your models here.
class Video(models.Model):
    videoid = models.CharField(max_length = 32, unique = True)
    title = models.CharField(max_length = 100)
    desp = models.CharField(max_length = 400)
    tags = models.CharField(max_length = 40)
    duration = models.IntegerField(default = 0)
    image = models.CharField(max_length = 200)
    
    def __unicode__(self):
        return self.videoid
    
class NotifyInfo(models.Model):
    url = models.CharField(max_length = 300) 
    
    def __unicode__(self):
        return self.url    
