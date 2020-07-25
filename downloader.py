import os
import setting
import boto3
import uuid
import datetime
import collections
from itertools import chain
from functools import singledispatch
from threading import current_thread
from threading import Thread as _Thread

s3 = boto3.resource('s3',
aws_access_key_id=setting.aws_access_key_id,
aws_secret_access_key=setting.aws_secret_access_key)

bucket = s3.Bucket(setting.img_bucket_name)

panarama_img_name = 'panorama_image.jpg'
panorama_img_path = os.getcwd()\
    + '/Unity_Build/PanoramaPartial_Data/requestScreenShots/'

panorama_img_file = panorama_img_path + panarama_img_name

class Thread(_Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group, target, name, args, kwargs)
        self.done = False
        self.result = None
        self.start()

    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

        self.done = True

    def join(self, timeout=None):
        if not self._initialized:
            raise RuntimeError("Thread.__init__() n t called")
        if not self._started.is_set():
            raise RuntimeError("cannot join thread before it is started")
        if self is current_thread():
            raise RuntimeError("cannot join current thread")

        if timeout is None:
            self._wait_for_tstate_lock()
        else:
            self._wait_for_tstate_lock(timeout=max(timeout, 0))
        if self.done:
            return self.result


def _chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

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
        strip_pattern = kwargs.get('strip_pattern', '/vrp/events/')
        try:
            bucket.download_file(key, key.strip(strip_pattern))
        except:
            pass


# scene: events/{event_id}/{scene_id}/{scene_file_location}
# evide: events/{event_id}/{scene_id}/{evidence_id}/{evidence_file_location}

