from django.urls import path
from .views import upload_and_list_files

urlpatterns = [
    path('upload_and_list.html/', upload_and_list_files, name='upload_and_list_files'),
]
