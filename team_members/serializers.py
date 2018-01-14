from rest_framework import serializers
from team_members.models import TeamMember


class TemaMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = (
          'id', 'first_name', 'last_name', 'email',
          'phone_number', 'role'
        )
