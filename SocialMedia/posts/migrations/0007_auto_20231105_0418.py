# Generated by Django 3.2.7 on 2023-11-05 04:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20231105_0416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.FileField(blank=True, upload_to='post', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'mp4', 'mov'])]),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
