from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from accounts.views import login_view, logout_view, registration_view, profile_settings, delete_view, contact_view

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('registration/', registration_view, name='registration_view'),
    path('settings/', profile_settings, name='profile_settings'),
    path('delete/', delete_view, name='delete_profile'),
    path('contact/', contact_view, name='contact_page'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)