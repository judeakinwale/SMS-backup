# Generated by Django 3.2.4 on 2021-09-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0011_alter_session_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]