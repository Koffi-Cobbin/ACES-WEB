from django.db.models import Q
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.contrib import messages
from django.utils import timezone
from . import forms
import json
from .import models
# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, *args, **kwargs): 
        context = super().get_context_data(*args, **kwargs)
        context['executives'] = models.Executive.objects.filter(is_active=True)
        context['upcoming_events'] = models.Event.objects.filter(is_upcoming=True)
        print("Hello world")
        return context

class AboutPageView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = models.Image.objects.all()[:12]
        return context

class HomePageView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['executives'] = models.Executive.objects.filter(is_active=True)
        context['upcoming_events'] = models.Event.objects.filter(is_upcoming=True)
        context["sliders"] = models.Slider.objects.all()
        return context

class AboutPageView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["executives"] = models.Executive.objects.filter(is_active=True)
        context["images"] = models.Image.objects.all()
        return context

class CourseListView(TemplateView):
    template_name = "core/course_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        levels = []
        for year, _ in models.Course.YEAR_CHOICES:
            levels.append(
                {
                    'level': year,
                    'courses':models.Course.objects.filter(year=year)
                }
            )
        context['levels'] = levels
        return context


class ExecutiveListView(ListView):
    model = models.Executive
    context_object_name = "executives"
    template_name = "core/executive_list.html"
    paginate_by = 24

class ExecutiveDetailView(DetailView):
    model = models.Executive
    context_object_name = "executive"
    template_name = "core/executive_detail.html"
 
class EventListView(ListView):
    model = models.Event
    context_object_name = "events"
    template_name = "core/event_list.html"

    paginate_by = 24

class EventDetailView(DetailView):
    model = models.Event
    context_object_name = "event"
    template_name = "core/event_detail.html"
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["image_form"] = forms.ImageUploadForm()
        return context

@login_required
def upload_event_images(request: HttpRequest, pk:int) -> HttpRequest:
    event = get_object_or_404(models.Event, pk=pk)
    if not request.user.is_superuser:
        return redirect(event.get_absolute_url())
    if request.method == "POST":
        image_form = forms.ImageUploadForm(request.POST, files=request.FILES)
        if image_form.is_valid():
            d = image_form.cleaned_data
            for image in request.FILES.getlist('image'):
                models.Image.for_model(image=image, description=d["description"], content_object=event)
            
    return redirect(event.get_absolute_url())


class SocialLinksView(TemplateView):
    template_name = "core/social_links.html"        

class ContactView(TemplateView):
    template_name = "core/contact.html"
    contact_form = None

    def post(self, request, *args, **kwargs):
        self.contact_form = forms.ContactForm(request.POST)
        if self.contact_form.is_valid():
            contact = self.contact_form.save()
            messages.success(request, "Your input has been recorded")
        else:
            messages.error(request, "Sorry there was an error in your form. Please fix and try again.")
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context["contact_form"] = self.contact_form  if self.contact_form else forms.ContactForm()
        return context



class HistoryView(TemplateView):
    template_name = "core/history.html"

class ProjectListView(ListView):
    model = models.Project
    context_object_name = "projects"
    paginate_by = 24
    template_name = "core/project_list.html"

class ProjectDetailView(DetailView):
    model = models.Project
    context_object_name = "project"
    template_name = "core/project_detail.html"
    image_form = None

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["image_form"] = forms.ImageUploadForm()
        return context

    @method_decorator(login_required)
    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_superuser:
            return self.get(request, *args, **kwargs)
        project = self.get_object()
        if not project:
            return self.get(request, *args, **kwargs)
        if request.method == "POST":
            self.image_form = forms.ImageUploadForm(request.POST, files=request.FILES)
            if self.image_form.is_valid():
                d = self.image_form.cleaned_data
                for image in request.FILES.getlist('image'):
                    models.Image.for_model(image=image, description=d["description"], content_object=project)
        return self.get(request, *args, **kwargs)


class ScholarshipListView(ListView):
    model = models.Scholarship
    template_name = "core/scholarship_list.html"
    context_object_name = "scholarships"
    paginate_by = 24

    def get_queryset(self):
        return models.Scholarship.objects.filter(end_date=None) | models.Scholarship.objects.filter(end_date__gte=timezone.now())

class ScholarshipDetailView(DetailView):
    model = models.Scholarship
    context_object_name = "scholarship"
    template_name = "core/scholarship_detail.html"

    def get_queryset(self):
        return models.Scholarship.objects.filter(end_date=None) | models.Scholarship.objects.filter(end_date__gte=timezone.now())


class ArticleListView(ListView):
    queryset = models.Article.objects.filter(is_draft=False)
    template_name = "core/article_list.html"
    context_object_name = "articles"
    category = None
    paginate_by = 24

    def get_queryset(self):
        queryset = self.queryset
        category_id = self.request.GET.get("category")
        if category_id:
            self.category = get_object_or_404(models.ArticleCategory, pk=int(category_id))
            queryset = queryset.filter(categories=self.category)
        self.search_term = self.request.GET.get("search")
        if self.search_term:
            queryset = queryset.filter(Q(title__icontains=self.search_term)| Q(content__icontains=self.search_term))
        return queryset
        

    def get_context_data(self):
        context = super().get_context_data()
        context['article_categories'] = models.ArticleCategory.objects.all()
        context['selected_category'] = self.category
        context['search_term'] = self.search_term
        return context

class ArticleDetailView(DetailView):
    model = models.Article
    queryset = models.Article.objects.filter(is_draft=False)
    context_object_name='article'
    template_name = "core/article_detail.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm()
        return context

@login_required
def article_vote(request: HttpRequest, pk) -> HttpResponse:
    if request.method == "POST":
        article = get_object_or_404(models.Article, pk=pk)
        articlevote = models.ArticleVote.objects.get_or_create(article=article, author = request.user)[0]
        print(articlevote)
        vote = json.loads(request.body)
        if vote < -1 or vote > 1:
            raise Http404("Vote must be between 0 and 1")
        articlevote.vote = int(vote)
        articlevote.save()
    return JsonResponse({
        'votes': article.evaluate_votes(),
        'current_user_vote':vote,
    })

@login_required
def comment(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(models.Article, pk=pk, is_draft=False)
    if not request.method == "POST":
        messages.error(request, "only post requests allowed.")
    else:
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment: models.ArticleComment = comment_form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            messages.success(request, "Comment saved successfully")
        else:
            messages.error(request, "Your comment could not be saved. Kindly fix the errors in the form.") 
            messages.error(request, comment_form.errors.as_text())
    return redirect(article.get_absolute_url())
