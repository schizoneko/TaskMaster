# name o path se lien quan den index.html, reference to the link in index.html
#{% url 'register' %} vi du o trong ''
from django.urls import path

from .import views

urlpatterns = [
    path('', views.home, name=''),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='my_login'),
    path('mypage/', views.mypage, name='mypage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_management, name='profile_management'),
    path('delete_account/', views.deleteAccount, name='delete_account'),
    path('logout/', views.user_logout, name='user_logout'),

    # Project URLs
    path('create_project/', views.createProject, name='create_project'),
    path('view_projects/', views.viewProjects, name='view_projects'),
    path('update_project/<int:pk>/', views.updateProject, name='update_project'),
    path('delete_project/<int:pk>/', views.deleteProject, name='delete_project'),

    # Task URLs
    path('create_task/<int:project_id>/', views.createTask, name='create_task'),
    path('view_tasks/<int:project_id>/', views.viewTasks, name='view_tasks'),
    
    path('update_task/<int:project_id>/<int:pk>/', views.updateTask, name='update_task'),
    path('delete_task/<int:project_id>/<int:pk>/', views.deleteTask, name='delete_task'),

    # View only
    path('user/<int:user_id>/dashboard/', views.view_user_dashboard, name='view_user_dashboard'),

    #Group chat
     path('project/<int:project_id>/chat/', views.project_chat, name='project_chat'),


    #AI
    #path('project/<int:project_id>/task/<int:task_id>/explain/', views.explain_task_content, name='explain_task_content'),
    path('explain_task_content/<int:project_id>/<int:task_id>/', views.explain_task_content, name='explain_task_content'),
]























