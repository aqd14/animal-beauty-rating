'''
Created on Oct 26, 2017

@author: aqd14
'''
import os
import json
import requests
from flickrapi import FlickrAPI
from pprint import pprint

config = json.load(open('../flickr.config'))

API_KEY = config['flickr-api-key']
IMAGE_DIR = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'test')
API_SECRET = config['flickr-api-secret']
EXTRA_URLS = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

flickr = FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

def prepare_dir(tags):
    category_dir = os.path.join(IMAGE_DIR, tags)
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

def flickr_query(tags, num_photos, per_page, photo_size):
    category_dir = prepare_dir(tags)
    print('Downloading photos with tag {}'.format(tags))
    urls = []
    for page in range(num_photos//per_page):
        photos = flickr.photos.search(tags=tags, per_page=per_page, page=page, sort='relevance', extras=EXTRA_URLS)
        urls.extend(extract_urls(photos, photo_size))
        print(len(urls))
    for num, url in enumerate(urls):
        print('[{}] Downloading url {}'.format(num, url))
        fname = extract_file_name(url)
        download_image(url, os.path.join(category_dir, fname))
        print('Finish downloading..!\n\n')
    print('Finish downloading photos with tag {}'.format(tags))


def extract_urls(photos, photo_size):
    urls = []
    for photo in photos['photos']['photo']:
        try:
            url = photo[photo_size]
            urls.append(url)
            pprint(url)
        except KeyError:
            print('Cannot extract url from photo {}'.format(photo))
            continue
    return urls

def extract_file_name(url):
    starting_cutoff = url.rindex('/') + 1
    return url[starting_cutoff:]

def main():
    num_photos = 500
    per_page = 50
    # flickr_query(tags='horse', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    flickr_query(tags='dog', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    flickr_query(tags='cat', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    flickr_query(tags='frog', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    flickr_query(tags='cow', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    flickr_query(tags='bird', num_photos=num_photos, per_page=per_page, photo_size='url_z')
    
if __name__ == '__main__':
    main()
