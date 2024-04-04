# from enum import Enum

class OrderStatus(object):

    BOOKED = 1,
    ACTIVE = 2,
    CANCELLED = 3,

    @staticmethod
    def list():
        return list(map(lambda c: (c.name, c.value), OrderStatus))