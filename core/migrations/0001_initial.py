# Generated by Django 3.2 on 2021-08-26 16:14

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('sub_title', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='article-images/')),
                ('content', ckeditor.fields.RichTextField()),
                ('is_draft', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=500)),
                ('main_phone_number', models.CharField(max_length=13)),
                ('office_phone_number', models.CharField(max_length=13)),
                ('email_address', models.EmailField(max_length=254)),
                ('about', ckeditor.fields.RichTextField()),
                ('mission', ckeditor.fields.RichTextField()),
                ('history', ckeditor.fields.RichTextField()),
                ('banner_prefix_text', models.CharField(max_length=40)),
                ('banner_title', models.CharField(max_length=40)),
                ('banner_subtitle', models.CharField(max_length=100)),
                ('banner_image', models.ImageField(upload_to='banner_image/')),
                ('whatsapp_link', models.URLField(blank=True)),
                ('facebook_link', models.URLField(blank=True)),
                ('twitter_link', models.URLField(blank=True)),
                ('youtube_link', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(choices=[(100, 'Level 100'), (200, 'Level 200'), (300, 'Level 300'), (400, 'Level 400')])),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('year', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('picture', models.ImageField(upload_to='events/%Y/%m/')),
                ('description', ckeditor.fields.RichTextField()),
                ('date', models.DateTimeField()),
                ('venue', models.CharField(max_length=500)),
                ('is_upcoming', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date', 'date_created', 'name'),
            },
        ),
        migrations.CreateModel(
            name='ExecutiveRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('core', models.BooleanField(default=True)),
                ('duty', models.TextField()),
            ],
            options={
                'ordering': ('core', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('picture', models.ImageField(upload_to='projects/%Y/%m/')),
                ('project_url', models.URLField(blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('date_started', models.DateTimeField()),
                ('date_ended', models.DateTimeField(blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date_created', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('application_link', models.URLField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('date', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(upload_to='slider/%Y/%m/')),
                ('title', models.CharField(max_length=60)),
                ('sub_title', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/images/%Y/%m/')),
                ('description', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Executive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('about', ckeditor.fields.RichTextField()),
                ('picture', models.ImageField(upload_to='executives/images/%Y/')),
                ('is_active', models.BooleanField(default=True)),
                ('date_started', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('executive_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executives', to='core.executiverole')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-is_active', 'executive_role', 'date_created'),
            },
        ),
        migrations.CreateModel(
            name='CodeTry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_ended', models.DateTimeField()),
                ('is_draft', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posted_code_tries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('book', models.FileField(upload_to='books/%Y/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='core.course')),
            ],
            options={
                'ordering': ('course', 'title'),
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(related_name='articles', to='core.ArticleCategory'),
        ),
        migrations.CreateModel(
            name='ArticleVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(choices=[(1, 1), (-1, -1)])),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='core.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('author', 'article')},
            },
        ),
    ]
