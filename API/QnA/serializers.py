from rest_framework.serializers import ModelSerializer, ValidationError, Field, RelatedField
from QnA.models import User, Organization, Vote, Message, \
                       Question, Answer, Comment, Keyword, Tag


class OrganizationSerializerGET(ModelSerializer):

    class Meta:
        model = Organization
        fields = ('rid', 'name', 'address')


class OrganizationSerializerPOST(ModelSerializer):

    class Meta:
        model = Organization
        fields = ('name', 'address')


class UserSerializerGET(ModelSerializer):

    organization = OrganizationSerializerGET()

    class Meta:
        model = User
        fields = ('rid', 'username', 'first_name', 'last_name', 'organization')
        read_only_fields = ('rid',)
        write_only_fields = ('password',)


class UserSerializerPOST(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'organization',
                  'email', 'first_name', 'last_name')
        write_only_fields = ('password',)


class VoteSerializerPOST(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'direction')

    def validate(self, attrs):

        # TODO: check that there is a message that can be voted

        if attrs['direction'] not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs


class MessageSerializerGET(ModelSerializer):

    class Meta:
        model = Message
        fields = ('content', 'version', 'user', 'created', 'modified')


class MessageSerializerPOSTAbstract(ModelSerializer):

    class Meta:
        model = Message
        fields = ('content', 'user', 'head')


class KeywordSerializer(ModelSerializer):

    class Meta:
        model = Keyword
        fields = ('content', 'category')


class TagSerializerGet(ModelSerializer):

    keyword = KeywordSerializer()

    class Meta:
        model = Tag
        fields = ('keyword', 'created')


class AnswerSerializerGET(ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    votes_up = Field(source='votes_up')
    votes_down = Field(source='votes_down')

    class Meta:
        model = Answer
        fields = ('rid', 'message', 'user')


class CommentSerializerGET(ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    votes_up = Field(source='votes_up')
    votes_down = Field(source='votes_down')

    class Meta:
        model = Comment
        fields = ('rid', 'message', 'user')


class QuestionSerializerGETSingle(ModelSerializer):

    message = MessageSerializerGET()
    answers = AnswerSerializerGET(many=True)
    comments = CommentSerializerGET(many=True)
    tags = TagSerializerGet(many=True)
    votes_up = Field(source='votes_up')
    votes_down = Field(source='votes_down')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'message', 'created',
                  'modified', 'answers', 'comments', 'tags',
                  'votes_up', 'votes_down')


class QuestionSerializerGETMany(ModelSerializer):

    user = UserSerializerGET()
    message = MessageSerializerGET()
    tags = TagSerializerGet(many=True)
    votes_up = Field(source='votes_up')
    votes_down = Field(source='votes_down')

    class Meta:
        model = Question
        fields = ('rid', 'title', 'message', 'user', 'created',
                  'modified', 'tags', 'votes_up', 'votes_down')


class QuestionSerializerPOST(ModelSerializer):

    class Meta:
        model = Question
        fields = ('title', 'user')


class MessageSerializerPOSTQuestion(MessageSerializerPOSTAbstract):

    head = QuestionSerializerPOST()
