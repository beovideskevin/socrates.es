from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.html import escape, strip_tags
from django.db.models import Q
from www.models import Tag, Category, Post, Comment, Subscriber, Video
from www.helpers import *
import random
import json
import logging
logger = logging.getLogger(__name__)

def art(request):
    arteCat = Category.objects.get(name="arte")
    posts = Post.objects.filter(category=arteCat).order_by('-created_at')

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

    return render(request, "art.html", {
        "posts": posts,
        "active": "art",
        "prevPage": page - 1 if page > 1 else None,
        "nextPage": page + 1 if page < paginator.num_pages else None,
        "activePage": page if page else 1,
        "pageRange": range(1, paginator.num_pages + 1)
    })

# Create your views here.
def blog(request):
    diarioCat = Category.objects.get(name="diario")
    artCat = Category.objects.get(name="arte")
    posts = Post.objects.filter(Q(category=diarioCat) | Q(category=artCat)).order_by('-created_at')

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
            "active": "",
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
            "active": "",
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
        logger.error(f"Post: post with slug {slug} does not exist.")
        return render(request, "404.html")

    comments = Comment.objects.filter(post_id=post.id, approved=True)
    
    if request.method == "POST":
        secret = settings.TURNSTILE_SECRET
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = strip_tags(escape(request.POST["name"]))
        message = strip_tags(escape(request.POST["message"]))
        nothing = strip_tags(escape(request.POST["nothing"]))
        sent = False
        error = False

        if (name == "" or message == "" or turnstile_response == '' or nothing != "" 
                or validate_turnstile(secret, turnstile_response, remote_ip) is False):
            error = True
            url = reverse(f"post", kwargs={"slug": slug}) + f"?name={name}&message={message}&error={error}&sent={sent}"
            return redirect(url)

        Comment.objects.create(name=name, content=message, post=post)

        send_mail(
            "Comentario de Socrates.es",
            f"{message}\nNombre: {name}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )

        sent = True
        url = reverse(f"post", kwargs={"slug": slug}) + f"?sent={sent}"
        return redirect(url)

    name = request.GET.get('name', "") 
    message = request.GET.get('message', "")
    sent = request.GET.get('sent', False)
    error = request.GET.get('error', False)
    
    return render(request, "post.html", {
        "post": post,
        "active": None,
        "error": error,
        "name": name,
        "message": message,
        "comments": comments,
        "sent": sent
    })

def like(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        logger.error(f"Like: post with slug {slug} does not exist.")
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
        logger.error(f"Facebook: post with slug {slug} does not exist.")
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
        logger.error(f"Twitter: post with slug {slug} does not exist.")
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
    if request.method == "POST":
        secret = settings.TURNSTILE_SECRET
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = strip_tags(escape(request.POST["name"]))
        email = strip_tags(escape(request.POST["email"]))
        message = strip_tags(escape(request.POST["message"]))
        nothing = strip_tags(escape(request.POST["nothing"]))
        sent = False
        error = False

        if (name == "" or email == "" or is_valid_email(email) is False or message == "" or nothing != ""
                or turnstile_response == '' or validate_turnstile(secret, turnstile_response, remote_ip) is False):
            error = True
            url = reverse('contact') + f"?name={name}&email={email}&message={message}&error={error}&sent={sent}"
            return redirect(url)

        send_mail(
            "Mensaje de Socrates.es",
            f"{message}\nNombre: {name}\nCorreo: {email}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )
        
        sent = True
        url = reverse('contact') + f"?sent={sent}"
        return redirect(url)

    name = request.GET.get('name', "") 
    message = request.GET.get('message', "")
    email = request.GET.get('email', "")
    sent = request.GET.get('sent', False)
    error = request.GET.get('error', False)
    
    return render(request, "contact.html", {
        "active": "contact",
        "error": error,
        "name": name,
        "email": email,
        "message": message,
        "sent": sent
    })

def ar(request):
    return render(request, "ar.html")

def aart(request):
    return render(request, "aart.html")

def api(request, tag=None):
    try:
        videos = Video.objects.all() if not tag else Video.objects.filter(tags__in=[Tag.objects.get(name=tag)])
    except Tag.DoesNotExist:
        logger.error(f"Video: video with tag {tag} does not exist.")
        return JsonResponse({"error": "Tag is not valid"}, status=400)

    videoJson = [
        {
            "philosopher": vid.philosopher,
            "url": vid.url,
            "poster": vid.poster,
            "quote": vid.quote,
            "width": vid.width,
            "height": vid.height,
            "mask": vid.mask
        }
        for vid in videos
    ]

    if tag is None:
        random.shuffle(videoJson)

    return JsonResponse({"success": videoJson}, status=200)
