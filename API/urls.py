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

from user.views import UserViewset
from project.views import ProjectAdminViewset, ProjectViewset, ContributorViewset, IssueViewset, CommentViewset


# création d'un routeur
router = routers.SimpleRouter()
router.register('user', UserViewset, basename='user')
router.register('project', ProjectViewset, basename='project')
router.register('project_admin', ProjectAdminViewset, basename='project_admin')
router.register('issue', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')
router.register('contributor', ContributorViewset, basename='contributor')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
