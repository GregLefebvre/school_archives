# Generated by Django 2.2.1 on 2019-12-23 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files_exchange', '0004_auto_20191222_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filehomework',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
