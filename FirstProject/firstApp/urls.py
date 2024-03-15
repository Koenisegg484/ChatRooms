from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.home, name = "home"),
    path('room/', views.room, name = "room"),
    path('room/<str:pk>/', views.particularRooms, name = "partRoom"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('login/', views.user_login_register, name="login_registration"),
    path('logout/', views.logoutuser, name="logout-user"),
    path('register/', views.register_user, name="register-user")
]


# handler404 =
# handler500 =