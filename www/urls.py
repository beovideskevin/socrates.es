from django.urls import path

from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("search", views.search, name="search"),
    path("thesis", views.thesis, name="thesis"),
    path("post/<str:slug>", views.post, name="post"),
    path("post/<str:slug>/like", views.like, name="like"),
    path("post/<str:slug>/facebook", views.facebook, name="facebook"),
    path("post/<str:slug>/twitter", views.twitter, name="twitter"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("ar", views.ar, name="ar"),
    path("aart", views.aart, name="aart"),
]