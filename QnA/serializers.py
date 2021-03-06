from django.contrib.contenttypes.models import ContentType

from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework import exceptions as exc

from QnA.models import User, Organization, Vote, Message, \
                       Question, Answer, Comment, Keyword, Tag, \
                       Course, Category


class OrganizationSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('rid', 'name', 'address')
        read_only_fields = ('rid',)


class OrganizationSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('name', 'address')


class UserSerializerGET(serializers.ModelSerializer):

    organization = OrganizationSerializerGET()

    class Meta:
        model = User
        fields = ('rid', 'username', 'first_name', 'last_name', 'organization')
        read_only_fields = ('rid',)
        write_only_fields = ('password',)


class UserSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'organization',
                  'email', 'first_name', 'last_name')
        write_only_fields = ('password',)


class MessageSerializerGET(serializers.ModelSerializer):

    user = UserSerializerGET()

    class Meta:
        model = Message
        fields = ('content', 'version', 'user', 'created', 'modified')


class AbstractMessageGETSingle(serializers.ModelSerializer):

    user_vote = serializers.SerializerMethodField('get_user_vote')

    def get_user_vote(self, obj):
        head_type = ContentType.objects.get_for_model(obj)

        if self.context.get('user', None):
            try:
                vote = Vote.objects.get(head_id=obj.pk,
                                        head_type=head_type,
                                        user=self.context['user'])
                return vote.direction
            except: return 0
        return None


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'description')


class KeywordSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)

    class Meta:
        model = Keyword
        fields = ('content', 'categories')


class TagSerializerGET(serializers.ModelSerializer):

    keyword = KeywordSerializer()

    class Meta:
        model = Tag
        fields = ('keyword', 'created')


class CourseSerializerPOST(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        categories = kwargs["data"].get('categories', None)
        category_objects = []

        try:
            kwargs["data"]["organization"] = kwargs["context"]["user"].organization.pk
        except:
            pass

        try:
            kwargs["data"]["moderators"] = [kwargs["context"]["user"].pk]
        except:
            pass

        if kwargs.get("context") and kwargs["context"].get('user', None) and categories:
            for category in categories:
                try:
                    category_objects.append(
                        Category.objects.get(title = category).pk
                        )
                except:
                    raise exc.ParseError("Course could not be created.")
        print "objektit:", category_objects
        kwargs["data"]['categories'] = category_objects

        super(CourseSerializerPOST, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = ('name', 'code', 'categories', 'organization', 'moderators')


class CourseSerializerGET(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    organization = OrganizationSerializerGET()
    moderators = UserSerializerGET(many=True)

    class Meta:
        model = Course
        fields = ('name', 'code', 'categories', 'organization', 'moderators')


class CommentSerializerGET(AbstractMessageGETSingle):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Comment
        fields = ('rid', 'message', 'user', 'votes_up',
                  'votes_down', 'created', 'user_vote')
        read_only_fields = ('rid',)


class AnswerSerializerGET(AbstractMessageGETSingle):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    comments = CommentSerializerGET(many=True)
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Answer
        fields = ('rid', 'message', 'user', 'created',
                  'votes_up', 'votes_down', 'user_vote', 'comments')
        read_only_fields = ('rid',)


class QuestionSerializerGETSingle(AbstractMessageGETSingle):

    message = MessageSerializerGET()
    answers = AnswerSerializerGET(many=True)
    comments = CommentSerializerGET(many=True)
    tags = TagSerializerGET(many=True)
    slug = serializers.Field(source='slug')
    user = UserSerializerGET()
    comment_amount = serializers.Field(source='comment_amount')
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'slug', 'user', 'votes_up',
                  'votes_down', 'message', 'created', 'modified',
                  'comment_amount', 'tags', 'comments', 'answers', 'user_vote')
        read_only_fields = ('rid', 'created')


class QuestionSerializerGETMany(serializers.ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    tags = TagSerializerGET(many=True)
    slug = serializers.Field(source='slug')
    comment_amount = serializers.Field(source='comment_amount')
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')
    answer_amount = serializers.SerializerMethodField('get_answer_amount')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'slug', 'user', 'created',
                  'modified', 'message', 'comment_amount',
                  'tags', 'votes_up', 'votes_down', 'answer_amount')
        read_only_fields = ('rid', 'created')

    def get_answer_amount(self, obj):
        return obj.answers.count()


### POST (ABSTRACT MESSAGE) QUESTION/COMMENT/ANSWER ###

class MessageSerializerPOSTAbstract(serializers.ModelSerializer):

    #! Define head in sub class

    class Meta:
        model = Message
        fields = ('content', 'user', 'head')


### POST QUESTION ###

class QuestionSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('title', 'user')


class MessageSerializerPOSTQuestion(MessageSerializerPOSTAbstract):

    head = QuestionSerializerPOST()


### POST ANSWER ###

class AnswerSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('user', 'question')

class MessageSerializerPOSTAnswer(MessageSerializerPOSTAbstract):

    head = AnswerSerializerPOST()


### POST COMMENT ###

class CommentToAbstractMessageSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'head_id', 'head_type')

class MessageSerializerPOSTComment(MessageSerializerPOSTAbstract):

    head = CommentToAbstractMessageSerializerPOST()


### POST VOTE ###

class VoteSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'direction', 'head_id', 'head_type')

    def validate(self, attrs):
        if attrs.get('direction', None) not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs
