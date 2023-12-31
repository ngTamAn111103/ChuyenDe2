# Generated by Django 4.2.7 on 2023-11-23 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0009_alter_profile_email"),
        ("chat", "0006_chatroom_is_block"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlockChat",
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
                (
                    "chatroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chatroom"
                    ),
                ),
                (
                    "profile_block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
        ),
    ]
