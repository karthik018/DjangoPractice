# Generated by Django 2.2.2 on 2019-06-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20190626_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
