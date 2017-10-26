'''
Created on Oct 26, 2017

@author: aqd14
'''
import os
from pathlib import Path
import json
import requests
from flickrapi import FlickrAPI
from pprint import pprint

config = json.load(open('../flickr.config'))

API_KEY = config['flickr-api-key']
DATA_DIR = os.path.join(Path().resolve().parent, 'data')
API_SECRET = config['flickr-api-secret']
EXTRA_URLS = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

flickr = FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

def prepare_dir(tags):
    category_dir = os.path.join(DATA_DIR, tags)
    if not os.path.isdir(category_dir):
        os.makedirs(category_dir)
    return category_dir

def download_image(url, file_name):
    content = requests.get(url, stream=True)
    if content.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in content.iter_content(1024):
                f.write(chunk)
    else:
        print('Can\'t download image at url: {0}'.format(url))

def flickr_query(tags, num_photos, photo_size):
    category_dir = prepare_dir(tags)
    
    photos = flickr.photos.search(tags=tags, per_page=10, sort='relevance', extras=EXTRA_URLS)
    urls = extract_urls(photos, photo_size)
    
    for url in urls:
        fname = extract_file_name(url)
        download_image(url, os.path.join(category_dir, fname))
    
def extract_urls(photos, photo_size):
    urls = []
    for photo in photos['photos']['photo']:
        url = photo[photo_size]
        urls.append(url)
        pprint(url)
    return urls

def extract_file_name(url):
    starting_cutoff = url.rindex('/') + 1
    return url[starting_cutoff:]

def main():
    flickr_query(tags='horse', num_photos=10, photo_size='url_z')
    
if __name__ == '__main__':
    main()
