# Generated by Django 3.2 on 2022-01-25 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0015_auto_20210925_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='timer',
            field=models.IntegerField(default=15),
        ),
    ]