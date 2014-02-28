#coding: utf-8
'''
视图文件

Author: liufh
Created on 2013-01-14
'''
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from urlparse import parse_qs
import logging
import traceback
from utils import thqs, get_json_result, get_categories, get_videos, USERID
from videos.models import Video, NotifyInfo

logger = logging.getLogger('apidemo')
    
def show_userinfo(request):
    requesthead = 'http://spark.bokecc.com/api/user?'
    q = {'userid': USERID, 'format': 'json'}
    my_json = get_json_result(requesthead, q)
    user = my_json['user']
    return render_to_response('userinfo.html', {'userinfo': user})

def index(request):
    return render_to_response('index.html')
        
def show_videolist(request):
    total = Video.objects.count()
    videos = []
    if total > 0:
        videos_info = Video.objects.all()
        for item in videos_info:
            video = {}
            video['id'] = item.videoid
            video['title'] = item.title
            video['image'] = item.image
            videos.append(video)
    page_size=30
    paginator = Paginator(videos, page_size)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return render_to_response('videolist.html', {'posts': posts, 'userid': USERID, 'total': total})

def show_play(request, userid, videoid):
    user = {'userid': USERID, 'videoid': videoid}
    return render_to_response('play.html', {'user': user})

def show_playcode(request, videoid):
    #设置播放器的默认值
    playerwidth = 600
    playerheight = 490
    is_autoplay = False
    if 'width' in request.GET:
        playerwidth = request.GET['width']
    if 'height' in request.GET:
        playerheight = request.GET['height']
    if 'autoplay' in request.GET:
        is_autoplay = request.GET['autoplay']
    requesthead = 'http://spark.bokecc.com/api/video/playcode?'
    q = {'videoid': videoid, 'player_width': playerwidth, 'player_height': playerheight, 'auto_play': is_autoplay, 'format': 'json'}
    my_json = get_json_result(requesthead, q)
    video_js = my_json['video']['playcode']
    return render_to_response('playcode.html', {'video_js': video_js, 'videoid': videoid})
    
def show_edit(request, videoid):
    requesthead = 'http://spark.bokecc.com/api/video?'
    q = {'videoid': videoid, 'userid': USERID, 'format': 'json'}
    categories = get_categories()
    my_json = get_json_result(requesthead, q)
    video = my_json['video']
    images = video ['image-alternate']
    return render_to_response('edit.html', {'video': video, 
                                            'images': images, 
                                            'categories': categories
                                            }
                                  )
    
def edit_video(request):
    requesthead = 'http://spark.bokecc.com/api/video/update?'
    q = {'format': 'json'}
    request_params = request.GET
    if 'videoid' in request_params:
        q['videoid'] = request_params['videoid']
    if 'title' in request_params:
        q['title'] = request_params['title'].encode('utf-8')
    if 'tag' in request_params:
        q['tag'] = request_params['tag'].encode('utf-8')
    if 'description' in request_params:
        q['description'] = request_params['description'].encode('utf-8')
    if 'categoryid' in request_params:
        q['categoryid'] = request_params['categoryid']
    if 'imageindex' in request_params:
        q['imageindex'] = request_params['imageindex']
    info = ''
    my_json = get_json_result(requesthead, q)
    video = my_json['video']
    if video['id'] == q['videoid']:
        info = '更新成功，请刷新页面查看'
    return render_to_response('editvideo.html', {'info': info})
        
def show_upload(request):
    categories = get_categories()
    return render_to_response('upload.html', {'categories': categories})
    
def show_notify_info(request):
    infos = []
    for item in NotifyInfo.objects.all():
        infos.append(parse_qs(item.url.encode('utf-8')))
    return render_to_response('notify_info.html', {'infos': infos})
    
def notify(request):
    notify_result = ''
    try:
        notify_content = []
        for item in request.GET:
            item_str = '%s=%s' % (item, request.GET[item])
            notify_content.append(item_str.encode('utf-8'))
        notify_url = '&'.join(notify_content)
        NotifyInfo.objects.create(url = notify_url)
        notify_result = 'OK'
    except Exception:
        logger.error(traceback.format_exc())
        notify_result = 'Fail'
    finally:
        return render_to_response('notify.html', {'notify_result': notify_result})
    
def show_search(request):
    categories = get_categories()
    return render_to_response('search.html', {'categories': categories})
    
def search_video(request):
    requesthead = 'http://spark.bokecc.com/api/videos/search?'
    q = {'userid': USERID, 'format': 'json'}
    request_params = request.GET
    if ('search_query' in request_params) and ('search_cont' in request_params):
        q_str = '%s:%s' % (request_params['search_query'], request_params['search_cont'])
        q['q'] = q_str.encode('utf-8')
    if 'sort_param' in request_params:
        q['sort'] = request_params['sort_param']    
    if 'categoryid' in request_params:
        q['categoryid'] = request_params['categoryid']
    my_json = get_json_result(requesthead, q)
    videos = my_json['videos']
    if videos['total'] > 0:
        for video in videos['video']:
            video['creation_date'] = video.pop('creation-date')
            video_file_size = float(video['filesize'])/1024.0/1024.0
            video['filesize'] = '%.2f' % video_file_size
    return render_to_response('searchvideo.html', {'userid': USERID, 'videos': videos})

def get_upload_url(request):
    q = {'userid': USERID}
    if 'title' in request.GET:
        q['title'] = request.GET['title'].encode('utf-8')
    if 'tag' in request.GET:
        q['tag'] = request.GET['tag'].encode('utf-8')
    if 'description' in request.GET:
        q['description'] = request.GET['description'].encode('utf-8')
    if 'categoryid' in request.GET:
        q['categoryid'] = request.GET['categoryid']
    uploadurl = thqs().get_hqs(q)
    return render_to_response('getuploadurl.html', {'uploadurl': uploadurl})

def delete(request, video_id):
    try:
        #通知接口删除
        requesthead ='http://spark.bokecc.com/api/video/delete?'
        q = {'videoid': video_id, 'format': 'json'}
        my_json = get_json_result(requesthead, q)
        api_result = my_json['result']
        #删除数据库
        Video.objects.filter(videoid = video_id).delete()
        db_result = 'OK'
        if api_result == 'OK' and db_result == 'OK':
            info = '删除成功，请刷新页面！'
        else:
            info = '删除失败，请刷新页面重试'
    except Exception:
        logger.error(traceback.format_exc())
        info = '删除异常，请刷新页面重新'
    return render_to_response('delete.html', {'info': info})
    
def videosync(request):
    number_per_page = 100
    requesthead = 'http://spark.bokecc.com/api/videos?'
    q = {'userid': USERID, 'format': 'json'}
    ori_count = Video.objects.count()
    if ori_count > 0:
        videoid_from = Video.objects.order_by('id').last().videoid
        q['videoid_from'] = videoid_from
        video_total = get_videos(requesthead, q, number_per_page)
    else:
        video_total = get_videos(requesthead, q, number_per_page)
    status = '本次共同步%d个视频，请返回视频列表查看！' % video_total
    return render_to_response('videosync.html', {'status': status})
    