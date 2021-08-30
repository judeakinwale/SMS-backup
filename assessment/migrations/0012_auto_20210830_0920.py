# Generated by Django 3.2.4 on 2021-08-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0011_alter_quiztaker_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
