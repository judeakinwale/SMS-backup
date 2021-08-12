# Generated by Django 3.2.4 on 2021-08-12 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_alter_level_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='code',
            field=models.IntegerField(choices=[(100, 'One'), (200, 'Two'), (300, 'Three'), (400, 'Four'), (500, 'Five')], default=100, null=True),
        ),
    ]