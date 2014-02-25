# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import re
import hashlib


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)

    name     = models.CharField(max_length=255)
    address  = models.TextField(blank=True)

    created   = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)

    reputation    = models.IntegerField(default=0)
    organization  = models.ForeignKey(Organization, to_field='organization_id', null=True, blank=True)

    def __unicode__(self):
        return self.username


class Vote(models.Model):

    direction = models.SmallIntegerField(default=1)
    user      = models.ForeignKey(User, to_field="user_id")

    created   = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now_add=True, auto_now=True)


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)

    user         = models.ForeignKey(User, to_field="user_id")
    name         = models.CharField(max_length=63, unique=True)
    organization = models.ForeignKey(Organization)

    created   = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.name


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)

    content  = models.TextField()
    version  = models.PositiveIntegerField(default=1)
    user     = models.ForeignKey(User, to_field="user_id")

    # relation
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        unique_together = (('message_id', 'version'),
                           ('content_type', 'version'))
        db_table        = 'QnA_messages'
        get_latest_by   = 'created'

    def __unicode__(self):
        return "Message | pk: %d, version: %d, content: %s" \
               % (self.pk, self.version, self.content)


class MessageMixin(object):

    @property
    def message(self):
        """
        Returns the messages with highest version numver
        """
        content_type = ContentType.objects.get_for_model(self.__class__)

        messages = Message.objects.filter(
            content_type__pk=content_type.id,
            object_id=self.id).order_by('-version')

        if messages:
            message = messages

        if not message: message = None

        if not hasattr(self, "_message"):
            self._message = message

        return self._message


class AbstractMessage(models.Model, MessageMixin):

    messages = generic.GenericRelation(Message)
    votes    = generic.GenericRelation(Vote)

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        abstract = True


class Answer(AbstractMessage):
    '''
    Represents an answer to a question (Question()).
    '''
    accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'QnA_answers'


class Question(AbstractMessage):

    title  = models.CharField(max_length=512)
    tags   = generic.GenericRelation(Tag)

    class Meta:
        db_table = 'QnA_questions'


class Comment(AbstractMessage):

    class Meta:
        db_table = 'QnA_comments'


class TagEntry(models.Model):
    tag_entry_id = models.AutoField(primary_key=True)

    tag  = models.ForeignKey(Tag, to_field="tag_id")
    user = models.ForeignKey(User, to_field="user_id")

    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.tag.name


class ResetEntry(models.Model):
    user = models.ForeignKey(User, to_field="user_id")
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
