from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from dj_rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView,
)
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('auth/password-reset/', include('dj_rest_auth.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/password_reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('subscriptions/', include('subscription.urls')),
    path('discounts/', include('discounts.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
