from . import views
from .views import chartPie, chartBar
from django.urls import path
from django.conf.urls import handler404

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('fileupload', views.fileupload, name='fileupload'),
    path('register', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    
    path("simulation", views.simulation, name="simulation"),
    path("deletedata/<str:user_id>/<str:check_path>", views.delete1, name="delete"),
    path("deleteall/<str:check_path>", views.delete_all, name="delete_all"),
    path('users/', views.users, name='users'),
    path('users/delete/<int:id>', views.user_delete, name='user_delete'),
    path('change_password/', views.changePassword, name='change_password'),

    # API
    path('api/chart-pie/', chartPie.as_view(), name='api_chart_pie'),
    path('api/chart-bar/', chartBar.as_view(), name='api_chart_bar'),
]
handler404 = views.custom_404