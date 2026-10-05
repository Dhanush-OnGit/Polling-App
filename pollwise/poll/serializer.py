from rest_framework import serializers
from poll.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email","username","password","phone","id"]
        read_only_fields = ["id"]
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    voters = serializers.SerializerMethodField()
    class Meta:
        model = Choice
        fields = "__all__"
        read_only_fields = ["id", "poll_object"]

    def get_votes(Self,object):
        vote_qs = vote.objects.filter(choice_object=object)
        return vote_qs.count()
    def get_voters(self,object):
        voters_qs = vote.objects.filter(choice_object=object)
        return voters_qs.values_list("owner_object__username",flat=True)

class PollSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only = True)
    choices = serializers.SerializerMethodField()
    total_vote = serializers.SerializerMethodField()
    class Meta:
        model = poll
        fields = "__all__"
        read_only_fields = ["owner","created_at","is_active"]

    def get_choices(self,object):
        choice_qs = Choice.objects.filter(poll_object = object)
        serializer_instance = ChoiceSerializer(choice_qs,many = True)
        return serializer_instance.data

    def get_total_vote(self,object):
        vote_qs = vote.objects.filter(poll_object=object)
        return vote_qs.count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = vote
        fields = "__all__"
        read_only_fields = ["id","poll_object","owner_object","created_at"]
