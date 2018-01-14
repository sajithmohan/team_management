from team_members.views import TemaMemberListView, TeamMemberDetailView
from django.urls import re_path


urlpatterns = [
      re_path(r'^$', TemaMemberListView.as_view()),
      re_path(r'^(?P<pk>\d+)/$', TeamMemberDetailView.as_view())
]
