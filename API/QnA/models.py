from django.db import models

class Customer(models.Model):
    '''
    Each customer has one unique Customer object. So far, this is only a dummy model.

    ToDo: Complete the Customer model attributes.
    '''
    customer_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)

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

class Question(models.Model):
    '''
    This is the question model. Question is very similiar to Answer, but it also has heading but no votes.


    '''

    created = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)
    customer = models.ForeignKey(Customer)

    author = models.ForeignKey('User')
    heading = models.CharField(max_length=150)
    content = models.TextField()
    #topic
    #tags

    view_counter = models.IntegerField()
    #history = models.TextField()


class Answer(models.Model):
    '''
    This is the answer model.


    '''
    answer_id = models.PositiveIntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)
    parent = models.ForeignKey(Question)

    author = models.ForeignKey('User')
    content = models.TextField()
    votes = models.IntegerField()
    correct = models.BooleanField(default=False)

    #history = models.TextField()


class Organization(models.Model):

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    image = models.ImageField()

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


# dummy
class User(models.Model):

    user_id = models.PositiveIntegerField(unique=True)
    username = models.CharField(max_length=255)
    reputation = models.IntegerField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    organization_id = models.ForeignKey(Organization)

    def serialize(self):
        jsondict = {
            'username': self.username,
            'user_id': self.user_id,
            'reputation': self.reputation,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'created': self.created,
            'modified': self.modified,
            'organization_id': organization_id
        }

        return jsondict


class Vote(models.Model):

    type = models.SmallIntegerField(default=0)
    user_id = models.ForeignKey(User)
    message_id = models.ForeignKey(User)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def serialize(self):
        jsondict = {
            'type': self.type,
            'user_id': self.user_id,
            'message_id': self.message_id,
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
            'user_id': self.user_id,
            'message_id': self.message_id,
            'created': self.created,
            'modified': self.modified,
            'organization_id': self.organization_id,
            'follow_counter': self.follow_counter,
            'question_counter': self.question_counter,
            'course_flag': self.course_flag
        }

        return jsondict

class Comment(models.Model):
    '''
    This is the comment model.


    '''

    created = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)
    parent_question = models.ForeignKey(Question, blank=True)
    parent_answer = models.ForeignKey(Answer, to_field="answer_id")

    author = models.ForeignKey(User, to_field="user_id")
    content = models.TextField()

    #history = models.TextField()

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
