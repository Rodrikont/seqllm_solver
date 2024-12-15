from abc import ABC, abstractmethod

class HandlerInterface(ABC):
    @abstractmethod
    def execute(data):
        """Обработка данных"""
        pass
