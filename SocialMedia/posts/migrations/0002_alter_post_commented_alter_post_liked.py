# Generated by Django 4.1 on 2023-10-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_country_alter_profile_gender'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='commented',
            field=models.ManyToManyField(default=True, related_name='comments', to='profiles.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='likes', to='profiles.profile'),
        ),
    ]