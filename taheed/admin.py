# admin.py
from typing import Any
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.urls import path
from .views import custom_admin_dashboard

class CustomAdminSite(admin.AdminSite):
    site_header = 'My Custom Admin'
    site_title = 'Admin Portal'
    index_title = 'Welcome to the Custom Admin Dashboard'

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('', self.admin_view(custom_admin_dashboard))
    #     ]
    #     return custom_urls + urls
    
    
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }
        print("app_list >> ", app_list)

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )

admin_site = CustomAdminSite(name='custom_admin')
