import uuid

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from snappfood.models import Shop, Address
from snappfood.helper_models import ShopModel, AddressModel, CityModel, UserModel, CartModel


def get_user_id_by_token(req_meta):
    if not 'HTTP_AUTHORIZATION' in req_meta:
        return None
    token = req_meta['HTTP_AUTHORIZATION']
    query = '''
    SELECT "snappfood_user"."id"
    FROM "snappfood_user"
    WHERE ("snappfood_user"."token" = '%s');
    ''' % (
        token
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchone()
        except Exception as ex:
            print(str(ex))
            return None
    if fetch_res:
        return fetch_res[0]
    return None


@csrf_exempt
def register_view(request):
    response_data = {'result': True, 'errors': []}
    query = '''
    INSERT INTO "snappfood_user"
    ("token", "first_name", "last_name", "phone_number", "email", "password")
    VALUES
    ('%s', '%s', '%s', '%s', '%s', '%s');
    ''' % (
        uuid.uuid4(),
        request.POST['first_name'],
        request.POST['last_name'],
        request.POST['phone_number'],
        request.POST['email'],
        request.POST['password'],
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            user_pk = cursor.lastrowid
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})

    cart_query = '''
    INSERT INTO "snappfood_cart" ("user_id") VALUES (%d)
    ''' % (
        user_pk,
    )
    query = '''
    SELECT "snappfood_user"."token"
    FROM "snappfood_user"
    WHERE "snappfood_user"."id" = %d;
    ''' % (
        user_pk,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(cart_query)
            cursor.execute(query)
            fetch_res = cursor.fetchone()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    response_data['token'] = fetch_res[0]

    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def edit_profile_view(request):
    response_data = {'result': True, 'errors': []}
    query = '''
     UPDATE "snappfood_user"
     SET "first_name" = '%s',
     "last_name" = '%s',
     "phone_number" = '%s',
     "email" = '%s',
     "password" = '%s' WHERE "snappfood_user"."id" = 6
    ''' % (
        request.POST['first_name'],
        request.POST['last_name'],
        request.POST['phone_number'],
        request.POST['email'],
        request.POST['password'],
    )

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    print(fetch_res)
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def login_view(request):
    response_data = {'result': True, 'errors': []}
    query = '''
    SELECT "snappfood_user"."token"
    FROM "snappfood_user"
    WHERE ("snappfood_user"."phone_number" = '%s' AND "snappfood_user"."password" = '%s');
    ''' % (
        request.POST['phone_number'],
        request.POST['password'],
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchone()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    response_data['token'] = fetch_res[0]
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def address_add_view(request):
    user_pk = get_user_id_by_token(request.META)
    if not user_pk:
        raise Http404

    response_data = {'result': True, 'errors': []}
    query = '''
    INSERT INTO "snappfood_address"
    ("user_id", "city_id", "x", "y", "street", "alley", "plaque")
    VALUES
    (%d, %s, %s, %s, '%s', '%s', '%s')
    ''' % (
        user_pk,
        request.POST['city_id'],
        request.POST['x'],
        request.POST['y'],
        request.POST['street'],
        request.POST['alley'],
        request.POST['plaque'],
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    print(fetch_res)
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def address_list_view(request):
    user_pk = get_user_id_by_token(request.META)
    if not user_pk:
        raise Http404

    response_data = {'result': True, 'errors': [], 'addresses': []}
    query = '''
    SELECT "snappfood_address"."id",
    "snappfood_address"."street",
    "snappfood_address"."alley",
    "snappfood_address"."plaque"
    FROM "snappfood_address"
    INNER JOIN "snappfood_user"
    ON ("snappfood_address"."user_id" = "snappfood_user"."id")
    WHERE "snappfood_user"."id" = '%s'
    ''' % (
        user_pk,
    )

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    print(fetch_res)
    for res in fetch_res:
        response_data['addresses'].append(AddressModel(
            id=res[0],
            street=res[1],
            alley=res[2],
            plaque=res[3],
        ).serializee()
                                          )
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
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
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
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

@csrf_exempt
def shop_details_view(request, pk):
    response_data = {'result': True, 'errors': [], 'shop': None}
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
    WHERE "snappfood_shop"."id" = %d
    ''' % (
        pk,
    )

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            res = cursor.fetchone()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})

    response_data['shop'] = ShopModel(
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

    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def city_list_view(request):
    response_data = {'result': True, 'errors': [], 'cities': []}
    query = '''
    SELECT "snappfood_city"."id",
    "snappfood_city"."name" FROM "snappfood_city"
    '''

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchall()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    print(fetch_res)
    for res in fetch_res:
        response_data['cities'].append(CityModel(
            id=res[0],
            name=res[1],
        ).serializee()
                                      )
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def profile_view(request):
    user_pk = get_user_id_by_token(request.META)
    if not user_pk:
        raise Http404

    response_data = {'result': True, 'errors': [], 'profile': None}
    query = '''
    SELECT "snappfood_user"."id",
    "snappfood_user"."first_name",
    "snappfood_user"."last_name",
    "snappfood_user"."phone_number",
    "snappfood_user"."email",
    "snappfood_cart"."id"
    FROM "snappfood_user" INNER JOIN "snappfood_cart"
    ON ("snappfood_cart"."user_id" = "snappfood_user"."id")
    WHERE ("snappfood_user"."id" = %d);
    ''' % (
        user_pk,
    )

    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = cursor.fetchone()
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    res = fetch_res
    response_data['profile'] = UserModel(
        id=res[0],
        first_name=res[1],
        last_name=res[2],
        phone_number=res[3],
        email=res[4],
        cart=CartModel(
            id=res[5]
        )
    ).serializee()

    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def cart_add_view(request):
    pass
