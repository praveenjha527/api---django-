from django.db import models
from django.contrib.auth.models import User
from login.models import UserProfile, UserProfileManager, TimeStampedModel
from jsonfield import JSONField

class Notifications(TimeStampedModel):
    user = models.ForeignKey(UserProfile, unique=True, related_name='user_id')
    ANDROID = 0
    IOS = 1
    DEVICE_TYPE = (
        (ANDROID, 'android'),
        (IOS, 'ios'),
    )
    device_type = models.CharField(max_length=1, choices=DEVICE_TYPE, default=ANDROID)
    platform_endpoint = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    subscription_id = models.ManyToManyField(UserProfile, related_name='subscription_id')