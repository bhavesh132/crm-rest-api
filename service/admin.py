from django.contrib import admin
from .models import Type, SubType, Ticket, Task, Note

# Register your models here.
admin.site.register(Type)
admin.site.register(SubType)
admin.site.register(Ticket)
admin.site.register(Task)
admin.site.register(Note)