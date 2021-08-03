
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.fields  import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
import bs4
from ckeditor.fields import RichTextField
from django.utils import timezone

User = get_user_model()
# Create your models here.

class Configuration(models.Model):
    location = models.CharField(max_length=500)
    main_phone_number = models.CharField(max_length=13)
    office_phone_number = models.CharField(max_length=13)
    email_address = models.EmailField()
    about = RichTextField()
    history = RichTextField()
    banner_prefix_text = models.CharField(max_length=40)
    banner_title = models.CharField(max_length=40)
    banner_subtitle = models.CharField(max_length=100)

    banner_image = models.ImageField(upload_to="banner_image/")

    # social links
    whatsapp_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    
    def __str__(self):
        return "Site Configuration"

    def get_about_text(self):
        return bs4.BeautifulSoup(self.about, 'html.parser').get_text()
        
    @classmethod
    def object(cls):
        return cls.objects.first()
    
    
    def save(self, *args, **kwargs):
        self.pk = 1
        self.id = 1
        super().save(*args, **kwargs)

class Slider(models.Model):
    banner = models.ImageField(upload_to="slider/%Y/%m/")
    title = models.CharField(max_length=60)
    sub_title = models.CharField(max_length=50)

    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.title

    
class Image(models.Model):
    image = models.ImageField(upload_to="gallery/images/%Y/%m/")
    description = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType,null=True, on_delete=models.CASCADE, blank=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)
    
    @classmethod
    def for_model(cls,*,image, description, content_object: models.Model):
        _image = cls(image=image, description=description, content_object=content_object)
        _image.save()
        return _image

        

    
class ExecutiveRole(models.Model):
    name = models.CharField(max_length=100)
    core = models.BooleanField(default=True)
    duty = models.TextField()
    class Meta:
        ordering = ("core", 'name')
    
    def __str__(self) -> str:
        return self.name

class Executive(models.Model):
    executive_role = models.ForeignKey(ExecutiveRole, related_name="executives", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    about = RichTextField()
    picture = models.ImageField(upload_to='executives/images/%Y/')
    is_active = models.BooleanField(default=True)
    date_started = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("-is_active", "executive_role", "date_created")
    
    def __str__(self) -> str:
        return self.name
    
    def get_about_text(self):
        return bs4.BeautifulSoup(self.about, 'html.parser').get_text()

    def get_absolute_url(self) -> str:
        return reverse('core:executive-detail', kwargs={'pk': self.pk})


class Event(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(upload_to="events/%Y/%m/")
    description = RichTextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=500)
    images = GenericRelation(Image, related_query_name="event")
    is_upcoming = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date", "date_created", "name")
    
    def __str__(self) -> str:
        return self.name

    def get_description_text(self):
        return bs4.BeautifulSoup(self.description, 'html.parser').get_text()

    def get_absolute_url(self) -> str:
        return reverse("core:event-detail",kwargs={"pk": self.pk} )


class Course(models.Model):
    YEAR_CHOICES = (
        (100, "Level 100"),
        (200, "Level 200"),
        (300, "Level 300"),
        (400, "Level 400"),
    )
    year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("year", "title")
    
    def __str__(self):
        return self.title

class Book(models.Model):
    course = models.ForeignKey(Course, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = RichTextField(blank=True)
    book = models.FileField(upload_to="books/%Y/")

    class Meta:
        ordering = ("course", "title")

    def __str__(self):
        return self.title
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name + self.message[:20]
    


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    picture = models.ImageField(upload_to="projects/%Y/%m/")
    project_url = models.URLField(blank=True)
    slug = models.SlugField(blank=True)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField(blank=True)
    completed = models.BooleanField(default=False)
    images = GenericRelation(Image, related_query_name="project")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created", "title")
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.title} {self.pk}")
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:project-detail", kwargs={"slug": self.slug})


class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    application_link = models.URLField(blank=True)

    end_date = models.DateField(blank=True)

    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("date", "title")
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        if not self.end_date:
            return True
        return timezone.now() >= self.end_date
    
    def get_absolute_url(self):
        return reverse("core:scholarship-detail", kwargs={"pk": self.pk})
class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='article-images/')
    content = RichTextField()
    categories = models.ManyToManyField(ArticleCategory, related_name="articles", symmetrical=True)
    is_draft = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified  = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-date_created', )
        
    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('core:article-detail', kwargs={'pk': self.pk})
    
    def get_comment_url(self):
        return reverse('core:article-comment', kwargs={'pk': self.pk})
    
    def get_vote_url(self):
        return reverse('core:article-vote', kwargs={'pk': self.pk})
    def evaluate_votes(self):
        return sum([vote.vote for vote in self.votes.all() ])

class ArticleComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_comments")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.content

class ArticleVote(models.Model):
    VOTE_CHOICES = (
        (1,1),
        (-1,-1)
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_votes")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="votes")
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('author', 'article')

class CodeTry(models.Model):
    author = models.ForeignKey(User, related_name="posted_code_tries", blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_ended = models.DateTimeField()
    is_draft = models.BooleanField(default=False)