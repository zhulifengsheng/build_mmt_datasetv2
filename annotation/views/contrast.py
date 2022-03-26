from django.http import Http404
from django.shortcuts import render

from annotation.models import Caption, User, ZhWithoutImage, FixZhWithImage

def _get_image_set(user_zh):
    if user_zh and user_zh.exists():    # user_zh存在且QuerySet集合中有值
        res = []
        for i in user_zh:
            if 'coco' in Caption.objects.get(id=i.caption_id).image_obj.image_name:
                res.append(Caption.objects.get(id=i.caption_id).image_obj_id)
        return set(res)
        return set([Caption.objects.get(id=i.caption_id).image_obj_id for i in user_zh])
    return None

def contrast(request):
    if request.method == 'POST':
        # which: 0是不看图片标注，1是看图片标注
        which = request.POST.get('which')
        user1 = request.POST.get('user1')
        user2 = request.POST.get('user2')
        user3 = request.POST.get('user3') # user3可以为空
        
        user1_obj = User.objects.get(username=request.POST.get('user1'))
        user2_obj = User.objects.get(username=request.POST.get('user2'))
        user3_obj = User.objects.get(username=request.POST.get('user3')) if user3 != '' else None
        
        if which == '0':
            # TODO 对比不看图片标注
            user1_zh = ZhWithoutImage.objects.filter(user_that_annots_it=user1_obj)
            user2_zh = ZhWithoutImage.objects.filter(user_that_annots_it=user2_obj)
            caption_list = list(set([i.caption_id for i in user1_zh]) & set([i.caption_id for i in user2_zh]))
            print(len(caption_list))

        elif which == '1':
            # 对比不看图片标注 user*_zh: <QuerySet []> | None
            user1_zh = FixZhWithImage.objects.filter(user_that_fixs_and_annots_it=user1_obj)
            user2_zh = FixZhWithImage.objects.filter(user_that_fixs_and_annots_it=user2_obj)
            user3_zh = FixZhWithImage.objects.filter(user_that_fixs_and_annots_it=user3_obj) if user3_obj else None
            # user*_set: Set | None
            user1_set = _get_image_set(user1_zh)
            user2_set = _get_image_set(user2_zh)
            user3_set = _get_image_set(user3_zh)
            if user1_set and user2_set: # 前两个用户必须得标注过看图片标注
                if user3_set:
                    image_id_list = list(user1_set & user2_set & user3_set)
                image_id_list = list(user1_set & user2_set)
            else:
                image_id_list = []
            
            if len(image_id_list) == 0: # 没有公共标注的内容
                res = {
                    'usernames': [ i.username for i in User.objects.all()],
                    'error_msg': True,
                }
                return render(request, "contrast.html", res)
            
            image_id_list.sort()    # 排序为了每次返回的结果一致
            res = {     # 有公共标注的内容
                'user1': user1,
                'user2': user2, 
                'user3': user3,
                'has_user3': True if user3 != '' else False,    # 是否询问了第三个用户
                'image_id_list': image_id_list, # TODO，应该存入临时数据表中，而不是发送一堆数据给前端
            }
            return render(request, "contrast_with_image.html", res)
        else:
            raise Http404('前端发送了错误的对比信息')

    # GET方法
    res = {
        'usernames': [ i.username for i in User.objects.all()],
        'error_msg': False,
    }
    return render(request, "contrast.html", res)
   