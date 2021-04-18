from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.create_new_listing, name="create_new_listing"),
    path("<int:id>", views.view_listing, name="listing"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("listings/<int:id>/watch", views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<int:id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
]
