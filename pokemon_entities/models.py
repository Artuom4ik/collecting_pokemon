from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=100)
    title_jp = models.CharField(max_length=100)
    image = models.ImageField(null=True)
    description = models.TextField(blank=True)
    previous_evolution = models.ForeignKey(
        "Pokemon",
        related_name="next_evolutions", 
        on_delete=models.SET_NULL, # on_delete - https://dvmn.org/encyclopedia/django_orm/on_delete/
        null=True, # null=True - превращает обязательное поле в необязательное в базе данных.
        blank=True) # blank=True - делает поле необязательным для заполнения в админке.

    def __str__(self):
        return f"{self.title}"


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.pokemon.title}, {self.latitude}, {self.longitude}"
# your models here
