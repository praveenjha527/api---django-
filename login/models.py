#from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db import models
import json
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from datetime import datetime, timedelta
from django.db.models.query import QuerySet

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class GeneralManager(models.Manager):
    use_for_related_fields = True

    # a model manager to filter all the slots that have been created today and not any time in the past
    def istoday(self, **kwargs):
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        return self.filter(created__gte = today, **kwargs)

    def has_meeting(self, **kwargs):
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        return self.exclude(created__gte = today, accept_status = 1, **kwargs)

class UserProfileManager(BaseUserManager):

    def create_user(self, liid, email, actoken, first_name, last_name, password=None):

        if not liid:
            raise ValueError('User must have an liid')

        user = self.model(
           liid = liid,
           email= MyUserManager.normalize_email(email),
           actoken = actoken,
           first_name = first_name,
           last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

   # [TODO] [KP] Refactor ths using 'create_user' like in thotr
    def create_superuser(self, liid, email, actoken, first_name, last_name, password=None):

        if liid is None:
           raise ValueError('User must have an liid')

        user = self.model(
           liid = liid,
           email= MyUserManager.normalize_email(email),
           actoken = actoken,
           first_name = first_name,
           last_name=last_name,
        )
        user.is_admin = True
        return user

class UserProfile(AbstractBaseUser):

    liid = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=140)
    profile_picture = models.CharField(blank=True, null=True, max_length=500)
    profile_url = models.CharField(blank=True, null=True, max_length=500)
    education = JSONField(null=True)
    work = models.CharField(null=True, blank=True, max_length=200)
    dob = models.DateField(blank=True, null=True)
    skills = JSONField(null=True, blank=True)
    headline = models.CharField(null=True, blank=True, max_length=200)
    connections = JSONField(null=True, blank=True)
    positions = JSONField(null=True, blank=True)
    numconnections = models.IntegerField()
    groups = JSONField(null=True, blank=True)
    actoken = models.CharField(max_length=500)
    pastpositions = JSONField(null=True, blank=True)
    presentpositions = JSONField(null=True, blank=True)
    industry = models.CharField(null=True, blank=True, max_length=300)
    number_of_meetings = models.IntegerField(null=True, blank=True)
    percent_met = models.FloatField(null=True, blank=True)
    fav_users = models.ManyToManyField("self", symmetrical=False, related_name="favourites")
    block_users = models.ManyToManyField("self", symmetrical=False, related_name="blocked")

    USERNAME_FIELD = 'liid'
    REQUIRED_FIELDS = ['email', 'actoken']

    objects = UserProfileManager()

    def get_full_name(self):
        name = self.first_name + ' ' + self.last_name
        return name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):
        return self.get_full_name()

class Slots(TimeStampedModel):
    user = models.ForeignKey(UserProfile)
    slotno = models.IntegerField(blank=False, null=False)

    objects = GeneralManager()
	
    class Meta:
        unique_together = ('created', 'user', 'slotno')
            
class Responses(TimeStampedModel):
    from_id = models.ForeignKey(UserProfile, related_name='from_id')
    to_id = models.ForeignKey(UserProfile, related_name='to_id')
    slotno = models.IntegerField()
    DEFAULT = 0
    ACCEPT = 1
    REJECT = 2
    CONFIRMATION_STATUS = (
        (DEFAULT, 'default'),
        (ACCEPT, 'accept'),
        (REJECT, 'reject'),
    )
    accept_status = models.CharField(max_length=1,choices=CONFIRMATION_STATUS, default=DEFAULT)
    message = models.CharField(max_length=500, blank=True, null=True)

    objects = GeneralManager()
	
class Points(TimeStampedModel):
    user = models.ForeignKey(UserProfile)
    lat = models.FloatField()
    lon = models.FloatField()
    
    class Meta:
        db_table = 'login_point'