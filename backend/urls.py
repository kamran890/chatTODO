from django.contrib import admin
from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from backend.app.adapters import (
    auth,
    task,
)

admin.site.site_header = "ChatTODO Admin Panel"
admin.site.site_title = "ChatTODO Admin Panel"
admin.site.index_title = "ChatTODO Admin Panel"


schema_view = get_schema_view(
   openapi.Info(
      title="ChatTODO REST API",
      default_version='v1.0.0',
      description="ChatTODO REST API",
   ),
)


urlpatterns = [
    path(r'admin/', admin.site.urls, name="admin"),
    path(r'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='docs'
    ),
    path(
        'api/v1/signup/',
        auth.SignupView.as_view(),
        name='signup'
    ),
    path(
        'api/v1/login/',
        auth.DecoratedTokenObtainPairView.as_view(),
        name='login'
    ),
    path(
        'api/v1/logout/',
        auth.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'api/v1/chat/',
        task.TaskManagementView.as_view(),
        name='task_management'
    ),

]
