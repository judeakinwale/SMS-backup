# Generated by Django 3.2 on 2021-07-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20210705_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='biodata',
            name='matric_no',
            field=models.CharField(default='', max_length=300),
        ),
    ]
