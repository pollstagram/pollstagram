# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'poll_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_markdown', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('content_markup', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('content_rawtext', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('published_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'poll', ['Question'])

        # Adding model 'Choice'
        db.create_table(u'poll_choice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Question'])),
            ('content_markdown', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('content_markup', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('content_rawtext', self.gf('django.db.models.fields.TextField')(max_length=255)),
        ))
        db.send_create_signal(u'poll', ['Choice'])

        # Adding model 'Answer'
        db.create_table(u'poll_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Choice'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answer_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'poll', ['Answer'])

        # Adding model 'BinaryAnswer'
        db.create_table(u'poll_binaryanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['poll.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'poll', ['BinaryAnswer'])

        # Adding model 'MCQAnswer'
        db.create_table(u'poll_mcqanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['poll.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'poll', ['MCQAnswer'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'poll_question')

        # Deleting model 'Choice'
        db.delete_table(u'poll_choice')

        # Deleting model 'Answer'
        db.delete_table(u'poll_answer')

        # Deleting model 'BinaryAnswer'
        db.delete_table(u'poll_binaryanswer')

        # Deleting model 'MCQAnswer'
        db.delete_table(u'poll_mcqanswer')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'poll.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Choice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'poll.binaryanswer': {
            'Meta': {'object_name': 'BinaryAnswer', '_ormbases': [u'poll.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['poll.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'poll.choice': {
            'Meta': {'object_name': 'Choice'},
            'content_markdown': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'content_markup': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'content_rawtext': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Question']"})
        },
        u'poll.mcqanswer': {
            'Meta': {'object_name': 'MCQAnswer', '_ormbases': [u'poll.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['poll.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'poll.question': {
            'Meta': {'ordering': "['-published_time']", 'object_name': 'Question'},
            'content_markdown': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'content_markup': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'content_rawtext': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['poll']