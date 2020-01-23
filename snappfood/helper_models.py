class Model:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def serializee(self):
        the_dict = self.__dict__

        for i in the_dict:
            if type(the_dict[i]) not in [int, str]:
                print(the_dict[i])
                the_dict[i] = the_dict[i].serializee()

        return the_dict


class CityModel(Model):
    pass


class AddressModel(Model):
    pass


class ShopModel(Model):
    pass


class AdminModel(Model):
    pass


class CategoryModel(Model):
    pass


class FoodModel(Model):
    pass


class UserModel(Model):
    pass


class CartModel(Model):
    pass


class WalletModel(Model):
    pass


class DiscountModel(Model):
    pass


class InvoiceModel(Model):
    pass


class CommentModel(Model):
    pass
