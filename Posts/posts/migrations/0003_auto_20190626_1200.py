# Generated by Django 2.2.2 on 2019-06-26 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20190626_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='commented_on_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Comments'),
        ),
    ]
