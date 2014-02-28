#!/usr/bin/python
#coding: utf-8
'''
工具文件

Author: liufh
Created on 2014-2-13
'''
import urllib
import json
import time
import hashlib
from math import ceil
from videos.models import Video

#在此处配置您的"SPARK_KEY"和“USERID”
SPARK_KEY = '' 
USERID = ''

def get_json_result(requesthead, q):
    '获取接口返回的信息'
    my_url = requesthead + thqs().get_hqs(q)
    f = urllib.urlopen(my_url)
    return json.loads(f.read())

def get_categories():
    '获取视频列表信息'
    requesthead = 'http://spark.bokecc.com/api/video/category?'
    q = {'userid': USERID, 'format': 'json'}
    my_json = get_json_result(requesthead, q)
    categories = my_json['video']['category']
    for item in categories:
        item['sub_category'] = item.pop('sub-category') 
    return categories
    
def insert_video_info(video_info):
    Video.objects.create(videoid = video_info['id'], 
                         title = video_info['title'], 
                         desp = video_info['desp'], 
                         tags = video_info['tags'], 
                         duration = video_info['duration'], 
                         image = video_info['image'], )
    
def get_videos(requesthead, q, number_per_page):
    my_json = get_json_result(requesthead, q)
    videos = my_json['videos']
    video_total = videos['total']
    if video_total > 0:
        for video_info in videos['video']:
            insert_video_info(video_info)
        ite = int(ceil(float(video_total)/number_per_page))
        if ite > 1:
            for page in range(2, ite+1):
                q['page'] = page
                my_json = get_json_result(requesthead, q)
                videos = my_json['videos']
                for video_info in videos['video']:
                    insert_video_info(video_info)
    return video_total

class thqs(object):
    '生成thqs请求url'
    def my_urlencode(self, q):
        '对请求的字段进行urlencode，返回值是包含所有字段的list'
        l = []
        #遍历字典，进行quote_plus操作，并把所有字段拼成list
        for k in q:
            k = urllib.quote_plus(str(k))
            v = urllib.quote_plus(str(q[k]))
            url_param = '%s=%s' % (k, v)
            l.append(url_param)
        l.sort()
        return '&'.join(l)
    
    def get_hqs(self, q):
        '按照thqs算法对所有的字段进行处理'
        qftime = 'time=%d' % int(time.time())
        salt = 'salt=%s' % SPARK_KEY
        qftail = '&%s&%s' % (qftime, salt)
        
        qs = self.my_urlencode(q)
        qf = qs + qftail
        hashqf = 'hash=%s' % (hashlib.new('md5', qf).hexdigest().upper())
        hqs = '&'.join((qs, qftime, hashqf))
        return hqs
