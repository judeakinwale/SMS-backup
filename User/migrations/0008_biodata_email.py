# Generated by Django 3.2 on 2021-07-05 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20210705_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='biodata',
            name='email',
            field=models.EmailField(default='', max_length=25, unique=True),
            preserve_default=False,
        ),
    ]
