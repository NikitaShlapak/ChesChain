from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("<str:room_name>/", views.room, name="room"),
    path("board/<str:board_name>", views.board, name="board"),
    path('logout', views.logout, name='logout'),
]