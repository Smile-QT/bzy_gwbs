from django.contrib import admin

# Register your models here.
from app.gwbs.models import User, UserAnswer, ExamTime

admin.site.register(User)
admin.site.register(UserAnswer)
admin.site.register(ExamTime)
