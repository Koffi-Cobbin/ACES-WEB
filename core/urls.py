from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name="index"),
    path('about/', views.AboutPageView.as_view(), name="about"),
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/<int:pk>", views.EventDetailView.as_view(), name="event-detail"),
    path("events/<int:pk>/upload-image/", views.upload_event_images, name="upload-event-images"),
    path("executives/", views.ExecutiveListView.as_view(), name="executive-list"),
    path("executives/<int:pk>/", views.ExecutiveDetailView.as_view(), name="executive-detail"),
    path("social-links/", views.SocialLinksView.as_view(), name="social-links"),
    path("contact-us/", views.ContactView.as_view(), name="contact"),

   path("history/", views.HistoryView.as_view(), name="history"),
   path('course-materials/', views.CourseListView.as_view(), name="course-materials"),

    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("scholarships/", views.ScholarshipListView.as_view(), name="scholarship-list"),
    path("scholarships/<int:pk>", views.ScholarshipDetailView.as_view(), name="scholarship-detail"),

    path('articles/', views.ArticleListView.as_view(), name="article-list"),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name="article-detail"),
    path('articles/<int:pk>/vote/', views.article_vote, name="article-vote"),
    path('articles/<int:pk>/comment/', views.comment, name="article-comment"),
]