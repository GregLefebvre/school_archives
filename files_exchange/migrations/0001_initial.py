# Generated by Django 2.2.1 on 2019-12-20 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import files_exchange.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug_title', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug_title', models.SlugField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug_title', models.SlugField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('nb_files', models.IntegerField(default=0)),
                ('nb_promos', models.IntegerField(default=0)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files_exchange.TypeSchool')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug_title', models.SlugField(max_length=100)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files_exchange.TypeSchool')),
            ],
        ),
        migrations.CreateModel(
            name='FileHomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug_title', models.SlugField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('nb_views', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to=files_exchange.models.path_and_rename)),
                ('status', models.IntegerField(default=0)),
                ('promo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files_exchange.Promo')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files_exchange.School')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
