# Generated by Django 2.2.1 on 2019-12-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_exchange', '0009_moderation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderation',
            name='is_suitable',
            field=models.BooleanField(null=True),
        ),
    ]
