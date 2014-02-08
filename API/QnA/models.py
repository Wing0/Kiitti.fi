from django.db import models
from django.contrib.auth.models import AbstractUser
from QnA.utils import *
import re

def format_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S')

class Organization(models.Model):

    organization_id = models.PositiveIntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    #image = models.ImageField()

    def __unicode__(self):
        return self.name

    def get_image():
        return None

    def serialize(self):
        jsondict = {
            'name': self.name,
            'address': self.address,
            'created': format_date(self.created),
            'modified': format_date(self.modified),
            'organizationId':self.organization_id
        }

        return jsondict

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate organization_id that is unique and ascending.
        '''
        if self.pk is None:
            # Create user actions
            orgobjects = Organization.objects.all()
            largest_id = max([0] + [org.organization_id for org in orgobjects])
            self.organization_id = largest_id
        # Just save
        super(Organization, self).save(*args, **kwargs)

    def validate(self):
        messages = []
        '''
        if not isinstance(self.organization_id, int) or self.organization_id < 0:
            valid = False
            messages.append({"type": "alert", "content": "Organization id must be a positive integer.", "identifier": "organization_id"})
        '''
        if not isinstance(self.name, basestring):
            messages.append(compose_message("Name has to be a string", "name"))
        if len(self.name) < 3:
            messages.append(compose_message("Name has to be at least 3 character long.", "name"))
        if not isinstance(self.address, basestring):
            messages.append(compose_message("Address has to be a string.", "address"))
        if len(self.address) < 3:
            messages.append(compose_message("Address has to be at least 3 character long.", "address"))
        return messages

class User(AbstractUser):

    user_id = models.PositiveIntegerField(unique=True)
    reputation = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, to_field='organization_id')

    def serialize(self):
        jsondict = {
            'username': self.username,
            'userId': self.user_id,
            'reputation': self.reputation,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'created': self.date_joined,
            'lastLogin': self.last_login
        }
        try:
            if self.organization.organization_id:
                jsondict["organizationId"] = self.organization.organization_id
        except:
            pass
        return jsondict

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate user_id that is unique and ascending.
        '''
        if self.pk is None:
            # Create user actions
            userobjects = User.objects.all()
            largest_id = max([0] + [user.user_id for user in userobjects])
            self.user_id = largest_id +1
            self.reputation = 0
        # Just save
        super(User, self).save(*args, **kwargs)

    def validate(self):
        valid = True
        messages = []

        if not isinstance(self.username, basestring):
            valid = False
            messages.append(compose_message("Username has to be a string.","username"))
        if not len(self.username) <= 255:
            valid = False
            messages.append(compose_message("Username has to be a shorter than 256 characters.","username"))
        if not len(self.username) >= 3:
            valid = False
            messages.append(compose_message("Username has to be a longer than 2 characters.","username"))

        if not isinstance(self.email, basestring):
            valid = False
            messages.append(compose_message("Email has to be a string.","email"))
        else:
            if not re.match("[^@]+@[^@]+\.[^@]+",self.email):
                valid = False
                messages.append(compose_message("Give a valid email address.","email"))
            else:
                retrieved_user = False
                try:
                    retrieved_user = User.objects.get(email=self.email)
                except:
                    retrieved_user = False
                if retrieved_user:
                    valid = False
                    messages.append(compose_message("Email already in use.","email"))

        if not isinstance(self.first_name, basestring):
            valid = False
            messages.append(compose_message("First name has to be a string.","first_name"))
        if not len(self.first_name) <= 255:
            valid = False
            messages.append(compose_message("First name has to be a shorter than 256 characters.","first_name"))
        if not len(self.first_name) >= 1:
            valid = False
            messages.append(compose_message("First name has to be at least 1 character.","first_name"))

        if not isinstance(self.last_name, basestring):
            valid = False
            messages.append(compose_message("Last name has to be a string.","last_name"))
        if not len(self.last_name) <= 255:
            valid = False
            messages.append(compose_message("Last name has to be a shorter than 256 characters.","last_name"))
        if not len(self.last_name) >= 1:
            valid = False
            messages.append(compose_message("Last name has to be at least 1 character.","last_name"))

        if not isinstance(self.password, basestring):
            valid = False
            messages.append(compose_message("Password has to be a string.","password"))
        if not len(self.password) <= 255:
            valid = False
            messages.append(compose_message("Password has to be a shorter than 256 characters.","password"))
        if not len(self.password) >= 4:
            valid = False
            messages.append(compose_message("Password has to be at least 4 character.","password"))

        if not isinstance(self.organization_id, int):
            valid = False
            messages.append(compose_message("Organization id has to be a integer.","organization_id"))
        else:
            Organization.objects.get()

        return valid, messages


