from django.db.models import query
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.contrib import messages
from . import forms
from .import models
# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, *args, **kwargs): 
        context = super().get_context_data(*args, **kwargs)
        context['executives'] = models.Executive.objects.filter(is_active=True)
        context['upcoming_events'] = models.Event.objects.filter(is_upcoming=True)
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

class ExecutiveDetailView(DetailView):
    model = models.Executive
    context_object_name = "executive"
    template_name = "core/executive_detail.html"
 
class EventListView(ListView):
    model = models.Event
    context_object_name = "events"
    template_name = "core/event_list.html"

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

    def post(self, request, *args, **kwargs):
        contact_form = forms.ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save()
            messages.success(request, "Your input has been recorded")
        else:
            messages.error(request, "Sorry there was an error in your form. Please fix and try again.")
        return self.get(request, *args, **kwargs)



class HistoryView(TemplateView):
    template_name = "core/history.html"

class ProjectListView(ListView):
    model = models.Project
    context_object_name = "projects"
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

    def get_queryset(self):
        return models.Scholarship.objects.filter(end_date=None) | models.Scholarship.objects.filter(end_date__gte=timezone.now())

class ScholarshipDetailView(DetailView):
    model = models.Scholarship
    context_object_name = "scholarship"
    template_name = "core/scholarship_detail.html"

    def get_queryset(self):
        return models.Scholarship.objects.filter(end_date=None) | models.Scholarship.objects.filter(end_date__gte=timezone.now())


