# Generated by Django 5.1.1 on 2024-10-24 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resto', '0003_alter_restaurant_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='location',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]