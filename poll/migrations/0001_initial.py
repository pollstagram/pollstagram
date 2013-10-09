# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('poll_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('poll', ['Tag'])

        # Adding model 'Question'
        db.create_table('poll_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_markdown', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_markup', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('published_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Question'])

        # Adding M2M table for field tags on 'Question'
        m2m_table_name = db.shorten_name('poll_question_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['poll.question'], null=False)),
            ('tag', models.ForeignKey(orm['poll.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'tag_id'])

        # Adding model 'Choice'
        db.create_table('poll_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Question'])),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=255)),
        ))
        db.send_create_signal('poll', ['Choice'])

        # Adding model 'Vote'
        db.create_table('poll_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Question'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('vote_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('positive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('poll', ['Vote'])

        # Adding model 'Answer'
        db.create_table('poll_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Question'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('answer_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Answer'])

        # Adding model 'BinaryAnswer'
        db.create_table('poll_binaryanswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['poll.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('poll', ['BinaryAnswer'])

        # Adding model 'MCQAnswer'
        db.create_table('poll_mcqanswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['poll.Answer'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('poll', ['MCQAnswer'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('poll_tag')

        # Deleting model 'Question'
        db.delete_table('poll_question')

        # Removing M2M table for field tags on 'Question'
        db.delete_table(db.shorten_name('poll_question_tags'))

        # Deleting model 'Choice'
        db.delete_table('poll_choice')

        # Deleting model 'Vote'
        db.delete_table('poll_vote')

        # Deleting model 'Answer'
        db.delete_table('poll_answer')

        # Deleting model 'BinaryAnswer'
        db.delete_table('poll_binaryanswer')

        # Deleting model 'MCQAnswer'
        db.delete_table('poll_mcqanswer')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'poll.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'poll.binaryanswer': {
            'Meta': {'object_name': 'BinaryAnswer', '_ormbases': ['poll.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['poll.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'poll.choice': {
            'Meta': {'object_name': 'Choice'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Question']"})
        },
        'poll.mcqanswer': {
            'Meta': {'object_name': 'MCQAnswer', '_ormbases': ['poll.Answer']},
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['poll.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'poll.question': {
            'Meta': {'object_name': 'Question'},
            'content_markdown': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_markup': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['poll.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'poll.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'poll.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'positive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['poll']