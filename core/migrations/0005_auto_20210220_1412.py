# Generated by Django 3.1.6 on 2021-02-20 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210220_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='year',
            field=models.PositiveIntegerField(choices=[(100, 'Level 100'), (200, 'Level 200'), (300, 'Level 300'), (400, 'Level 400')], max_length=3),
        ),
    ]