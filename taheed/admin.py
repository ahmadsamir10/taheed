# admin.py
from django.db.models import Q
from django.contrib import admin
from django.template.response import TemplateResponse
from users.models import Motorcycle, Client, User, Settings
from users.admin import UserAdmin, ClientAdmin, MotorcycleAdmin, SettingsAdmin

class CustomAdminSite(admin.AdminSite):
    site_header = 'My Custom Admin'
    site_title = 'Admin Portal'
    index_title = 'Welcome to the Custom Admin Dashboard'
    
    def get_statistics(self):
        statistics = {
            "registered_clients_count": 0,
            "clients_who_purchased_count": 0,
            "all_motorcycles_count": 0,
            "all_motorcyles_total_price": 0
        }
        try:
            motorcycles_information = Motorcycle.objects.first()
            registered_clients_count = Client.objects.filter(Q(steps="second") | Q(steps="completed")).count()
            clients_who_purchased_count = Client.objects.filter(steps="completed").count()
            statistics['registered_clients_count'] = registered_clients_count
            statistics['clients_who_purchased_count'] = clients_who_purchased_count
            all_motorcycles_count = motorcycles_information.available_motorcycles + motorcycles_information.soldout_motorcycles
            statistics['all_motorcycles_count'] = motorcycles_information.available_motorcycles + motorcycles_information.soldout_motorcycles
            statistics['all_motorcyles_total_price'] = motorcycles_information.motorcycle_price * all_motorcycles_count
            return statistics
        except:
            return statistics
    
    
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
            **self.get_statistics()
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )

admin_site = CustomAdminSite(name='تعهيد')


# Register models with the custom admin site
admin_site.register(Motorcycle, MotorcycleAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Settings, SettingsAdmin)
admin_site.register(Client, ClientAdmin)