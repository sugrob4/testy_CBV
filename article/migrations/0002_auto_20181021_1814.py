# Generated by Django 2.0.7 on 2018-10-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='email_user',
            field=models.EmailField(blank=True, max_length=70),
        ),
        migrations.AddField(
            model_name='comments',
            name='login_user',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
