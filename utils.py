"""Custom S3 storage backends to store files in subfolders."""
import pusher

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

MediaRootS3BotoStorage = lambda: S3BotoStorage(location='crm')

def trigger_notification(channel, event, msg, status, id_, time_):
    p = pusher.Pusher(app_id=settings.PUSHER_APP_ID, 
    				  key=settings.PUSHER_KEY,
                      secret=settings.PUSHER_SECRET,
                      ssl=True)
    time_ = time_.strftime('%Y-%m-%d %H:%M:%S')
    p.trigger(channel, event, {'message': msg, 'status': status, 'id': id_, 'time': time_})
