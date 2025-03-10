from django.contrib import admin
from .models import Profile  # Make sure Profile is correctly imported
from online_test.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Test_paper_subject1)
admin.site.register(Test_history)
admin.site.register(Test_paper_subject2)
admin.site.register(Test_paper_subject3)
if not admin.site.is_registered(Profile):
    @admin.register(Profile)
    class ProfileAdmin(admin.ModelAdmin):
        list_display = ['username', 'father_name', 'mother_name', 'phone', 'email']