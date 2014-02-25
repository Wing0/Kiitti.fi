from rest_framework.serializers import ModelSerializer, ValidationError, Field
from QnA.models import User, Organization, Vote, Question


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
        fields = ('rid', 'first_name', 'last_name', 'organization')


class UserSerializerPOST(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'organization',
                  'email', 'first_name', 'last_name')


class VoteSerializerPOST(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'rid', 'direction')

    def validate(self, attrs):

        # TODO: check that there is a message that can be voted

        if attrs['direction'] not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs


class QuestionSerializerGETSingle(ModelSerializer):

    # TODO ...

    message = Field()

    class Meta:
        model = Question
        fields = ('title', 'created',)


class QuestionSerializerGETMany(ModelSerializer):

    # TODO ...

    message = Field()

    class Meta:
        model = Question
        fields = ('title', )
