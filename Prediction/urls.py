from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('predict/', views.upload_file, name='predict'),
    path('download/', views.file_download, name='download_file'),
    path('McgmCategory/', TemplateView.as_view(template_name='Prediction/mcgm_categories.html'), name='McgmCategory'),
    path('SpeakupCategory/', TemplateView.as_view(template_name='Prediction/speakup_categories.html'),
         name='SpeakupCategory'),
    path('predict/checkOutput/', views.handle_user_selected_data, name='checkOutput'),

]
