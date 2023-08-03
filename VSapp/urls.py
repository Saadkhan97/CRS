from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('hadith_text/<str:pk>', views.hadith_text, name='hadith_text'),
    path('logout/', views.logoutp, name='logout'),
    path('download_pdf/<str:pk>',views.download_pdf,name='download_pdf'),
    path('books_admin/', views.books_admin, name='books_admin'),
    path('user_books/', views.user_books, name='user_books'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)