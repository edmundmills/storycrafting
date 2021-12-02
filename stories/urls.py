from django.urls import path

from . import views

app_name = 'stories'
urlpatterns = [
    path('stories/new/', views.NewView.as_view(), name='new'),
    path('stories/<int:pk>/write/', views.WriteView.as_view(), name='write'),
    path('', views.IndexView.as_view(), name='index'),
]
