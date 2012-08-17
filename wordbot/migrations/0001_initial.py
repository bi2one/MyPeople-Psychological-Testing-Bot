# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OAuthToken'
        db.create_table('wordbot_oauthtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('consumer_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('wordbot', ['OAuthToken'])

        # Adding model 'BotInfo'
        db.create_table('wordbot_botinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oauth_token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordbot.OAuthToken'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('callback', self.gf('django.db.models.fields.CharField')(default='http://192.168.164.123:8000/', max_length=255)),
            ('profile_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('wordbot', ['BotInfo'])

        # Adding model 'Deck'
        db.create_table('wordbot_deck', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('wordbot', ['Deck'])

        # Adding model 'Card'
        db.create_table('wordbot_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordbot.Deck'])),
            ('side1', self.gf('django.db.models.fields.TextField')()),
            ('side2', self.gf('django.db.models.fields.TextField')()),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('flip_status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('wordbot', ['Card'])

        # Adding model 'Status'
        db.create_table('wordbot_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buddy_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wordbot.Deck'], null=True)),
        ))
        db.send_create_signal('wordbot', ['Status'])

    def backwards(self, orm):
        # Deleting model 'OAuthToken'
        db.delete_table('wordbot_oauthtoken')

        # Deleting model 'BotInfo'
        db.delete_table('wordbot_botinfo')

        # Deleting model 'Deck'
        db.delete_table('wordbot_deck')

        # Deleting model 'Card'
        db.delete_table('wordbot_card')

        # Deleting model 'Status'
        db.delete_table('wordbot_status')

    models = {
        'wordbot.botinfo': {
            'Meta': {'object_name': 'BotInfo'},
            'callback': ('django.db.models.fields.CharField', [], {'default': "'http://192.168.164.123:8000/'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'oauth_token': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.OAuthToken']"}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'wordbot.card': {
            'Meta': {'object_name': 'Card'},
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Deck']"}),
            'flip_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side1': ('django.db.models.fields.TextField', [], {}),
            'side2': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'wordbot.deck': {
            'Meta': {'object_name': 'Deck'},
            'buddy_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'wordbot.oauthtoken': {
            'Meta': {'object_name': 'OAuthToken'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wordbot.status': {
            'Meta': {'object_name': 'Status'},
            'buddy_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Deck']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['wordbot']