from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('wineapp/', include('wineapp.urls')),
    # Accounts: one-step registration plus login, logout and password change.
    # Password reset is deliberately not routed: the site sends no email, so
    # those views would only ever fail.
    path('accounts/register/',
         RegistrationView.as_view(success_url=reverse_lazy('wineapp:index')),
         name='registration_register'),
    path('accounts/register/closed/',
         TemplateView.as_view(template_name='registration/registration_closed.html'),
         name='registration_disallowed'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
