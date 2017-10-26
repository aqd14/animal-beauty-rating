'''
Created on Oct 26, 2017

@author: aqd14
'''

import json
import requests
from flickrapi import FlickrAPI
from pprint import pprint


config = json.load(open('./flickr.config'))

DATA_DIR = './data'
API_KEY = config['flickr_api_key']
API_SECRET = config['flickr_api_secret']

def download_image(url, file_name):
    content = requests.get(url, stream=True)
    if content.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in content.iter_content(1024):
                f.write(chunk)
    else:
        print('Can\'t download image at url: {0}'.format(url))

flickr = FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
cats = flickr.photos.search(tags=['cat', 'dogs'], per_page=5, extras=extras)
url = cats['photos']['photo'][1]['url_s']
# print(type(photos))
pprint(url)

if __name__ == 'main':
    download_image(url, 'test.jpg')        