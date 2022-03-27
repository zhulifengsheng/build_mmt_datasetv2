from django.http import Http404
from django.shortcuts import render

from annotation.models import User
from annotation.utils.operate_dataset import get_annotation_info

def statis(request):
    username = request.session.get("info")['username']
    if User.objects.get(username=username).is_admin:
        res = get_annotation_info()
        return render(request, "statis.html", res)
    
    raise Http404('非管理员访问')