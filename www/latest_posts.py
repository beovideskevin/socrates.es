from www.models import Post

def get_latest(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    return {'latest_posts': posts[:5]} 