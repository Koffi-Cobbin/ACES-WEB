from django.contrib import admin

# Register your models here.
from .models import  ContactMessage, Event, Executive, ExecutiveRole, Configuration, Image, Course, Book, Project, Scholarship, Slider

admin.site.site_header = "ACES-KNUST"
admin.site.index_title = "Welcome to ACES, KNUST Administration Panel"



admin.site.register(Executive)
admin.site.register(ExecutiveRole)
admin.site.register(Configuration)
admin.site.register(Event)


admin.site.register(Course)
admin.site.register(Book)
admin.site.register(Image)
admin.site.register(ContactMessage)

admin.site.register(Slider)
admin.site.register(Project)
admin.site.register(Scholarship)