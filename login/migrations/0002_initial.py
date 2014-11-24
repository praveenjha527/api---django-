# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfiles'
        db.create_table(u'login_userprofiles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=500, blank=True)),
            ('fbid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('work', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'login', ['UserProfiles'])

        # Adding model 'Activities'
        db.create_table(u'login_activities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal(u'login', ['Activities'])

        # Adding model 'Events'
        db.create_table(u'login_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timing', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('starttime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.FloatField')()),
            ('isfreeze', self.gf('django.db.models.fields.BooleanField')()),
            ('activities', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'login', ['Events'])

        # Adding model 'Responses'
        db.create_table(u'login_responses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['login.Events'])),
            ('guest_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('confirmation_guest', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('confirmation_host', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('chat_freeze', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'login', ['Responses'])

        # Adding model 'Locations'
        db.create_table(u'login_locations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timing', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('latnlong', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'login', ['Locations'])


    def backwards(self, orm):
        # Deleting model 'UserProfiles'
        db.delete_table(u'login_userprofiles')

        # Deleting model 'Activities'
        db.delete_table(u'login_activities')

        # Deleting model 'Events'
        db.delete_table(u'login_events')

        # Deleting model 'Responses'
        db.delete_table(u'login_responses')

        # Deleting model 'Locations'
        db.delete_table(u'login_locations')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'login.activities': {
            'Meta': {'object_name': 'Activities'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'login.events': {
            'Meta': {'object_name': 'Events'},
            'activities': ('jsonfield.fields.JSONField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isfreeze': ('django.db.models.fields.BooleanField', [], {}),
            'location': ('django.db.models.fields.FloatField', [], {}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {}),
            'timing': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'login.locations': {
            'Meta': {'object_name': 'Locations'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latnlong': ('django.db.models.fields.FloatField', [], {}),
            'timing': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'login.responses': {
            'Meta': {'object_name': 'Responses'},
            'chat_freeze': ('django.db.models.fields.BooleanField', [], {}),
            'confirmation_guest': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'confirmation_host': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'event_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['login.Events']"}),
            'guest_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'login.userprofiles': {
            'Meta': {'object_name': 'UserProfiles'},
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fbid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '500', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'work': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['login']