# Generated by Django 5.1.3 on 2025-05-05 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("www", "0003_rename_tags_category_rename_posts_post_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ManyToManyField(related_name="post", to="www.category"),
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="post", to="www.tag"),
        ),
    ]
