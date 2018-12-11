import sys
sys.path.append('../')

import requests
import time
from typing import List
from utilities import find_all_pic_vid_content, find_all_key_locs, inner_quote_content, find_best_pic_quality, save_page_content
from local.config import user_data
#Picture: /p/Bqf78O3FGn8a4XzKqovOvuwFK98CDtLSUu6DFY0/

def download_picture_page(session=None, page_url=None):
    '''

    '''

    # Step : Find best quality image
    # Find largest "config_width":1080
    session = session
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    base_url = 'https://www.instagram.com/p/'
    single_picture_url = base_url + page_url
    resp = session.get(single_picture_url, headers=headers, timeout=20)
    html_text = resp.text


    best_src_index = find_best_pic_quality(html_text)
    src_url = inner_quote_content(html_text, best_src_index)

    return src_url

session = requests.Session()
resp1 = session.get('https://www.instagram.com/accounts/login')
csrf_index = find_all_key_locs(resp1.text, key='"csrf_token":')[0]
csrf_token = inner_quote_content(resp1.text, csrf_index)

rollout_index = find_all_key_locs(resp1.text, key='"rollout_hash":')[0]
rollout_hash = inner_quote_content(resp1.text, rollout_index)

data = {
        'username': user_data['email'],
        'password': user_data['password'],
        'queryParams': {}
        }
headers = {'origin': 'https://www.instagram.com',
            'referer': 'referer: https://www.instagram.com/accounts/login/',
            'x-csrftoken': csrf_token,
            'x-instagram-ajax': rollout_hash,
            'x-requested-with': 'XMLHttpRequest'}

r = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers)
print('Did I login? : ', r.text)


# Rough skeleton of how to get best img url for a single image page
src_url = download_picture_page(session=session, page_url= '')
save_page_content(src_url, session, '../local/test2.jpg')
