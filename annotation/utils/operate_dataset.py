from torch import fix_
from annotation.models import FixZhWithImage, Caption, Image, FixInfo, User, ZhWithoutImage
from annotation.utils.deal_front_data import parse_html

def get_annotation_info():
    res = {
        'img_total_number': Image.objects.all().count(),
        'cap_total_number': Caption.objects.all().count(),
        'fix_zh_total_number': len(FixZhWithImage.objects.all()),
        'noun_error_number': 0,
        'verb_error_number': 0, 
        'adj_error_number': 0,
        'number_error_number': 0,
        'other_error_number': 0,
        'xihua_error_number': 0,
    }
    num = 0
    for fix_zh_obj in FixZhWithImage.objects.all(): 
        if fix_zh_obj.user_that_fixs_and_annots_it != User.objects.get(username='lch') and \
            'coco' in Caption.objects.get(id=fix_zh_obj.caption_id).image_obj.image_name:
            num += 1
            for i in parse_html(fix_zh_obj.fix_zh_with_image):
                if i[-1] == 1:
                    res['noun_error_number'] += 1
                elif i[-1] == 2:
                    res['verb_error_number'] += 1
                elif i[-1] == 3:
                    res['adj_error_number'] += 1
                elif i[-1] == 4:
                    res['number_error_number'] += 1
                elif i[-1] == 5:
                    res['other_error_number'] += 1
                else:
                    res['xihua_error_number'] += 1
    print(num)
    res['fix_zh_image_total_number'] = res['noun_error_number'] + res['verb_error_number'] + \
        res['adj_error_number'] + res['number_error_number'] + res['other_error_number'] + \
            res['xihua_error_number']
    return res