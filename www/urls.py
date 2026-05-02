from django.urls import path

from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("arte", views.art, name="arte"),
    path("buscar", views.search, name="buscar"),
    path("etiqueta", views.tag, name="etiqueta"),
    path("tesis", views.thesis, name="tesis"),
    path("post/<str:slug>", views.post, name="post"),
    path("post/<str:slug>/like", views.like, name="like"),
    path("post/<str:slug>/facebook", views.facebook, name="facebook"),
    path("post/<str:slug>/twitter", views.twitter, name="twitter"),
    path("acerca", views.about, name="acerca"),
    path("contacto", views.contact, name="contacto"),
    path("subscribirse", views.subscribe, name="subscribirse"),
    path("ar", views.ar, name="ar"),
    path("ar/<str:slug>", views.ar, name="ar"),
    path("aart", views.aart, name="aart"),
    path("api", views.api, name="api"),
    path("api/<str:slug>", views.api, name="api"),
]