from django.contrib import admin


# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
    ]
    fieldsets = [
        *UserAdmin.fieldsets,
    ]
    fieldsets.insert(
        2,
        (
            "Profile Information",
            {
                "fields": (
                   
                    "picture",
                    "phone_number",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


