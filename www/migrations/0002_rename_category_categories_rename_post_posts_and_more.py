# Generated by Django 5.1.3 on 2025-05-04 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("www", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Category",
            new_name="Categories",
        ),
        migrations.RenameModel(
            old_name="Post",
            new_name="Posts",
        ),
        migrations.RenameModel(
            old_name="Subscriber",
            new_name="Subscribers",
        ),
        migrations.RenameModel(
            old_name="Tag",
            new_name="Tags",
        ),
    ]
