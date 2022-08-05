from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("auction/<str:id>", views.auction, name="auction"),
    path("auction/<str:id>/watch", views.watch, name="watch"),
    path("auction/<str:id>/bid", views.bidding, name="newbid"),
    path("auction/<str:id>/close", views.close, name="close"),
    path("watchlist", views.WatchList, name="watchlist" ),
    path("categorylist", views.CategoryList, name="categorylist"),
    path("category/<str:catty>", views.category,name="categoryauctions"),
    path("auction/<str:id>/comment", views.Comment, name="newcomment")
]
