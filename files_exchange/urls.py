from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_files, name='search_files'),
    path('<int:id_page>/', views.search_files, name='search_files'),
    # path('results/', views.result_files, name='result_files'),
    # path('results/<int:page>/', views.result_files, name='result_files'),
    path('moderation/', views.moderation_page, name='moderation_page'),
    path('upload/', views.upload_file, name='upload_file'),
    path('ajax/propose_school/', views.propose_school_name, name='propose_school'),
    path('<int:id_file>/<slug:title_file>/', views.one_file_page, name='one_file_page'),
    path('test_translate/', views.test_i18n, name='test_translate'),
]
