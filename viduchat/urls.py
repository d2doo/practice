from django.urls import path
from . import views
app_name = 'viduchat'
urlpatterns = [
    path('sessions/', views.initializeSession, name='initializeSession'),
    path('sessions/<sessionId>/connections/', views.createConnection, name='createConnection'),
]
