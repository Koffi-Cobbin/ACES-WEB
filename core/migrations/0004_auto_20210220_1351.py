# Generated by Django 3.1.6 on 2021-02-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210218_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executive',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]