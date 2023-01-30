from mongoengine import DynamicDocument, DynamicEmbeddedDocument


class User(DynamicDocument):
    def __init__(self):
        super().__init__()


class Supplier(DynamicDocument):
    def __init__(self):
        super().__init__()


class Order(DynamicDocument):
    def __init__(self):
        super().__init__()


class Product(DynamicDocument):
    def __init__(self):
        super().__init__()


class Cart(DynamicDocument):
    def __init__(self):
        super().__init__()


class Log(DynamicDocument):
    def __init__(self):
        super().__init__()


models = {
    "User": User,
    "Supplier": Supplier,
    "Order": Order,
    "Product": Product,
    "Cart": Cart,
    'Log': Log
}
