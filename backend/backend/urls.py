from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from subscription.urls import urlpatterns as subscription_urls
from discounts.urls import urlpatterns as discount_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('payment/', include('payment.urls')),
    path('subscriptions/', include('subscription.urls')),
    path('discounts/', include('discounts.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
