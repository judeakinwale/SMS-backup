# Generated by Django 3.2.4 on 2021-09-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_courseadviser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academicdata',
            old_name='programme',
            new_name='specialization',
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='programme',
            new_name='specialization',
        ),
    ]