class AbstractMessage(models.Model):
    '''
    This is the Abstract message class for all the message classes. The other message classes
    will inherit this class.
    '''
    content = models.TextField()
    version = models.PositiveIntegerField()
    user = models.ForeignKey(User, to_field="user_id")
    organization = models.ForeignKey(Organization, to_field="organization_id")
    created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)
    message_id = models.PositiveIntegerField()

    def serialize(self):
        jsondict = {
            'content': self.content,
            'version': self.version,
            'userId': self.user.user_id,
            'organizationId': self.organization.organization_id,
            'created': format_date(self.created),
            'messageId': self.message_id
        }

        return jsondict

    def validate(self):
        messages = []
        if not isinstance(self.content, basestring):
            messages.append(compose_message("Content must be a string.","content"))
        if len(self.content) < 1:
            messages.append(compose_message("Content is missing or its length is zero.", "content"))

        if not isinstance(self.user, User):
            messages.append(compose_message("User id must be an user object.","user_id"))

        if self.message_id != None and (not isinstance(self.message_id, int) or self.message_id < 0):
            messages.append(compose_message("Message id must be a positive number.","message_id"))
        return messages

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate message_id that is unique and ascending.
        '''
        if self.pk is None:
            # When created
            if not isinstance(self.version , int):
                self.version = 0
            # When created
            all_objects = AbstractMessage.objects.all()
            largest_id = max([0] + [obj.message_id for obj in all_objects])
            self.message_id = largest_id + 1
        # Just save
        super(AbstractMessage, self).save(*args, **kwargs)


class Answer(AbstractMessage):
    '''
    Represents an Answer for Question.

    '''
    question_id = models.PositiveIntegerField() #this is the message_id of the question this answer is response to
    accepted = models.BooleanField(default=False)

    def serialize(self):
        jsondict = super(Answer, self).serialize()
        jsondict['questionId'] = self.question_id
        jsondict['accepted'] = self.accepted

        return jsondict

    def validate(self):
        messages = super(Answer, self).validate()
        if not isinstance(self.question_id, int) or self.question_id < 0:
            valid = False
            messages.append(compose_message("Question id must be a positive integer.", "question_id"))
        if not isinstance(self.accepted, bool):
            valid = False
            messages.append(compose_message("Accepted value must be a boolean.", "accepted"))
        return messages

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate tag_entry_id that is unique and ascending.
        '''
        # Just save
        super(Answer, self).save(*args, **kwargs)


class Question(AbstractMessage):
    '''

    '''
    title = models.CharField(max_length=250)

    def __unicode__(self):
        return self.title

    def serialize(self):
        jsondict = super(Question, self).serialize()
        jsondict['title'] = self.title
        jsondict['tags'] = [tag_entry.tag.name for tag_entry in TagEntry.objects.filter(message_id=self.message_id)]
        jsondict['meta'] = {"number_of_answers":len(exclude_old_versions(list(Answer.objects.filter(question_id=self.message_id))))} #ToDo
        return jsondict

    def validate(self):
        messages = super(Question, self).validate()
        if not isinstance(self.title, basestring):
            messages.append(compose_message("Title has to be a string.", "title"))
        if self.title and len(self.title) < 5:
            messages.append(compose_message("Title must be atleast five characters long.",  "title"))
        return messages

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate message_id that is unique and ascending.
        '''
        super(Question, self).save(*args, **kwargs)

    def save_changes(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate version number that is unique and ascending.
        '''
        if self.pk is None:
            # When created
            all_versions = Question.objects.filter(message_id=self.message_id)
            largest_version = max([0] + [obj.version for obj in all_versions])
            self.version = largest_version + 1
        # Just save
        super(Question, self).save(*args, **kwargs)


