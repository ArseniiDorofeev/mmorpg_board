from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mmorpg_board_app.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
