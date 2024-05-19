from . import views
from .views import chartPie, chartBar, FileUpload, SimulationAPI
from django.urls import path
from django.conf.urls import handler404

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('fileupload/', views.fileupload, name='fileupload'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    
    path("simulation/", views.simulation, name="simulation"),
    path('database/', views.database, name='database'),
    path("delete/<str:user_id>/", views.delete1, name="delete"),
    path("deleteall/", views.delete_all, name="delete_all"),
    path("save-file/", views.save_file, name="save_file"),
    path('users/', views.users, name='users'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
    path('change_password/', views.changePassword, name='change_password'),

    # API
    path('api/chart-pie/', chartPie.as_view(), name='api_chart_pie'),
    path('api/chart-bar/', chartBar.as_view(), name='api_chart_bar'),
    path('api/fileupload/', FileUpload.as_view(), name='api_fileupload'),
    path('api/simulation-api/', SimulationAPI.as_view(), name='api_simulation_api'),
    # path('api/data/', getData.as_view(), name='api_data'),
    # path('api/number/', getNumber.as_view(), name='api_number'),
]
handler404 = views.custom_404