class Comment(AbstractMessage):
    '''

    '''
    is_question_comment = models.BooleanField(default=False) #if true, this is a comment to a Question. If False, it is comment to an Answer.
    parent_id = models.PositiveIntegerField() #this is the message_id of the message to which this comment is for
    def serialize(self):
        jsondict = super(Comment, self).serialize()
        jsondict['parentId'] = self.parent_id
        return jsondict

    def validate(self):
        messages = super(Comment, self).validate()
        if not isinstance(self.parent_id, int) or self.parent_id < 0 :
            messages.append(compose_message("Parent id has to be a integer.", "parent_id"))
        if not isinstance(self.is_question_comment, bool):
            messages.append(compose_message("Is question value is not boolean.", "is_question_comment"))
        return messages

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate tag_entry_id that is unique and ascending.
        '''
        # Just save
        super(Comment, self).save(*args, **kwargs)

class Vote(models.Model):

    rate = models.SmallIntegerField(default=0)
    user = models.ForeignKey(User, to_field="user_id")
    message_id = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def serialize(self):
        jsondict = {
            'rate': self.rate,
            'userId': self.user.user_id,
            'messageId': self.message_id,
            'created': format_date(self.created),
            'modified': format_date(self.modified)
        }

        return jsondict

    def validate(self):
        messages = []
        if not isinstance(self.rate, int):
            messages.append(compose_message("Rate has to be a integer.", "rate"))
        if not isinstance(self.user.user_id, int) or self.user_id < 0:
            messages.append(compose_message("User id has to be a positive integer.", "userId"))
        if not isinstance(self.user.user_id, int) or self.message_id < 0:
            messages.append(compose_message("Message id has to be a positive integer.", "messageId"))

        return messages

class Tag(models.Model):
    tag_id = models.PositiveIntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    user = models.ForeignKey(User, to_field="user_id")
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=63, unique=True)
    course_flag = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def serialize(self):
        count = 0
        count = TagEntry.objects.filter(tag=self.tag_id).count()
        jsondict = {
            'tagId':self.tag_id,
            'user': self.user.user_id,
            'created': format_date(self.created),
            'modified': format_date(self.modified),
            'organizationId':self.organization.organization_id,
            'name':self.name,
            'courseFlag':self.course_flag,
            'count': count
        }

        return jsondict

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate tag_id that is unique and ascending.
        '''
        if self.pk is None:
            # When created
            all_objects = Tag.objects.all()
            largest_id = max([0] + [obj.tag_id for obj in all_objects])
            self.tag_id = largest_id +1
        # Just save
        super(Tag, self).save(*args, **kwargs)

    def validate(self):
        messages = []
        if not isinstance(self.name, basestring):
            messages.append(compose_message("Tag name has to be a string.", "name"))
        elif len(self.name) < 3:
            messages.append(compose_message("Tag name has to be longer than 3 characters.", "name"))
        elif len(self.name) > 255:
            messages.append(compose_message("Tag name has to be shorter than 255 characters.", "name"))
        if not isinstance(self.course_flag, bool):
            messages.append(compose_message("Course flag has to be a boolean value.", "courseFlag"))
        if not isinstance(self.organization, Organization):
            messages.append(compose_message("Organization has to be an Organization instance.", "organization"))
        if not isinstance(self.user, User):
            messages.append(compose_message("Creator has to be an User instance.", "creator"))
        return messages


class TagEntry(models.Model):
    tag_entry_id = models.PositiveIntegerField(unique=True)
    tag = models.ForeignKey(Tag, to_field="tag_id")
    message_id = models.PositiveIntegerField(default=0)

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    creator = models.ForeignKey(User, to_field="user_id")

    def __unicode__(self):
        return self.tag.name

    def serialize(self):
        jsondict = {
            'tagEntryId':self.tag_entry_id,
            'tagId':self.tag.tag_id,
            'messageId': self.message_id,
            'creator': self.creator.user_id,
            'created': format_date(self.created),
            'modified': format_date(self.modified),
        }

        return jsondict

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate tag_entry_id that is unique and ascending.
        '''
        if self.pk is None:
            # When created
            all_objects = TagEntry.objects.all()
            largest_id = max([0] + [obj.tag_entry_id for obj in all_objects])
            self.tag_entry_id = largest_id +1
        # Just save
        super(TagEntry, self).save(*args, **kwargs)


    def validate(self):
        messages = []
        if not isinstance(self.creator.user_id, int) or self.creator.user_id < 0:
            messages.append(compose_message("Creator must be a positive integer.", "creator"))
        '''
        if not isinstance(self.organization_id, int) or self.organization_id < 0:
            messages.append({"type": "alert", "content": "Organization id has to be a positive integer.", "identifier": "organization_id"})

        if not isinstance(self.name, int):
            messages.append({"type": "alert", "content": "Name has to be a string.", "identifier": "name"})

        if not len(self.name) > 0:
            messages.append({"type": "alert", "content": "Name has to be atleast 1 character long.", "identifier": "name"})

        if not isinstance(self.course_flag, bool):
            messages.append({"type": "alert", "content": "Course flag must be a boolean.", "identifier": "course_flag"})
        '''
        return messages

'''
ToDo:
    User object
        How do they relate to Customer?
            Do we need customer-specific users
            ForeignKey to customer -> custom user class
        How do we relate to the user?
            separate id instead of primary_key?
        Custom user class or not?
            If it is custom, could we include user profile attributes as well?
        Could single user be registered to several customers?

    User profile model:
        Reputation
        Avatar
        Rights
        Events
        etc.

'''
