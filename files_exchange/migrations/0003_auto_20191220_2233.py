# Generated by Django 2.2.1 on 2019-12-20 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files_exchange', '0002_auto_20191220_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='filehomework',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='files_exchange.Subject'),
        ),
    ]
