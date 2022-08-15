from django.db import models

STR_LEN = 15


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        unique=True,
        max_length=200
    )
    slug = models.SlugField(
        'Адрес',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Category {self.name}, slug {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        'Адрес',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name[:STR_LEN]}'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name[:STR_LEN]}'
