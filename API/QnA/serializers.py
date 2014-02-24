from rest_framework.serializers import ModelSerializer, ValidationError
from QnA.models import Vote


class VoteSerializerPOST(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('user', 'message_id', 'direction')

    def validate(self, attrs):

        # TODO: check that there is a message that can be voted

        if attrs['direction'] not in [1, -1]:
            raise ValidationError("Direction must be 1 or -1")
        return attrs
