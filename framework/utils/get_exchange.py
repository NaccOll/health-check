from abc import abstractmethod
from collections import defaultdict
from ..metaclass.no_instances_meta import NoInstancesMeta


class Subscriber(metaclass=NoInstancesMeta):
    @abstractmethod
    def subscribe(self, msg):
        pass


class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, subscriber):
        self._subscribers.add(subscriber)

    def detach(self, subscriber):
        self._subscribers.remove(subscriber)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.subscribe(msg)


# Dictionary of all created exchanges
_exchanges = defaultdict(Exchange)

# Return the Exchange instance associated with a given name


def get_exchange(name):
    return _exchanges[name]
