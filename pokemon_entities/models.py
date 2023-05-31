from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название(рус)")
    title_en = models.CharField(max_length=100, verbose_name="Название(анг)")
    title_jp = models.CharField(max_length=100, verbose_name="Название(японский)")
    image = models.ImageField(null=True, verbose_name="Картинка")
    description = models.TextField(blank=True, verbose_name="Описание")
    previous_evolutions = models.ForeignKey(
        "Pokemon",
        related_name="next_evolutions", 
        on_delete=models.SET_NULL, # on_delete - https://dvmn.org/encyclopedia/django_orm/on_delete/
        null=True, # null=True - превращает обязательное поле в необязательное в базе данных.
        blank=True,
        verbose_name="Из кого эволюционировал") # blank=True - делает поле необязательным для заполнения в админке.

    def __str__(self):
        return f"{self.title}"


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    appeared_at = models.DateTimeField(verbose_name="Время появления")
    disappeared_at = models.DateTimeField(verbose_name="Время исчезания")
    level = models.IntegerField(null=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title}, {self.latitude}, {self.longitude}"
# your models here
