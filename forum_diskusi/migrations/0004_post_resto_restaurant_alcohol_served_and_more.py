# Generated by Django 5.1.1 on 2024-10-27 07:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_diskusi', '0003_restaurant_vote'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='resto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='forum_diskusi.restaurant'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='alcohol_served',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='appetizer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='beef',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='chicken',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='delivery',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='dessert',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='drinks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='other_dish',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='other_poultry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='outdoor',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='reservation',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='seafood',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='smoking_area',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='specialized',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='takeaway',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='wifi',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_type',
            field=models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'post')},
        ),
    ]
