# Generated by Django 3.2.4 on 2021-08-17 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210817_2050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academicdata',
            old_name='ended',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='academicdata',
            old_name='started',
            new_name='start_date',
        ),
    ]