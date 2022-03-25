import os

def split_ppl(_str):
    _str = str(_str)    # 将浮点型转换为字符串
    if _str == 'None':
        return _str
    if '.' not in _str[:5]:
        return '1w+'
    else:
        return _str[:5].strip()

def image_url(image_name):
    path_list = ['img']
    if 'flickr8k' in image_name:    # flickr8k有两个_
        path_list.extend(image_name.split('_')[:-2])
        path_list.append('_'.join(image_name.split('_')[-2:]))
    else:
        path_list.extend(image_name.split('_'))
    return os.path.join(*path_list)