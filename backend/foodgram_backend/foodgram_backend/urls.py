from api.views.recipes import redirect_short_link
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        's/<str:short_code>/',
        redirect_short_link,
        name='redirect_short_link',
    ),
]
