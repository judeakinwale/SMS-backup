# Generated by Django 3.2 on 2022-04-22 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0018_alter_grade_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessment.grade'),
        ),
    ]
