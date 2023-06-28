from django.urls import path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from Service.views import SignageViewAPI, CommunityViewAPI, ContentViewAPI, commentMediaAPI, CommunityCommentAPI, IssueBoardAPI

router = routers.DefaultRouter()
# app_name = "Service"

urlpatterns = [
    # path 뒤 name이 템플릿에서 href url 경로를 지정해줄 이름이다.
    path('', views.Idle, name='Idle'),
    path('signage/', SignageViewAPI.as_view(), name='signage'),
    path('Content/', ContentViewAPI.as_view(), name='content'),
    path('contentDetailView/<int:id>', views.contentDetailView, name="contentDetailView"),
    path('ContentLike/<int:id>', views.ContentLike, name="ContentLike"),
    path('ContentHits/<int:id>', views.ContentHits, name="ContentHits"),

    path('community/', CommunityViewAPI.as_view(), name="community"),
    path('communityMedia/', commentMediaAPI.as_view(), name="communityMedia"),
    path('CommunityComment/', CommunityCommentAPI.as_view(), name="CommunityComment"),
    path('DailyBoard/', views.DailyBoard, name="DailyBoard"),
    path('IssueBoard/', IssueBoardAPI.as_view(), name="IssueBoard"),

    path('paint', views.paint, name='paint'),
    path('paintlist', views.paintlist, name='paintlist'),
    path('ViewPaint/<int:id>', views.ViewPaint, name="ViewPaint"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
