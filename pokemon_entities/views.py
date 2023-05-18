import folium
import json

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    today_data = localtime()
    for pokemon in pokemons:
        pokemons_entity = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=today_data, disappeared_at__gte=today_data)
        for pokemon_entity in pokemons_entity:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                pokemon.image.path
            )
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    today_data = localtime()
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
        pokemons_entityes = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=today_data, disappeared_at__gte=today_data)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entityes:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon.image.path
        )
    if pokemon.next_evolution:
        next_evolution = {
                "title_ru": pokemon.next_evolution.title,
                "pokemon_id": pokemon.next_evolution.id,
                "img_url":  pokemon.next_evolution.image.url
            }
    else:
        next_evolution = {}

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': {
            "img_url": pokemon.image.url,
            "title_ru": pokemon.title,
            "title_en": pokemon.title_en,
            "title_jp": pokemon.title_jp,
            "pokemon_id": pokemon.id,
            "description": pokemon.description,
            "next_evolution" : next_evolution
        }
    })
