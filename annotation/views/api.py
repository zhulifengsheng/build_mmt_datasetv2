import json
from multiprocessing import context

from django.http import Http404, JsonResponse
from django.http.response import HttpResponse

from annotation.models import Caption, Image, User, FixZhWithImage
from annotation.utils.deal_end_data import image_url

def static_image_url(request):
    if request.is_ajax() and request.method == 'POST':
        context = {
            'static_image_url': '/static/'+image_url(Image.objects.get(id=int(request.POST.get('image_id'))).image_name),
        }
        return HttpResponse(json.dumps(context))

    raise Http404("非ajax访问了该api")

def login(request):
    if request.is_ajax() and request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = User.objects.filter(username=username, password=password)
        if res.exists():
            # save session
            request.session["info"] = {'username': res.first().username}
            is_user = True
        else:   
            is_user = False
        context = {
            'is_user': is_user,
            'username': username,
        }
        return HttpResponse(json.dumps(context))

    raise Http404("非ajax访问了该api")

def contrast_zh_table(request):
    if request.is_ajax() and request.method == 'POST':
        image_id = int(request.POST.get('image_id'))
        user1_obj = User.objects.get(username=request.POST.get('user1'))
        user2_obj = User.objects.get(username=request.POST.get('user2'))
        if request.POST.get('user3') != '':
            user3_obj = User.objects.get(username=request.POST.get('user3'))
        else:
            user3_obj = None 
        caption_objs = Caption.objects.filter(image_obj_id=image_id).order_by('caption_number')
        
        data = []
        for caption_obj in caption_objs:
            dic = {}
            t = caption_obj.zh_without_image_obj    # 选择歧义中正确的那个
            dic['zh_without_image'] = t.zhs_without_image.split('\n')[t.correct_number]
            
            dic['user1'] = FixZhWithImage.objects.get(caption_id=caption_obj.id, 
                user_that_fixs_and_annots_it=user1_obj).fix_zh_with_image
            dic['user2'] = FixZhWithImage.objects.get(caption_id=caption_obj.id, 
                user_that_fixs_and_annots_it=user2_obj).fix_zh_with_image
            dic['user3'] = FixZhWithImage.objects.get(caption_id=caption_obj.id, 
                user_that_fixs_and_annots_it=user3_obj).fix_zh_with_image if user3_obj else None
            dic['id'] = caption_obj.caption_number
            data.append(dic)

        context = {
            'code': 0,
            'data': data,
        }
        return JsonResponse(context)

    raise Http404("非法访问了该api")

def show_zh_table(request):
    if request.is_ajax() and request.method == 'POST':
        image_id = int(request.POST.get('image_id'))
        caption_objs = Caption.objects.filter(image_obj_id=image_id).order_by('caption_number')
        data = []
        for caption_obj in caption_objs:
            dic = {}
            dic['zh_machine_translation'] = caption_obj.zh_machine_translation  # 机器翻译
            if caption_obj.zh_without_image_obj:   # 若有不看图片标注，选择歧义中正确的那个
                t = caption_obj.zh_without_image_obj
                dic['zh_without_image'] = t.zhs_without_image.split('\n')[t.correct_number]
            else:
                dic['zh_without_image'] = '未标注'
            if caption_obj.fix_zh_with_image_obj:   # 若有看图片标注，更新不看图片标注为fix_zh，它带HTML有更多信息
                t = caption_obj.fix_zh_with_image_obj
                dic['zh_without_image'] = t.fix_zh_with_image
                if t.zh_with_image: # 看图片标注存在
                    dic['zh_with_image'] = t.zh_with_image
            else:
                dic['zh_with_image'] = '未标注'
            dic['id'] = caption_obj.caption_number
            data.append(dic)

        context = {
            'code': 0,
            'data': data,
        }
        return JsonResponse(context)

    raise Http404("非法访问了该api")

def show_en_table(request):
    if request.is_ajax() and request.method == 'POST':
        image_id = int(request.POST.get('image_id'))
        caption_objs = Caption.objects.filter(image_obj_id=image_id).order_by('caption_number')
        data = []
        for caption_obj in caption_objs:
            dic = {}
            dic['caption'] = caption_obj.caption
            if caption_obj.zh_without_image_obj and caption_obj.zh_without_image_obj.user_thinks_caption_ambiguity:
                dic['is_ambiguity'] = 1
            else:
                dic['is_ambiguity'] = 0
            dic['id'] = caption_obj.caption_number
            data.append(dic)
        
        context = {
            'code': 0,
            'data': data,
        }
        return JsonResponse(context)

    raise Http404("非法访问了该api")

