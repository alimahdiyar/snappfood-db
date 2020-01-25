import copy

from django.db import connection

class InvoiceStatusConsts:
    NOT_PAID = "پرداخت نشده"

def srlz(obj):
    if obj is None or type(obj) in [int, str]:
        return obj

    if type(obj) == dict:
        the_dict = copy.deepcopy(obj)
    else:
        the_dict = copy.deepcopy(obj.__dict__)

    for i in the_dict:
        if type(the_dict[i]) == list:
            for x in range(len(the_dict[i])):
                the_dict[i][x] = srlz(the_dict[i][x])
        elif type(the_dict[i]) == dict:
            for x in the_dict[i]:
                the_dict[i][x] = srlz(the_dict[i][x])
        elif type(the_dict[i]) not in [int, str]:
            the_dict[i] = srlz(the_dict[i])

    return the_dict


class ModelField:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Model:
    table_name_prefix = ''

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def update(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return self

    def serializee(self):
        return srlz(self)


class CityModel(Model):
    pass


class AddressModel(Model):
    pass


class ShopModel(Model):
    table_name = 'shop'
    fields = (
        ModelField('address', AddressModel)
    )

    def read_from_db(self, **kwargs):
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
            self.id,
        )

        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                res = cursor.fetchone()
            except Exception as ex:
                print(str(ex))
                raise ex
        self.update(
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

        return self


class AdminModel(Model):
    pass


class CategoryModel(Model):
    pass


class FoodModel(Model):
    pass


class UserModel(Model):
    pass


class CartModel(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.items = []
        query = '''
            SELECT "snappfood_food"."id",
            "snappfood_food"."name",
            "snappfood_food"."about",
            "snappfood_food"."price",
            "snappfood_food"."discount",
            "snappfood_food"."shop_id"
            FROM "snappfood_food"
            INNER JOIN "snappfood_cart_items"
            ON ("snappfood_food"."id" = "snappfood_cart_items"."food_id")
            WHERE "snappfood_cart_items"."cart_id" = %d
            ''' % (
            self.id,
        )

        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                fetch_res = cursor.fetchall()
            except Exception as ex:
                print(str(ex))
                raise ex
        print(fetch_res)
        for res in fetch_res:
            self.items.append(FoodModel(
                id=res[0],
                name=res[1],
                about=res[2],
                price=res[3],
                discount=res[4],
                shop=ShopModel(
                    id=res[5]
                ).read_from_db()
            )
            )


class WalletModel(Model):
    pass


class DiscountModel(Model):
    pass


class InvoiceModel(Model):
    pass


class CommentModel(Model):
    pass
