# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagEntry'
        db.create_table(u'QnA_tagentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_entry_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Tag'], to_field='tag_id')),
            ('message_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['TagEntry'])

        # Adding field 'Comment.comment_id'
        db.add_column(u'QnA_comment', 'comment_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=123),
                      keep_default=False)

        # Adding field 'Answer.answer_id'
        db.add_column(u'QnA_answer', 'answer_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=123),
                      keep_default=False)


        # Changing field 'Vote.message_id'
        db.alter_column(u'QnA_vote', 'message_id', self.gf('django.db.models.fields.PositiveIntegerField')())
        # Deleting field 'Tag.organization_id'
        db.delete_column(u'QnA_tag', 'organization_id_id')

        # Deleting field 'Tag.follow_counter'
        db.delete_column(u'QnA_tag', 'follow_counter')

        # Deleting field 'Tag.question_counter'
        db.delete_column(u'QnA_tag', 'question_counter')

        # Adding field 'Tag.tag_id'
        db.add_column(u'QnA_tag', 'tag_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=123, unique=True),
                      keep_default=False)

        # Adding field 'Tag.organization'
        db.add_column(u'QnA_tag', 'organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=123, to=orm['QnA.Organization']),
                      keep_default=False)


        # Changing field 'Tag.name'
        db.alter_column(u'QnA_tag', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63))
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique(u'QnA_tag', ['name'])


        # Changing field 'Tag.creator'
        db.alter_column(u'QnA_tag', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User']))
        # Deleting field 'Question.topic'
        db.delete_column(u'QnA_question', 'topic')

        # Adding field 'Question.title'
        db.add_column(u'QnA_question', 'title',
                      self.gf('django.db.models.fields.CharField')(default='asdasd', max_length=250),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique(u'QnA_tag', ['name'])

        # Deleting model 'TagEntry'
        db.delete_table(u'QnA_tagentry')

        # Deleting field 'Comment.comment_id'
        db.delete_column(u'QnA_comment', 'comment_id')

        # Deleting field 'Answer.answer_id'
        db.delete_column(u'QnA_answer', 'answer_id')


        # Changing field 'Vote.message_id'
        db.alter_column(u'QnA_vote', 'message_id', self.gf('django.db.models.fields.IntegerField')())
        # Adding field 'Tag.organization_id'
        db.add_column(u'QnA_tag', 'organization_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=123, to=orm['QnA.Organization'], to_field='organization_id'),
                      keep_default=False)

        # Adding field 'Tag.follow_counter'
        db.add_column(u'QnA_tag', 'follow_counter',
                      self.gf('django.db.models.fields.IntegerField')(default=5),
                      keep_default=False)

        # Adding field 'Tag.question_counter'
        db.add_column(u'QnA_tag', 'question_counter',
                      self.gf('django.db.models.fields.IntegerField')(default=123),
                      keep_default=False)

        # Deleting field 'Tag.tag_id'
        db.delete_column(u'QnA_tag', 'tag_id')

        # Deleting field 'Tag.organization'
        db.delete_column(u'QnA_tag', 'organization_id')


        # Changing field 'Tag.name'
        db.alter_column(u'QnA_tag', 'name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'Tag.creator'
        db.alter_column(u'QnA_tag', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id'))
        # Adding field 'Question.topic'
        db.add_column(u'QnA_question', 'topic',
                      self.gf('django.db.models.fields.CharField')(default='ASD', max_length=250),
                      keep_default=False)

        # Deleting field 'Question.title'
        db.delete_column(u'QnA_question', 'title')


    models = {
        u'QnA.abstractmessage': {
            'Meta': {'object_name': 'AbstractMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'QnA.answer': {
            'Meta': {'object_name': 'Answer', '_ormbases': [u'QnA.AbstractMessage']},
            u'abstractmessage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['QnA.AbstractMessage']", 'unique': 'True', 'primary_key': 'True'}),
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'answer_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'QnA.comment': {
            'Meta': {'object_name': 'Comment', '_ormbases': [u'QnA.AbstractMessage']},
            u'abstractmessage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['QnA.AbstractMessage']", 'unique': 'True', 'primary_key': 'True'}),
            'comment_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'QnA.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'QnA.question': {
            'Meta': {'object_name': 'Question', '_ormbases': [u'QnA.AbstractMessage']},
            u'abstractmessage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['QnA.AbstractMessage']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'QnA.tag': {
            'Meta': {'object_name': 'Tag'},
            'course_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Organization']"}),
            'tag_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'QnA.tagentry': {
            'Meta': {'object_name': 'TagEntry'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Tag']", 'to_field': "'tag_id'"}),
            'tag_entry_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'QnA.user': {
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
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Organization']", 'to_field': "'organization_id'", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'QnA.vote': {
            'Meta': {'object_name': 'Vote'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['QnA']