
from django.contrib.admin import AdminSite

from apps.models import Category


class OperatorAdminSite(AdminSite):
    site_header = "OPERATORS"
    site_title = "OPERATORS Portal"
    index_title = "Welcome to OPERATORS Researcher Events Portal"

operator_admin_site = OperatorAdminSite(name='operator_admin')
operator_admin_site.register(Category)
