from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register/", views.register_user, name="regiter"),
    path("add_anime", views.add_anime, name="add_anime"),
    path("show_anime/<int:pk>", views.show_anime, name="show_anime"),
    path("add_comment/<int:pk>/comment", views.add_comment, name="add_comment"),
    path("post_link/<int:pk>", views.post_likes, name="post_likes"),
]
