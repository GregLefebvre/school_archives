# Generated by Django 2.2.1 on 2019-12-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filehomework',
            name='slug_title',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='promo',
            name='slug_title',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='slug_title',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug_title',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='typeschool',
            name='slug_title',
            field=models.SlugField(max_length=100, null=True),
        ),
    ]
