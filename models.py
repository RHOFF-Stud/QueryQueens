from mongoengine import DynamicDocument, DynamicEmbeddedDocument


class Customer(DynamicDocument):
    def __init__(self):
        super().__init__()


class Supplier(DynamicDocument):
    def __init__(self):
        super().__init__()


class Order(DynamicDocument):
    def __init__(self):
        super().__init__()


class TShirt(DynamicEmbeddedDocument):
    def __init__(self):
        super().__init__()


class Product(DynamicDocument):
    def __init__(self):
        super().__init__()


class Cart(DynamicDocument):
    def __init__(self):
        super().__init__()


class Storage(DynamicDocument):
    def __init__(self):
        super().__init__()


models = {
    "Customer": Customer,
    "Supplier": Supplier,
    "Order": Order,
    "Product": Product,
    "Cart": Cart,
    "Storage": Storage
}
