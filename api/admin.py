from django.contrib import admin

from api.models import Poll, Question, Answer, Value

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Value)