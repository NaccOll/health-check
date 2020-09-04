import sys
from abc import abstractmethod

from ....metaclass.singleton_meta import SingletonMeta


class AbstractNotify:

    @abstractmethod
    def send_text(self, sender_name, text: str):
        class_name = self.__class__
        method_name = sys._getframe().f_code.co_name
        raise NotImplementedError(
            f"{class_name} no implement {method_name}")
