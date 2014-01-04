# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Comment.author'
        db.alter_column(u'QnA_comment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id'))

        # Changing field 'Comment.parent_answer'
        db.alter_column(u'QnA_comment', 'parent_answer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Answer'], to_field='answer_id'))
        # Adding field 'Answer.answer_id'
        db.add_column(u'QnA_answer', 'answer_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True),
                      keep_default=False)

        # Adding field 'User.user_id'
        db.add_column(u'QnA_user', 'user_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True),
                      keep_default=False)

        # Adding field 'User.reputation'
        db.add_column(u'QnA_user', 'reputation',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Comment.author'
        db.alter_column(u'QnA_comment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User']))

        # Changing field 'Comment.parent_answer'
        db.alter_column(u'QnA_comment', 'parent_answer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Answer']))
        # Deleting field 'Answer.answer_id'
        db.delete_column(u'QnA_answer', 'answer_id')

        # Deleting field 'User.user_id'
        db.delete_column(u'QnA_user', 'user_id')

        # Deleting field 'User.reputation'
        db.delete_column(u'QnA_user', 'reputation')


    models = {
        u'QnA.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Answer']", 'to_field': "'answer_id'"}),
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
            'reputation': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['QnA']