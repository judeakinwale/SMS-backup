# Generated by Django 3.2 on 2022-06-22 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0021_semester_is_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='code',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
