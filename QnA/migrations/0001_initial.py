# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('QnA_organizations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'QnA', ['Organization'])

        # Adding model 'User'
        db.create_table('QnA_users', (
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
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name('QnA_users_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'QnA.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name('QnA_users_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'QnA.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'Vote'
        db.create_table('QnA_votes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('direction', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
        ))
        db.send_create_signal(u'QnA', ['Vote'])

        # Adding model 'Category'
        db.create_table('QnA_categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'QnA', ['Category'])

        # Adding model 'Keyword'
        db.create_table('QnA_keywords', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63)),
        ))
        db.send_create_signal(u'QnA', ['Keyword'])

        # Adding M2M table for field category on 'Keyword'
        m2m_table_name = db.shorten_name('QnA_keywords_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('keyword', models.ForeignKey(orm[u'QnA.keyword'], null=False)),
            ('category', models.ForeignKey(orm[u'QnA.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['keyword_id', 'category_id'])

        # Adding model 'Tag'
        db.create_table('QnA_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Keyword'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.Organization'])),
            ('head_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('head_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Tag'])

        # Adding model 'Message'
        db.create_table('QnA_messages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('head_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('head_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Message'])

        # Adding unique constraint on 'Message', fields [u'id', 'version']
        db.create_unique('QnA_messages', [u'id', 'version'])

        # Adding model 'Comment'
        db.create_table('QnA_comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('head_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('head_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'QnA', ['Comment'])

        # Adding model 'Question'
        db.create_table('QnA_questions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'QnA', ['Question'])

        # Adding model 'Answer'
        db.create_table('QnA_answers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rid', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['QnA.Question'])),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'QnA', ['Answer'])

        # Adding model 'ResetEntry'
        db.create_table(u'QnA_resetentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['QnA.User'])),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'QnA', ['ResetEntry'])


    def backwards(self, orm):
        # Removing unique constraint on 'Message', fields [u'id', 'version']
        db.delete_unique('QnA_messages', [u'id', 'version'])

        # Deleting model 'Organization'
        db.delete_table('QnA_organizations')

        # Deleting model 'User'
        db.delete_table('QnA_users')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name('QnA_users_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name('QnA_users_user_permissions'))

        # Deleting model 'Vote'
        db.delete_table('QnA_votes')

        # Deleting model 'Category'
        db.delete_table('QnA_categories')

        # Deleting model 'Keyword'
        db.delete_table('QnA_keywords')

        # Removing M2M table for field category on 'Keyword'
        db.delete_table(db.shorten_name('QnA_keywords_category'))

        # Deleting model 'Tag'
        db.delete_table('QnA_tags')

        # Deleting model 'Message'
        db.delete_table('QnA_messages')

        # Deleting model 'Comment'
        db.delete_table('QnA_comments')

        # Deleting model 'Question'
        db.delete_table('QnA_questions')

        # Deleting model 'Answer'
        db.delete_table('QnA_answers')

        # Deleting model 'ResetEntry'
        db.delete_table(u'QnA_resetentry')


    models = {
        u'QnA.answer': {
            'Meta': {'object_name': 'Answer', 'db_table': "'QnA_answers'"},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['QnA.Question']"}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        u'QnA.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'QnA_categories'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'QnA.comment': {
            'Meta': {'object_name': 'Comment', 'db_table': "'QnA_comments'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'head_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        u'QnA.keyword': {
            'Meta': {'object_name': 'Keyword', 'db_table': "'QnA_keywords'"},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['QnA.Category']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'QnA.message': {
            'Meta': {'unique_together': "(('id', 'version'),)", 'object_name': 'Message', 'db_table': "'QnA_messages'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'head_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'QnA.organization': {
            'Meta': {'object_name': 'Organization', 'db_table': "'QnA_organizations'"},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'})
        },
        u'QnA.question': {
            'Meta': {'object_name': 'Question', 'db_table': "'QnA_questions'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'QnA.resetentry': {
            'Meta': {'object_name': 'ResetEntry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"})
        },
        u'QnA.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'QnA_tags'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'head_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Keyword']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Organization']"}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"})
        },
        u'QnA.user': {
            'Meta': {'object_name': 'User', 'db_table': "'QnA_users'"},
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
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.Organization']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rid': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'QnA.vote': {
            'Meta': {'object_name': 'Vote', 'db_table': "'QnA_votes'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['QnA.User']"})
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