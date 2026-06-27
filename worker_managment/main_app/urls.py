from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('workers/', views.workers, name='workers'),
    path('tasks/', views.tasks, name='tasks'),
    path('reports/', views.reports, name='reports'),
    path('worker-entry/', views.worker_entry, name='worker_entry'),
    path('find/', views.find_worker, name='find_worker'),
    path('worker/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    path('worker/<int:worker_id>/edit/', views.worker_edit, name='worker_edit'),
    path('worker/<int:worker_id>/delete/', views.worker_delete, name='worker_delete'),
    path('case-manager/', views.case_manager, name='case_manager'),
    path('salary-increment/', views.salary_increment, name='salary_increment'),
]