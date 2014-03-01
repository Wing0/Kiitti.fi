from rest_framework.serializers import ValidationError
from rest_framework import serializers
from QnA.models import User, Organization, Vote, Message, \
                       Question, Answer, Comment, Keyword, Tag


class OrganizationSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('rid', 'name', 'address')


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

    class Meta:
        model = Message
        fields = ('content', 'version', 'user', 'created', 'modified')


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = ('content', 'category')


class TagSerializerGet(serializers.ModelSerializer):

    keyword = KeywordSerializer()

    class Meta:
        model = Tag
        fields = ('keyword', 'created')


class AnswerSerializerGET(serializers.ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Answer
        fields = ('rid', 'message', 'user')


class CommentSerializerGET(serializers.ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Comment
        fields = ('rid', 'message', 'user')


class QuestionSerializerGETSingle(serializers.ModelSerializer):

    message = MessageSerializerGET()
    answers = AnswerSerializerGET(many=True)
    comments = CommentSerializerGET(many=True)
    tags = TagSerializerGet(many=True)
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'message', 'created',
                  'modified', 'answers', 'comments', 'tags',
                  'votes_up', 'votes_down')


class QuestionSerializerGETMany(serializers.ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    tags = TagSerializerGet(many=True)
    votes_up = serializers.Field(source='votes_up')
    votes_down = serializers.Field(source='votes_down')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'message', 'user', 'created',
                  'modified', 'tags', 'votes_up', 'votes_down')


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


### POST COMMENT ###

class CommentToQuestionSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'head_id', 'head_type')

class MessageSerializerPOSTComment(MessageSerializerPOSTAbstract):

    head = CommentToQuestionSerializerPOST()


### POST VOTE ###

class VoteSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'direction', 'head_id', 'head_type')

    def validate(self, attrs):
        if attrs.get('direction', None) not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs
