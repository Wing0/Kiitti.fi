# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'QnA_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'QnA', ['Organization'])

        # Adding model 'User'
        db.create_table(u'QnA_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Organization'], to_field='organization_id', null=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'QnA_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'QnA.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'QnA_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'QnA.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'AbstractMessage'
        db.create_table(u'QnA_abstractmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('message_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['AbstractMessage'])

        # Adding model 'Answer'
        db.create_table(u'QnA_answer', (
            (u'abstractmessage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['QnA.AbstractMessage'], unique=True, primary_key=True)),
            ('question_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'QnA', ['Answer'])

        # Adding model 'Question'
        db.create_table(u'QnA_question', (
            (u'abstractmessage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['QnA.AbstractMessage'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'QnA', ['Question'])

        # Adding model 'Comment'
        db.create_table(u'QnA_comment', (
            (u'abstractmessage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['QnA.AbstractMessage'], unique=True, primary_key=True)),
            ('is_question_comment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Comment'])

        # Adding model 'Vote'
        db.create_table(u'QnA_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rate', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id')),
            ('message_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['Vote'])

        # Adding model 'Tag'
        db.create_table(u'QnA_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id')),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63)),
            ('course_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'QnA', ['Tag'])

        # Adding model 'TagEntry'
        db.create_table(u'QnA_tagentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_entry_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Tag'], to_field='tag_id')),
            ('message_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'], to_field='user_id')),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['TagEntry'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'QnA_organization')

        # Deleting model 'User'
        db.delete_table(u'QnA_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'QnA_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'QnA_user_user_permissions'))

        # Deleting model 'AbstractMessage'
        db.delete_table(u'QnA_abstractmessage')

        # Deleting model 'Answer'
        db.delete_table(u'QnA_answer')

        # Deleting model 'Question'
        db.delete_table(u'QnA_question')

        # Deleting model 'Comment'
        db.delete_table(u'QnA_comment')

        # Deleting model 'Vote'
        db.delete_table(u'QnA_vote')

        # Deleting model 'Tag'
        db.delete_table(u'QnA_tag')

        # Deleting model 'TagEntry'
        db.delete_table(u'QnA_tagentry')


    models = {
        u'QnA.abstractmessage': {
            'Meta': {'object_name': 'AbstractMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'QnA.answer': {
            'Meta': {'object_name': 'Answer', '_ormbases': [u'QnA.AbstractMessage']},
            u'abstractmessage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['QnA.AbstractMessage']", 'unique': 'True', 'primary_key': 'True'}),
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'QnA.comment': {
            'Meta': {'object_name': 'Comment', '_ormbases': [u'QnA.AbstractMessage']},
            u'abstractmessage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['QnA.AbstractMessage']", 'unique': 'True', 'primary_key': 'True'}),
            'is_question_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Organization']"}),
            'tag_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'QnA.tagentry': {
            'Meta': {'object_name': 'TagEntry'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']", 'to_field': "'user_id'"})
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