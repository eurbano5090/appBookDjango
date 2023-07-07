from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    list_display = ('id', 'titulo', 'autor', 'valoracion')
    list_filter = ('valoracion', 'fecha_modificacion')


# Register your models here.
admin.site.register(Book, BookAdmin)
