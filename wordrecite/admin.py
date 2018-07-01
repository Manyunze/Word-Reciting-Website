from django.contrib import admin

# Register your models here.
from .models import UserAttrib, Word, Vocabulary, Note, UserWord, Task


admin.site.register(UserAttrib)
admin.site.register(UserWord)
admin.site.register(Note)
admin.site.register(Vocabulary)
admin.site.register(Word)
admin.site.register(Task)
