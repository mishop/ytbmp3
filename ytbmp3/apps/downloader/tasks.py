from __future__ import absolute_import

import os
import shutil
import subprocess
import uuid
import time

from django.conf import settings

from celery import shared_task

from ytbmp3.apps.downloader.models import Video, ActivityLog
from ytbmp3.apps.downloader.utils import create_filename, get_video_info

@shared_task
def convert(url, client_ip=None):
    """
    Convert the YouTube video to MP3 audio.

    Steps:
        1. Get the video's information to make sure the provided url is valid.
        2. If info is returned and the duration is no more than
           MAX_DURATION_SECONDS, log the request and start the conversion.
        3. Return the download link if conversion completes successfully.
    """
    info = get_video_info(url)

    result = None
    if info and info['duration'] <= settings.MAX_DURATION_SECONDS:
        youtube_id = info['id']
        title = info['title']

        audio_filename = create_filename(info['title'])

        video, created = Video.objects.get_or_create(youtube_id=youtube_id)
        video.url = url
        video.title = title
        video.duration = int(info['duration'])
        video.save()

        ActivityLog.objects.create(
            video=video,
            client_ip=client_ip,
            action=ActivityLog.CONVERT,
        )

        result = {
            'youtube_id': youtube_id,
            'title': title
        }

        # Simply return the filename and update the video object if the file
        # already exists, otherwise, start the conversion.
        output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)
        if os.path.exists(output_filepath):
            result['filename'] = audio_filename

            # Update the video object.
            video.audio_filename = audio_filename
            video.audio_filesize = os.path.getsize(output_filepath)
            video.save()
        else:
            conversion_result = start_conversion(url, audio_filename, video)

            # If extraction result is 0, extraction is successful.
            if conversion_result == 0:
                result['filename'] = audio_filename

    return result


def start_conversion(url, audio_filename, video):
    # process of converting the same video.
    # to change mp3 quality change --audio-quality (0-9) 0-best https://github.com/rg3/youtube-dl/issues/5673 
    output_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)
    result = subprocess.check_call([
        'python','-m',
        'youtube_dl','--no-playlist',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '4', 
        '--output',  str(output_filepath[:-4]) + '.%(ext)s',
        url,
    ])
    # Status code 0 is successful.
    if result == 0:
        # Update the video object.
        video.audio_filename = audio_filename
        video.audio_filesize = os.path.getsize(output_filepath)
        video.save()

    return result
