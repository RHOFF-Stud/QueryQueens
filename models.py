import json

from mongoengine import DynamicDocument, DynamicEmbeddedDocument

from path import db


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


class Logs(DynamicDocument):
    def __init__(self):
        super().__init__()


models = {
    "Customer": Customer,
    "Supplier": Supplier,
    "Order": Order,
    "Product": Product,
    "Logs": Logs
}
