from rest_framework import generics
from team_members.models import TeamMember
from team_members.serializers import TemaMemberSerializer


class TemaMemberListView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all existing team members.
    post:
    Creates a team member
    """
    queryset = TeamMember.objects.all()
    serializer_class = TemaMemberSerializer


class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns single team member with given id
    put:
    Updates a team member
    patch:
    Updates a team member with partial data
    delete:
    removes a team member
    """
    queryset = TeamMember.objects.all()
    serializer_class = TemaMemberSerializer
