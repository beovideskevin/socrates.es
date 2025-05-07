from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from www.models import Tag, Category, Post, Comment, Subscriber
from www.helpers import *

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def blog(request):
    posts = Post.objects.all().order_by('created_at') # -created_at

    page = request.GET.get('page')
    if page is None or page == "":
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1

    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog.html", {
        "posts": posts,
        "active": "blog",
        "prevPage": page - 1 if page > 1 else None,
        "nextPage": page + 1 if page < paginator.num_pages else None,
        "activePage": page if page else 1,
        "pageRange": range(1, paginator.num_pages + 1)
    })

def search(request):
    q = request.GET.get('search')
    if q is None or q == "":
        return render(request, "blog.html", {
            "posts": [],
            "active": "blog",
            "search": True,
            "words": "",
            "prevPage": 1,
            "nextPage": 1,
            "activePage": 1,
            "pageRange": range(1, 1)
        })
    words = [word.strip() for word in q.split("+") if word.strip()]
    if not words:
        return render(request, "blog.html", {
            "posts": [],
            "active": "blog",
            "search": True,
            "words": "",
            "prevPage": 1,
            "nextPage": 1,
            "activePage": 1,
            "pageRange": range(1, 1)
        })

    posts = Post.objects.filter(content__icontains=words[0]).order_by('-created_at')

    for word in words[1:]:
        posts = posts.filter(content__icontains=word)

    page = request.GET.get('page')
    if page is None or page == "":
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1

    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog.html", {
        "posts": posts,
        "active": "search",
        "search": True,
        "words": '+'.join(words),
        "prevPage": page - 1 if page > 1 else None,
        "nextPage": page + 1 if page < paginator.num_pages else None,
        "activePage": page if page else 1,
        "pageRange": range(1, paginator.num_pages + 1)
    })

def thesis(request):
    thesisCat = Category.objects.get(name="tesis")
    posts = Post.objects.filter(category=thesisCat).order_by('slug')

    page = request.GET.get('page')
    if page is None or page == "":
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1

    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "thesis.html", {
        "posts": posts,
        "active": "thesis",
        "prevPage": page - 1 if page > 1 else None,
        "nextPage": page + 1 if page < paginator.num_pages else None,
        "activePage": page if page else 1,
        "pageRange": range(1, paginator.num_pages + 1)
    })

def post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        logger.error(f"Post with slug {slug} does not exist.")
        return render(request, "404.html")

    comments = Comment.objects.filter(post_id=post.id, approved=True)
    sent = False

    if request.method == "POST":
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = request.POST["name"]
        message = request.POST["message"]
        nothing = request.POST["nothing"]

        if name == "" or message == "" or turnstile_response == '' or nothing != "":
            return render(request, "post.html", {
                "post": post,
                "active": None,
                "error": True,
                "name": name,
                "message": message,
                "comments": comments
            })

        if validate_turnstile(turnstile_response, remote_ip) is False:
            return render(request, "post.html", {
                "post": post,
                "active": None,
                "error": True,
                "name": name,
                "message": message,
                "comments": comments
            })

        sent = True
        send_mail(
            "Comentario de Socrates.es",
            f"{message}\nNombre: {name}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )

        Comment.objects.create(name=name, content=message, post=post)

    return render(request, "post.html", {
        "post": post,
        "active": None,
        "sent": sent,
        "comments": comments
    })

def like(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        logger.error(f"Post with slug {slug} does not exist.")
        data = {
            'message': 0,
            'status': 404
        }
        return JsonResponse(data)

    post.like += 1
    post.save()
    data = {
        'message': post.like,
        'status': 200
    }
    return JsonResponse(data)

def facebook(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        logger.error(f"Post with slug {slug} does not exist.")
        data = {
            'message': 0,
            'status': 404
        }
        return JsonResponse(data)

    post.facebook += 1
    post.save()
    data = {
        'message': post.facebook,
        'status': 200
    }
    return JsonResponse(data)

def twitter(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        logger.error(f"Post with slug {slug} does not exist.")
        data = {
            'message': 0,
            'status': 404
        }
        return JsonResponse(data)

    post.twitter += 1
    post.save()
    data = {
        'message': post.twitter,
        'status': 200
    }
    return JsonResponse(data)

def about(request):
    return render(request, "about.html", {
        "active": "about"
    })

def contact(request):
    sent = False
    if request.method == "POST":
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        nothing = request.POST["nothing"]

        if (name == "" or email == "" or is_valid_email(email) is False or message == ""
                or turnstile_response == '' or nothing != ""):
            return render(request, "contact.html", {
                "active": "contact",
                "error": True,
                "name": name,
                "email": email,
                "message": message
            })

        if validate_turnstile(turnstile_response, remote_ip) is False:
            return render(request, "contact.html", {
                "active": "contact",
                "error": True,
                "name": name,
                "email": email,
                "message": message
            })

        sent = True
        send_mail(
            "Mensaje de Socrates.es",
            f"{message}\nNombre: {name}\nCorreo: {email}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )

    return render(request, "contact.html", {
        "active": "contact",
        "sent": sent
    })

def ar(request):
    return render(request, "ar.html")

def aart(request):
    return render(request, "aart.html")
