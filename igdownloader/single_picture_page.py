# Necessary when importing from sibling directories
import sys
sys.path.append('../')

import requests
import time
from typing import List
from utilities import (find_all_pic_vid_content, find_all_key_locs, 
                        inner_quote_content, find_best_pic_quality, 
                        save_page_content, login_session,
                        SessionObj
                        )

def download_picture_page_url(session: SessionObj=None, page_url: str=None) -> str:
    '''
    ::param session:: logged in requests Session object
    ::param page_url:: The Modal page displaying a set of images "/p/HASH/"
    ::return:: URL of downloadable picture or video from IG

    Use this to retireve the link for a downloadable picture or video from a single IG modal page
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    base_url = 'https://www.instagram.com/p/'
    single_picture_url = base_url + page_url
    resp = session.get(single_picture_url, headers=headers, timeout=20)
    html_text = resp.text
    best_src_index = find_best_pic_quality(html_text)
    src_url = inner_quote_content(html_text, best_src_index)

    return src_url

# Rough skeleton of how to get best img url for a single image page
session = login_session(requests.Session())
src_url = download_picture_page_url(session=session, page_url= 'BrMY-tUFONNJXaiPLl8YJqBPTEk1DKSPzLPjEY0/')
save_page_content(src_url, session, '../local/test2.jpg')
