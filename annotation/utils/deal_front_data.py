import re

error_choices = {
    '名词': 1,
    '动词': 2,
    '形容词': 3,
    '数量': 4,
    '其他错误': 5,
    '描述细化': 6,
}

def parse_html(html):
    res = []
    span_length = 0

    title_start_list = [i.end() for i in re.finditer('title="', html)]
    title_end_list = [i.start() for i in re.finditer('">', html)]
    span_start_list = [i.start() for i in re.finditer('<span', html)]
    span_end_list = [i.start() for i in re.finditer('</span', html)]

    assert len(title_start_list) == len(title_end_list) == len(span_start_list) == len(span_end_list)

    for title_start, title_end, span_start, span_end in zip(title_start_list, title_end_list, span_start_list, span_end_list):
        span_length += title_end + 2 - span_start
        word_start = title_end + 2 - span_length
        word_end = span_end - span_length - 1

        error_number = error_choices[html[title_start:title_end].split('：')[0]]
        
        res.append((word_start, word_end, html[title_end + 2:span_end], html[title_start:title_end].split('：')[1], error_number))
        span_length += 7
    return res