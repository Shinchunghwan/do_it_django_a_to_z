# Generated by Django 4.1.3 on 2022-11-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_updated_at_alter_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='head_image',
            field=models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d/'),
        ),
    ]
