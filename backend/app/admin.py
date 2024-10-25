from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from backend.tenant.utils import is_public_schema
from backend.app.models import Task


@admin.register(Task)
class TaskAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')

    def has_module_permission(self,request, view=None):
        return not is_public_schema(request=request)
