from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    description = models.TextField(blank=True)

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
