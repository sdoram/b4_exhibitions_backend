from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/accompanies/", include("accompanies.urls")),
    path("api/exhibitions/", include("exhibitions.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/users/", include("users.urls")),
    path("api/user/", include("allauth.urls")),
    path("api/user/", include("dj_rest_auth.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
