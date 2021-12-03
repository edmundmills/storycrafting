from django.urls import path

from . import views

app_name = 'stories'
urlpatterns = [
    path('stories/new/', views.NewView.as_view(), name='new'),
    path('stories/<int:pk>/write/', views.WriteView.as_view(), name='write'),
    path('proposals/<int:pk>/prompt/', views.prompt, name='prompt'),
    path('proposals/<int:pk>/accept_proposal/', views.accept_proposal, name='accept_proposal'),
    path('proposals/<int:pk>/reject_proposal/', views.reject_proposal, name='reject_proposal'),
    path('proposals/<int:pk>/add_thought/', views.add_thought, name='add_thought'),
    path('thoughts/<int:pk>/delete_thought/', views.delete_thought, name='delete_thought'),
    path('', views.IndexView.as_view(), name='index'),
]
