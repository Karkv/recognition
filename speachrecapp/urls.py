# from django.contrib import admin
from django.urls import path,include
# from django.conf import settings
# from django.conf.urls.static import static
# from  .views import *
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',include('speachrecapp.urls'))
    path('speachrec/',views.index),
    path('Getdata/',views.getData),
    path('post/',views.postData),
    path('face',views.detect_face),
]