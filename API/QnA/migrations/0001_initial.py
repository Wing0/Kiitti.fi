# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'QnA_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'QnA', ['Customer'])

        # Adding model 'Topic'
        db.create_table(u'QnA_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Customer'], to_field='customer_id')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('follow_counter', self.gf('django.db.models.fields.IntegerField')()),
            ('question_counter', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Topic'])

        # Adding model 'Tag'
        db.create_table(u'QnA_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_use', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Customer'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('follow_counter', self.gf('django.db.models.fields.IntegerField')()),
            ('question_counter', self.gf('django.db.models.fields.IntegerField')()),
            ('course_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'QnA', ['Tag'])

        # Adding model 'Question'
        db.create_table(u'QnA_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Customer'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('view_counter', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'QnA_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Question'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'QnA', ['Answer'])

        # Adding model 'Comment'
        db.create_table(u'QnA_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('parent_question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Question'], blank=True)),
            ('parent_answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Answer'], blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'QnA', ['Comment'])

        # Adding model 'User'
        db.create_table(u'QnA_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'QnA', ['User'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'QnA_customer')

        # Deleting model 'Topic'
        db.delete_table(u'QnA_topic')

        # Deleting model 'Tag'
        db.delete_table(u'QnA_tag')

        # Deleting model 'Question'
        db.delete_table(u'QnA_question')

        # Deleting model 'Answer'
        db.delete_table(u'QnA_answer')

        # Deleting model 'Comment'
        db.delete_table(u'QnA_comment')

        # Deleting model 'User'
        db.delete_table(u'QnA_user')


    models = {
        u'QnA.answer': {
            'Meta': {'object_name': 'Answer'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Question']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        u'QnA.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Answer']", 'blank': 'True'}),
            'parent_question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Question']", 'blank': 'True'})
        },
        u'QnA.customer': {
            'Meta': {'object_name': 'Customer'},
            'customer_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'QnA.question': {
            'Meta': {'object_name': 'Question'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Customer']"}),
            'edited': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'view_counter': ('django.db.models.fields.IntegerField', [], {})
        },
        u'QnA.tag': {
            'Meta': {'object_name': 'Tag'},
            'course_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Customer']"}),
            'follow_counter': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_use': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'question_counter': ('django.db.models.fields.IntegerField', [], {})
        },
        u'QnA.topic': {
            'Meta': {'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Customer']", 'to_field': "'customer_id'"}),
            'follow_counter': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'question_counter': ('django.db.models.fields.IntegerField', [], {})
        },
        u'QnA.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['QnA']