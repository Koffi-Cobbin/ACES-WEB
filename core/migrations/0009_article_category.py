# Generated by Django 3.1.6 on 2021-03-08 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210308_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(related_name='articles', to='core.ArticleCategory'),
        ),
    ]