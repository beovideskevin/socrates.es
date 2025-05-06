import locale
from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    abstract = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="post"
    )
    category = models.ManyToManyField(
        Category,
        blank=False,
        related_name="post"
    )
    content = models.TextField()
    poster = models.CharField(max_length=200, blank=True, null=True)
    like = models.IntegerField(default=0)
    facebook = models.IntegerField(default=0)
    twitter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def prettyDate(self):
        month = self.created_at.strftime("%B").capitalize()
        day = self.created_at.strftime("%d")
        year = self.created_at.strftime("%Y")
        return f"<span class='date'><span class='month'>{month}</span> <span class='day'>{day}</span><span class='year'>, {year}</span></span>"

    def allTags(self):
        return ",".join([tag.name for tag in self.tags.all()])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=200)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.post.title}"

class Subscriber(models.Model):
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
