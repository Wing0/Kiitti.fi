from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):

    organization_id = models.PositiveIntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    #image = models.ImageField()

    def get_image():
        return null

    def serialize(self):
        jsondict = {
            'name': self.name,
            'address': self.address,
            'created': self.created,
            'modified': self.modified
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

class User(AbstractUser):

    user_id = models.PositiveIntegerField(unique=True)
    reputation = models.IntegerField(default=0)
    organization_id = models.ForeignKey(Organization, to_field=organization_id, blank=True, null=True)

    def serialize(self):
        jsondict = {
            'username': self.username,
            'userId': self.user_id,
            'reputation': self.reputation,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'created': self.date_joined,
            'lastLogin': self.last_login,
            'organizationId': self.organization_id
        }

        return jsondict

    def save(self, *args, **kwargs):
        '''
            The default save method is overridden to be able to generate appropriate user_id that is unique and ascending.
        '''
        if self.pk is None:
            # Create user actions
            userobjects = User.objects.all()
            largest_id = max([0] + [user.user_id for user in userobjects])
            self.user_id = largest_id
            self.reputation = 0
        # Just save
        super(User, self).save(*args, **kwargs)

    def validate(self):
        valid = True
        messages = []

        if not isinstance(self.username, basetext):
            valid = False
            messages.append({"type":"alert","content":"Username has to be a string.","identifier":"username"})
        if not len(self.username) <= 255:
            valid = False
            messages.append({"type":"alert","content":"Username has to be a shorter than 256 characters.","identifier":"username"})
        if not len(self.username) >= 3:
            valid = False
            messages.append({"type":"alert","content":"Username has to be a longer than 2 characters.","identifier":"username"})

        if not isinstance(self.email, basetext):
            valid = False
            messages.append({"type":"alert","content":"Email has to be a string.","identifier":"email"})
        if not re.match("[^@]+@[^@]+\.[^@]+",self.email):
            valid = False
            messages.append({"type":"alert","content":"Give a valid email address.","identifier":"email"})

        if not isinstance(self.first_name, basetext):
            valid = False
            messages.append({"type":"alert","content":"First name has to be a string.","identifier":"first_name"})
        if not len(self.first_name) <= 255:
            valid = False
            messages.append({"type":"alert","content":"First name has to be a shorter than 256 characters.","identifier":"first_name"})
        if not len(self.first_name) >= 1:
            valid = False
            messages.append({"type":"alert","content":"First name has to be at least 1 character.","identifier":"first_name"})

        if not isinstance(self.last_name, basetext):
            valid = False
            messages.append({"type":"alert","content":"Last name has to be a string.","identifier":"last_name"})
        if not len(self.last_name) <= 255:
            valid = False
            messages.append({"type":"alert","content":"Last name has to be a shorter than 256 characters.","identifier":"last_name"})
        if not len(self.last_name) >= 1:
            valid = False
            messages.append({"type":"alert","content":"Last name has to be at least 1 character.","identifier":"last_name"})

        if not isinstance(self.organization_id, int):
            valid = False
            messages.append({"type":"alert","content":"Organization id has to be a integer.","identifier":"organization_id"})
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
    user_id = models.ForeignKey(User, to_field='user_id')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    message_id = models.PositiveIntegerField()

    def serialize(self):
        jsondict = {
            'content': self.content,
            'version': self.version,
            'userId': self.user_id,
            'created': self.created,
            'modified': self.modified,
            'messageId': self.message_id
        }

        return jsondict


class Answer(AbstractMessage):
    '''

    '''
    question_id = models.PositiveIntegerField() #this is the message_id of the question this answer is response to
    accepted = models.BooleanField(default=False)

    def serialize(self):
        jsondict = super(Answer, self).serialize()
        jsondict['questionId'] = self.question_id
        jsondict['accepted'] = self.accepted

        return jsondict


class Question(AbstractMessage):
    '''

    '''
    topic = models.CharField(max_length=250)
    def serialize(self):
        jsondict = super(Question, self).serialize()
        jsondict['topic'] = self.topic
        return jsondict

class Comment(AbstractMessage):
    '''

    '''
    parent_id = models.PositiveIntegerField() #this is the message_id of the message to which this comment is for
    def serialize(self):
        jsondict = super(Comment, self).serialize()
        jsondict['parentId'] = self.parent_id
        return jsondict


'''
class Tag(models.Model):

    ####
    This is the tag model for questions. Each Question may have 0-5 tags.
    Courses are also tags, but for those, the course_flag is set to True.

    created: Date when the object was created
    creator: ForeignKey, The user who created the tag
    customer: ForeignKey to the corresponding customer
    name: String, name of the topic, for example "Integrating"
    follow_counter: Integer, counter that easily expresses the number of followers in the tag
    question_counter: Integer, counter that easily expresses the number of questions in this category
    course_flag: Boolean, this is set to True if the tag represents a course, otherwise it is False

    ToDo: Tags are customer-specific. How can we make a distinction between the tags of different customers? ForeignKey or separate table?
    ####

    created = models.DateField(auto_now_add=True)
    last_use = models.DateField(auto_now=True)
    creator = models.ForeignKey('User')
    customer = models.ForeignKey(Customer, to_field="")

    name = models.CharField(max_length=30)
    follow_counter = models.IntegerField()
    question_counter = models.IntegerField()
    course_flag = models.BooleanField(default=False)

'''


class Vote(models.Model):

    rate = models.SmallIntegerField(default=0)
    user_id = models.ForeignKey(User, to_field="user_id")
    message_id = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def serialize(self):
        jsondict = {
            'rate': self.rate,
            'userId': self.user_id,
            'messageId': self.message_id,
            'created': self.created,
            'modified': self.modified
        }

        return jsondict

class Tag(models.Model):

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    creator = models.ForeignKey(User)
    organization_id = models.ForeignKey(Organization)

    name = models.CharField(max_length=30)
    follow_counter = models.IntegerField()
    question_counter = models.IntegerField()
    course_flag = models.BooleanField(default=False)

    def serialize(self):
        jsondict = {
            'creator': self.creator,
            'userId': self.user_id,
            'messageId': self.message_id,
            'created': self.created,
            'modified': self.modified,
            'organizationId': self.organization_id,
            'followCounter': self.follow_counter,
            'questionCounter': self.question_counter,
            'courseFlag': self.course_flag
        }

        return jsondict

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
