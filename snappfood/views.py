from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection

from snappfood.models import Shop, Address
from snappfood.helper_models import ShopModel, AddressModel, CityModel

def register_view(request):
    pass

def address_add_view(request):
    pass

def address_list_view(request):
    pass

def shop_list_view(request):
    response_data = {'result': True, 'errors': [], 'shops': []}
    query = '''
    SELECT "snappfood_shop"."id",
    "snappfood_shop"."name",
    "snappfood_shop"."about_text",
    "snappfood_shop"."minimum_bill_value",
    "snappfood_address"."id",
    "snappfood_address"."street",
    "snappfood_address"."alley",
    "snappfood_address"."plaque",
    "snappfood_city"."id",
    "snappfood_city"."name"
    FROM "snappfood_shop"
    INNER JOIN "snappfood_address" ON ("snappfood_shop"."address_id" = "snappfood_address"."id")
    INNER JOIN "snappfood_city" ON ("snappfood_address"."city_id" = "snappfood_city"."id")
    '''

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False, json_dumps_params={'ensure_ascii': False})
    print(fetch_res)
    for res in fetch_res:
        response_data['shops'].append(ShopModel(
            id=res[0],
            name=res[1],
            about_text=res[2],
            minimum_bill_value=res[3],
            address=AddressModel(
                id=res[4],
                street=res[5],
                alley=res[6],
                plaque=res[7],
                city=CityModel(
                    id=res[8],
                    name=res[9],
                )
            )
        ).serializee()
    )
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})
