# Generated by Django 3.2 on 2021-07-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_biodata_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodata',
            name='nationality',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
