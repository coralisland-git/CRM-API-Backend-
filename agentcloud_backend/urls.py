"""agentcloud_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from general import views

admin.site.site_header = "AgentCloud CRM Administrator"

schema_view = get_swagger_view(title='AgentCloud Backend API')

router = routers.DefaultRouter()
router.register(r'calendar', views.CalendarViewSet, 'calendar')
router.register(r'circle', views.CircleViewSet, 'circle')
router.register(r'event', views.EventViewSet, 'event')
router.register(r'lead', views.LeadViewSet, 'lead')
router.register(r'task', views.TaskViewSet, 'task')
router.register(r'color', views.ColorViewSet, 'color')
router.register(r'user', views.UserViewSet, 'user')
router.register(r'interaction', views.InteractionViewSet, 'interaction')
router.register(r'productoption', views.ProductOptionViewSet, 'productoption')
router.register(r'leadrelation', views.LeadRelationViewSet, 'leadrelation')
router.register(r'template', views.TemplateViewSet, 'template')
router.register(r'leadfile', views.LeadFileViewSet, 'leadfile')
router.register(r'eventfile', views.EventFileViewSet, 'eventfile')
router.register(r'notification', views.NotificationViewSet, 'notification')
router.register(r'tag', views.TagViewSet, 'tag')
router.register(r'calendar_permission', views.CalendarPermissionViewSet, 'calendar_permission')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^$', schema_view),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
