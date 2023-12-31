"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from rest_framework_nested import routers

from user.views import UserViewSet
from project.views import ProjectViewSet, IssueViewSet, CommentViewSet


# création d'un routeur
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet,  basename='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'issues', IssueViewSet, basename='issues')
# génère :
# /projects/{project_pk}/issues/
# /projects/{project_pk}/issues/{pk}/

# project_router.register(r'contributors', ContributorViewSet, basename='contributors')
# génère :
# /projects/{project_pk}/contributors/
# /projects/{project_pk}/contributors/{pk}/

issues_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='comments')
# génère :
# /projects/{project_pk}/issues/{issue_pk}/comments/
# /projects/{project_pk}/issues/{issue_pk}/comments/{pk}/


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/', include(router.urls)),
    path(r'api/', include(project_router.urls)),
    path(r'api/', include(issues_router.urls))
]
