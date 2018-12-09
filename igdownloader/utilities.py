'''
This module contains utility functions for parsing IG HTML source code
'''
from typing import List, Dict, Union, TypeVar

SessionObj = TypeVar('requests.Session()')


def save_page_content(url: str, session: SessionObj, filename: str) -> None:
    '''
    ::param url:: URL for an image or video
    ::param session:: requests.Session() object that is already logged in to IG
    ::param filename:: valid filename for image or video

    Save page content from a designated url
    '''
    resp = session.get(url)
    content = resp.content
    with open(filename, 'wb') as f:
        f.write(content)


def find_all_pic_vid_content(html_text: str) -> List[Dict[str, Union[str, int]]]:
    '''
    ::param html_text:: requests.get() return string of html source code
    ::return:: List of dictionaries with bounding indexes for all downloadable content on a page

    Finds all downloadable content on IG page and provides bounding indexes for the content. IG will encapsulate
    all pictures with ("GraphImage") and videos with ("GraphVideo").
    '''
    pictures = find_all_key_locs(html_text, key='"GraphImage"')
    videos = find_all_key_locs(html_text, key='"GraphVideo"')

    picture_library = []
    video_library = []

    if len(pictures) > 1:
        for picture_index_start, picture_index_end in zip(pictures[:-1], pictures[1:]):
            picture_library.append({'Type': 'Picture', 
                                    'Start': picture_index_start, 
                                    'End': picture_index_end})
    elif len(pictures) == 1:
        picture_library.append({'Type': 'Picture', 
                                'Start': pictures[0], 
                                'End': False})

    if len(videos) > 1:
        for video_index_start, video_index_end in zip(videos[:-1], videos[1:]):
            video_library.append({'Type': 'Video',
                                    'Start': video_index_start,
                                    'End': video_index_end})
    elif len(videos) == 1:
        video_library.append({'Type': 'Video',
                                'Start': video_index_start,
                                'End': video_index_end})

    return picture_library + video_library


def find_all_key_locs(html_text: str, key: str=None) -> List:
    '''
    ::param html_text:: requests.get() return string of html source code
    ::param key:: substring to be found within html_text
    ::return:: a list of all the indexes of the element appearing after the key
    
    # Example ----
    key = 'hello'

    my name is 'hello'_ the
    return -> 18 which is character "_"

    # Notes
    #key = '"config_width":' #multiple on page
    #video_key = '"video_url":' #only 1 on page if video
    #picture_key = '"src":'
    '''
    index = 0
    location = 0
    locations = []
    while location != -1:
        location = html_text.find(key, index)
        if location == -1:
            break
        else:
            locations.append(location + len(key))
            index = location + len(key)

    return locations


def find_best_pic_quality(html_text: str, key_config: str='"config_width":', key_img_url: str='"src":') -> int:
    '''
    ::param html_text:: requests.get() return string of html source code
    ::param key_config:: substring to be found multiple times with html
    ::param key_img_url:: substring that defines how to find img_url
    ::return:: index of the key_img_url for highest quality instance of key_config

    Finds all index locations of key instances in HTML and returns
    the index location of the "src" url of highest quality key (substring represents quality)
    '''
    # All locations is a list of indexes where the key appears
    all_locations = find_all_key_locs(html_text, key=key_config)

    # Quallities will be [(quality, index), (quality, index)]
    qualities = []
    for location in all_locations:
        quality = inner_dict_key_content(html_text, location)
        qualities.append((int(quality), location))
    sorted_qualities = sorted(qualities, key=lambda elm: elm[0])
    
    # The best "src": url is within these bounds
    start = sorted_qualities[-2][1]
    end = sorted_qualities[-1][1]
    best = find_all_key_locs(html_text[start:end], key=key_img_url)

    return best[0] + start


def inner_quote_content(html_text: str, start: int) -> str:
    '''
    ::param html_text:: requests.get() return string of html source code
    ::param start:: the beginning of a string that contains a substring contained by quotes
    ::return::
    # Example ----
    this is a test "string content" where i want to be returned -> string content

    Find all string content between next quotation mark and the one after that
    '''
    recording = False
    final_str = ''
    for elm in html_text[start:]:
        if elm == '"' and recording == False:
            recording = True
        elif elm =='"' and recording == True:
            break
        elif recording:
            final_str += elm

    return final_str

def inner_dict_key_content(html_text: str, start: int) -> str:
    '''
    ::param html_text:: requests.get() return string of html source code
    ::param start:: the beginning of a string that is ended by a ","
    ::return::
    # Example ----
    1293, -> 1293
    
    Find all string content before next ','
    Use this to parse dictionary key,value pairs
    '''
    final_str = ''
    for elm in html_text[start:]:
        if elm ==',':
            break
        else:
            final_str += elm

    return final_str