# Generated by Django 5.1.1 on 2024-10-23 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_restaurant_description_restaurant_rating_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
