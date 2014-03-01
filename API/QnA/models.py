# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import hashlib


class RIDMixin(models.Model):

    rid = models.PositiveIntegerField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        # Saves unique resource identifier automatically
        rid_dict = self._default_manager.all().aggregate(models.Max('rid'))
        max_rid = rid_dict['rid__max']

        if max_rid < settings.RID_MINIMUM_VALUE:
            max_rid = settings.RID_MINIMUM_VALUE - 1

        self.rid = max_rid + 1

        super(RIDMixin, self).save(*args, **kwargs)


class TimestampMixin(models.Model):

    created   = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True


class Organization(RIDMixin, TimestampMixin):

    name     = models.CharField(max_length=255)
    address  = models.TextField(blank=True)

    class Meta:
        db_table = 'QnA_organizations'

    def __unicode__(self):
        return self.name


class User(AbstractUser, RIDMixin):

    reputation    = models.IntegerField(default=0)
    organization  = models.ForeignKey(Organization, null=True, blank=True)

    class Meta:
        db_table = 'QnA_users'

    def __unicode__(self):
        return self.username


class Vote(TimestampMixin):

    direction = models.SmallIntegerField(default=1)
    user      = models.ForeignKey(User)

    # relation
    head_type  = models.ForeignKey(ContentType)
    head_id    = models.PositiveIntegerField()
    head       = generic.GenericForeignKey('head_type', 'head_id')

    class Meta:
        db_table = 'QnA_votes'


class Category(RIDMixin):

    title       = models.CharField(max_length=512)
    description = models.TextField()

    class Meta:
        db_table = 'QnA_categories'

    def __unicode__(self):
        return self.title


class Keyword(models.Model):

    content = models.CharField(max_length=63, unique=True)
    category = models.ManyToManyField(Category, blank=True, null=True)

    class Meta:
        db_table = 'QnA_keywords'

    def __unicode__(self):
        return self.content


class Tag(RIDMixin, TimestampMixin):

    keyword      = models.ForeignKey(Keyword)
    user         = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)

    # relation
    head_type  = models.ForeignKey(ContentType)
    head_id    = models.PositiveIntegerField()
    head       = generic.GenericForeignKey('head_type', 'head_id')

    class Meta:
        db_table = 'QnA_tags'

    def __unicode__(self):
        return "%s for ID%d" % (self.keyword.content, self.head_id)


class Message(TimestampMixin):

    content  = models.TextField()
    version  = models.PositiveIntegerField(default=1)
    user     = models.ForeignKey(User)

    # relation
    head_type  = models.ForeignKey(ContentType)
    head_id    = models.PositiveIntegerField()
    head       = generic.GenericForeignKey('head_type', 'head_id')

    class Meta:
        unique_together = (('id', 'version'),)
        db_table        = 'QnA_messages'
        get_latest_by   = 'created'

    def __unicode__(self):
        return "Message | pk: %d, version: %d, content: %s type: %s" \
               % (self.pk, self.version, self.content, self.head_type)

    def save(self, *args, **kwargs):

        # Increment version number automatically
        max_version_dict = self._default_manager.filter(
                        head_type=self.head_type,
                        head_id=self.head_id).aggregate(models.Max('version'))
        max_version = max_version_dict['version__max']

        if max_version:
            self.version = max_version + 1
        else:
            self.version = 1

        super(Message, self).save(*args, **kwargs)



class CommentMixin(object):

    @property
    def comments(self):
        head_type = ContentType.objects.get_for_model(self.__class__)

        comments = Comment.objects.filter(
            head_type__pk=head_type.id,
            head_id=self.id)

        if not hasattr(self, "_comments"):
            self._comments = message

        return self._comments


class AbstractMessage(RIDMixin, TimestampMixin):

    user     = models.ForeignKey(User)

    messages = generic.GenericRelation(Message,
                    content_type_field='head_type',
                    object_id_field='head_id')
    votes    = generic.GenericRelation(Vote,
                    content_type_field='head_type',
                    object_id_field='head_id')

    class Meta:
        abstract = True

    @property
    def message(self):
        """
        Returns the message with highest version number
        """
        head_type = ContentType.objects.get_for_model(self.__class__)

        messages = Message.objects.filter(
            head_type__pk=head_type.id,
            head_id=self.id).order_by('-version', '-created')

        if messages:
            message = messages[0]
            # one could raise error here if len(messages) > 0
        else:
            message = None

        if not hasattr(self, "_message"):
            self._message = message

        return self._message

    @property
    def votes_up(self):
        head_type = ContentType.objects.get_for_model(self.__class__)

        votes = Vote.objects.filter(
            head_type__pk=head_type.id,
            head_id=self.id)
        return len(votes.filter(direction=1))

    @property
    def votes_down(self):
        head_type = ContentType.objects.get_for_model(self.__class__)

        votes = Vote.objects.filter(
            head_type__pk=head_type.id,
            head_id=self.id)
        return len(votes.filter(direction=-1))


class Comment(AbstractMessage):

    # relation
    head_type  = models.ForeignKey(ContentType)
    head_id    = models.PositiveIntegerField()
    head       = generic.GenericForeignKey('head_type', 'head_id')

    class Meta:
        db_table = 'QnA_comments'


class Question(AbstractMessage, CommentMixin):

    title  = models.CharField(max_length=512)
    tags   = generic.GenericRelation(Tag,
                    content_type_field='head_type',
                    object_id_field='head_id')

    comments = generic.GenericRelation(Comment,
                    content_type_field='head_type',
                    object_id_field='head_id')

    class Meta:
        db_table = 'QnA_questions'


class Answer(AbstractMessage, CommentMixin):
    '''
    Represents an answer to a question (Question()).
    '''
    question = models.ForeignKey(Question, related_name='answers')
    accepted = models.BooleanField(default=False)

    comments = generic.GenericRelation(Comment,
                    content_type_field='head_type',
                    object_id_field='head_id')

    class Meta:
        db_table = 'QnA_answers'


class ResetEntry(models.Model):
    user = models.ForeignKey(User)
    salt = models.CharField(max_length=5)

    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self, has):
        if self.create() == has:
            return True
        return False

    def create(self):
        secret = "supercoderz"
        m = hashlib.sha256()
        m.update(self.user.email + self.salt + self.user.username + secret)
        has = m.hexdigest()

        return has[:10]
