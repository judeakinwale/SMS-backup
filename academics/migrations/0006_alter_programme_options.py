# Generated by Django 3.2.4 on 2021-09-18 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0005_alter_programme_max_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programme',
            options={'verbose_name': 'Specialization', 'verbose_name_plural': 'Specializations'},
        ),
    ]
