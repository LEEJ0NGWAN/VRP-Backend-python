import os
import setting
import boto3
import uuid
import datetime
import collections
from thread import Thread, _chunker

s3 = boto3.resource('s3',
aws_access_key_id=setting.aws_access_key_id,
aws_secret_access_key=setting.aws_secret_access_key)

bucket = s3.Bucket(setting.img_bucket_name)

panarama_img_name = 'sinput6.jpg'
panorama_img_path = os.getcwd()\
    + '/extract_panorama_partial.app/Contents/requestScreenShots/'

panorama_img_file = panorama_img_path + panarama_img_name

def downloads(keys, **kwargs):
    if type(keys) is str:
        download_(keys, panorama=True)
        return

    if len(keys) > 10:
        thread_list = [
            Thread(target=downloads, args=(keys_, ), kwargs=kwargs)
            for keys_ in _chunker(keys, 10)
        ]
        return

    [download_(key) for key in keys]

def download_(key, **kwargs):
    if kwargs.get('panorama', False):
        if not os.path.exists(os.path.dirname(panorama_img_path)):
            os.makedirs(os.path.dirname(panorama_img_path))
        try:
            bucket.download_file(key, panorama_img_file)
        except:
            pass

    else:
        # strip_pattern = kwargs.get('strip_pattern', '/vrp/events/')
        try:
            # bucket.download_file(key, key.strip(strip_pattern))
            pattern = './' + key
            bucket.download_file(key, pattern)
        except:
            pass


# scene: events/{event_id}/{scene_id}/{scene_file_location}
# evide: events/{event_id}/{scene_id}/{evidence_id}/{evidence_file_location}

