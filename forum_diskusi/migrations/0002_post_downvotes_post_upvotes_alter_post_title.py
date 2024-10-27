# Generated by Django 5.1.1 on 2024-10-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_diskusi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
