from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('debug/', views.debug_info, name='debug_info'),
    path('leetcode-daily/', views.leetcode_daily, name='leetcode_daily'),
    path('leetcode-recent/', views.leetcode_recent, name='leetcode_recent'),
    path('leetcode-question/<str:question_slug>/', views.leetcode_question_detail, name='leetcode_question_detail'),
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/update/', views.todo_update, name='todo_update'),
    path('todos/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
]
