# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table(u'poll_vote')

        # Deleting model 'Tag'
        db.delete_table(u'poll_tag')

        # Deleting field 'Choice.content'
        db.delete_column(u'poll_choice', 'content')

        # Adding field 'Choice.content_markdown'
        db.add_column(u'poll_choice', 'content_markdown',
                      self.gf('django.db.models.fields.TextField')(default=0, max_length=255),
                      keep_default=False)

        # Adding field 'Choice.content_markup'
        db.add_column(u'poll_choice', 'content_markup',
                      self.gf('django.db.models.fields.TextField')(default=0, max_length=255),
                      keep_default=False)

        # Removing M2M table for field tags on 'Question'
        db.delete_table(db.shorten_name(u'poll_question_tags'))


    def backwards(self, orm):
        # Adding model 'Vote'
        db.create_table(u'poll_vote', (
            ('vote_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('positive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Question'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('poll', ['Vote'])

        # Adding model 'Tag'
        db.create_table(u'poll_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('poll', ['Tag'])

        # Adding field 'Choice.content'
        db.add_column(u'poll_choice', 'content',
                      self.gf('django.db.models.fields.TextField')(default=0, max_length=255),
                      keep_default=False)

        # Deleting field 'Choice.content_markdown'
        db.delete_column(u'poll_choice', 'content_markdown')

        # Deleting field 'Choice.content_markup'
        db.delete_column(u'poll_choice', 'content_markup')

        # Adding M2M table for field tags on 'Question'
        m2m_table_name = db.shorten_name(u'poll_question_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['poll.question'], null=False)),
            ('tag', models.ForeignKey(orm['poll.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'tag_id'])


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Question']"}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Question']"})
        },
        u'poll.mcqanswer': {
            'Meta': {'object_name': 'MCQAnswer', '_ormbases': [u'poll.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['poll.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'poll.question': {
            'Meta': {'object_name': 'Question'},
            'content_markdown': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'content_markup': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['poll']