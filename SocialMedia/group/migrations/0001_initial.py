# Generated by Django 4.2.7 on 2023-11-28 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "avatar",
                    models.ImageField(
                        default="avatar_default.jpg", upload_to="avatars/"
                    ),
                ),
                (
                    "cover",
                    models.ImageField(
                        default="avatar_default.jpg", upload_to="avatars/"
                    ),
                ),
                ("description", models.TextField(default="Mô tả nhóm....")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "admins",
                    models.ManyToManyField(
                        related_name="group_admins", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="GroupMember", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="avatars/")),
                ("content", models.TextField(default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_group",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="group.group"
                    ),
                ),
            ],
        ),
    ]