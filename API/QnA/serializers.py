from rest_framework.serializers import ModelSerializer, ValidationError
from QnA.models import Organization, Vote


class OrganizationSerializerGET(ModelSerializer):

    class Meta:
        model = Organization
        fields = ('organization_id', 'name', 'address')


class OrganizationSerializerPOST(ModelSerializer):

    class Meta:
        model = Organization
        fields = ('name', 'address')


class VoteSerializerPOST(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'message_id', 'direction')

    def validate(self, attrs):

        # TODO: check that there is a message that can be voted

        if attrs['direction'] not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs
