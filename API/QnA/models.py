from django.db import models

class AbstractMessage(models.Model):
    '''
    This is the Abstract message class for all the message classes. The other message classes
    will inherit this class.
    '''
    content = models.TextField()
    version = models.PositiveIntegerField()
    user_id = models.ForeignKey(User, to_field='user_id')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField()
    message_id = models.PositiveIntegerField()

    def serialize(self):
        jsondict = {
            'content': self.content,
            'version': self.version,
            'user_id': self.user_id,
            'created': self.created,
            'modified': self.modified,
            'message_id': self.message_id
        }

        return jsondict


class Answer(AbstractMessage):
    '''

    '''
    question_id = models.PositiveIntegerField() #this is the message_id of the question this answer is response to

    def serialize(self):
        jsondict = super(Answer, self).serialize()
        jsondict['question_id'] = self.question_id
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
        jsondict['parent_id'] = self.parent_id
        return jsondict



class Topic(models.Model):
    '''
    This is the topic model for questions. Each Question belongs to one or more Topic.

    created: Date when the object was created
    customer: ForeignKey to the corresponding customer
    follow_counter: Integer, counter that easily expresses the number of followers in the topic
    question_counter: Integer, counter that easily expresses the number of questions in this category
    name: String, name of the topic, for example "Mathematics"

    ToDo: Topics are customer-specific. How can we make a distinction between the topics of different customers? ForeignKey or separate table?
    '''
    created = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, to_field='customer_id')

    name = models.CharField(max_length=30)
    follow_counter = models.IntegerField()
    question_counter = models.IntegerField()

class Tag(models.Model):
    '''
    This is the tag model for questions. Each Question may have 0-5 tags.
    Courses are also tags, but for those, the course_flag is set to True.

    created: Date when the object was created
    creator: ForeignKey, The user who created the tag
    customer: ForeignKey to the corresponding customer
    name: String, name of the topic, for example "Integrating"
    follow_counter: Integer, counter that easily expresses the number of followers in the tag
    question_counter: Integer, counter that easily expresses the number of questions in this category
    course_flag: Boolean, this is set to True if the tag represents a course, otherwise it's False

    ToDo: Tags are customer-specific. How can we make a distinction between the tags of different customers? ForeignKey or separate table?
    '''

    created = models.DateField(auto_now_add=True)
    last_use = models.DateField(auto_now=True)
    creator = models.ForeignKey('User')
    customer = models.ForeignKey(Customer, to_field="")

    name = models.CharField(max_length=30)
    follow_counter = models.IntegerField()
    question_counter = models.IntegerField()
    course_flag = models.BooleanField(default=False)

# dummy
class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=255)
    reputation = models.IntegerField()

    def serialize(self):
        jsondict = {
            'username': self.username,
            'user_id': self.user_id,
            'reputation': self.reputation
        }

        return jsondict
    '''
    def validate(self, jsondict):


    '''


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
