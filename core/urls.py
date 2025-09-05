from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leetcode-daily/', views.leetcode_daily, name='leetcode_daily'),
    path('leetcode-recent/', views.leetcode_recent, name='leetcode_recent'),
    path('leetcode-question/<str:question_slug>/', views.leetcode_question_detail, name='leetcode_question_detail'),
]
