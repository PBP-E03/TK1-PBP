# Generated by Django 5.1.1 on 2024-10-27 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_diskusi', '0005_alter_post_resto'),
        ('resto', '0010_alter_restaurant_special_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='resto',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='resto.restaurant'),
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
