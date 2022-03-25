from django.shortcuts import render

from annotation.models import Image
from annotation.utils.deal_end_data import image_url

def annotation_with_image(request):
    username = request.session.get("info")['username']
    res = {
        'now_index': 1,
        'image_id': 1,
        'image_name': image_url(Image.objects.get(id=1).image_name),
    }
    return render(request, 'annotation_with_image.html', res)