from django.urls import path
from . import views

urlpatterns = [
    path('', views.view, name='view'),
    path('user',views.user, name='user'),
    path('csv',views.csvdownload, name='csv'),
    path('agreement',views.agreement, name='agreement'),
    path('howto',views.howto, name='howto'),
    path('upload<int:mode>', views.upload, name='upload'),
    path('logintw', views.logintw, name='logintw'),
    path('back', views.back, name='back'),
]
