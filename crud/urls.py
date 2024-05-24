from . import views
from .views import *
from django.urls import path
from django.conf.urls import handler404

urlpatterns = [    
    path('', views.dashboard, name='dashboard'),
    path('export-report/', views.export_report, name='export_report'),
    path('fileupload/', views.fileupload, name='fileupload'),
    path("simulation/", views.simulation, name="simulation"),
    path('database/', views.database, name='database'),
    path("delete/<str:user_id>/", views.delete1, name="delete"),
    path("deleteall/", views.delete_all, name="delete_all"),
    path("save-file/", views.save_file, name="save_file"),

    path('users/', views.users, name='users'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),

    # account
    path('register/', RegisterView1.as_view(), name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('login/', LoginView1.as_view(), name='login'),
    path('logout/', LogoutView1.as_view(), name='logout'),
    path('change-password/', views.changePassword, name='change_password'),

    # API
    path('api/chart-pie/', chartPie.as_view(), name='api_chart_pie'),
    path('api/chart-bar/', chartBar.as_view(), name='api_chart_bar'),
    path('api/fileupload/', FileUpload.as_view(), name='api_fileupload'),
    path('api/simulation-api/', SimulationAPI.as_view(), name='api_simulation_api'),
    path('api/analysis-userID/', analysisUserID.as_view(), name='api_analysis_userID'),
    path('api/is-selected/', isSelected.as_view(), name='api_is_selected'),
    path('api/edit-userID/', editUserID.as_view(), name='api_edit_userID'),
    path('api/get-data/', getData.as_view(), name='api_get_data'),
    # path('api/data/', getData.as_view(), name='api_data'),
    # path('api/number/', getNumber.as_view(), name='api_number'),
]
handler404 = views.custom_404