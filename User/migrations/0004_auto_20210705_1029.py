# Generated by Django 3.2 on 2021-07-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='biodata',
            name='first_name',
            field=models.CharField(max_length=150, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='biodata',
            name='last_name',
            field=models.CharField(max_length=150, null=True, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='biodata',
            name='middle_name',
            field=models.CharField(max_length=150, null=True, verbose_name='last name'),
        ),
    ]
