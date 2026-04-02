from typing import Any

class Status():
    def __init__(self, 
                 locked: bool = False, 
                 worker: str|None = None, 
                 operation: str|None = None, 
                 data: Any = None):
        self.locked = locked
        self.worker = worker
        self.operation = operation
        self.data = data
        
    def __repr__(self):
        return {
            "locked": self.locked,
            "worker": self.worker,
            "operation": self.operation,
            "data": self.data,
        }
        
    def to_dict(self):
        return self.__repr__()
        
    def __str__(self):
        return f"locked={self.locked}, worker={self.worker}, operation={self.operation}, data={self.data}"

class CardStatus():
    __status = {}
    
    def __init__(self, logger = None):
        self.logger = logger
    
    def set(self, card_id: int, status: Status):
        if card_id in self.__status.keys():
            if self.logger: self.logger.warn(f'Overwriting card {card_id} status')
        self.__status[card_id] = status
        return True
        
    def get(self, card_id: int):
        return self.__status.get(card_id, None)
    
    def delete(self, card_id: int):
        if not self.__status.pop(card_id, None):
            if self.logger: self.logger.warn(f'No status for card {card_id}')
            return False
        return True