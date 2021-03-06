# Generated by Django 3.2.4 on 2021-08-17 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_academicdata_programme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicdata',
            name='ended',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='academicdata',
            name='started',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='academichistory',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='academichistory',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
