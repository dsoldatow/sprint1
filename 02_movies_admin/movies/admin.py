from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.name

    # Отображение полей в списке
    list_display = ('name', 'description', 'created', 'modified')

    # Поиск по полям
    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    def __str__(self):
        return self.tittle

    # Отображение полей в списке
    list_display = ('tittle', 'type', 'creation_date', 'rating', 'created', 'modified')

    # Фильтрация в списке
    list_filter = ('type',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)

    def __str__(self):
        return self.full_name

    # Отображение полей в списке
    list_display = ('full_name', 'created', 'modified')

    # Поиск по полям
    search_fields = ('full_name', 'id')
