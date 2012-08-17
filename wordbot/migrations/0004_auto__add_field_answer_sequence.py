# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Answer.sequence'
        db.add_column('wordbot_answer', 'sequence',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Answer.sequence'
        db.delete_column('wordbot_answer', 'sequence')

    models = {
        'wordbot.answer': {
            'Meta': {'ordering': "['sequence', 'id']", 'object_name': 'Answer'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Question']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'wordbot.answerlog': {
            'Meta': {'object_name': 'AnswerLog'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Answer']"}),
            'buddy_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
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
        'wordbot.question': {
            'Meta': {'object_name': 'Question'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Survey']"})
        },
        'wordbot.result': {
            'Meta': {'object_name': 'Result'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Survey']"}),
            'weight_end': ('django.db.models.fields.IntegerField', [], {}),
            'weight_start': ('django.db.models.fields.IntegerField', [], {})
        },
        'wordbot.resultlog': {
            'Meta': {'object_name': 'ResultLog'},
            'buddy_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Result']"})
        },
        'wordbot.status': {
            'Meta': {'object_name': 'Status'},
            'buddy_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wordbot.Deck']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wordbot.survey': {
            'Meta': {'object_name': 'Survey'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['wordbot']