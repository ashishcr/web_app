from django.urls import path

from . import views

urlpatterns = [
    path('',views.upload_file,name = 'home'),
    path('plot_data/',views.plotly_plot,name='plot_data')
]