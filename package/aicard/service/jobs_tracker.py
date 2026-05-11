from typing import Any
import threading

class Job():
    def __init__(self, 
                 worker: str|None = None, 
                 operation: str|None = None, 
                 data: Any = None):
        self.worker = worker
        self.operation = operation
        self.data = data
        
    def __repr__(self):
        return f"worker={self.worker}, operation={self.operation}, data={self.data}"
        
    def to_dict(self):
        return {
            "worker": self.worker,
            "operation": self.operation,
            "data": self.data,
        }
        
    def __str__(self):
        return f"worker={self.worker}, operation={self.operation}, data={self.data}"

class CardJobsTracker():
    __jobs = {} # active
    __last_job = {} # last finished job of each card_id
    __last_id = 0
    
    
    def __init__(self, logger = None):
        self.logger = logger
    
    def set(self, card_id: int, job: Job):
        if card_id in self.__jobs.keys():
            if self.logger: self.logger.warn(f'Overwriting card {card_id} job')
            job_id = job.id
        else:
            self.__last_id += 1
            job_id = self.__last_id
        job.id = job_id
        self.__jobs[card_id] = job
        return True
    
    def get(self, card_id: int):
        return self.__jobs.get(card_id, None)
    
    def get_last(self, card_id: int):
        return self.__last_job.get(card_id, None)
    
    def set_last(self, card_id: int, job: Job):
        self.__last_job[card_id] = job
    
    def pop_last(self, card_id: int):
        return self.__last_job.pop(card_id, None)

    def delete(self, card_id: int, timer=5):
        if card_id not in self.__jobs:
            if self.logger: self.logger.warn(f'No job for card {card_id}')
            return False
        job = self.get(card_id)
        self.set_last(card_id, job)
        def _delayed_delete():
            if self.__jobs.pop(card_id, None) is None:
                if self.logger: self.logger.warn(f'Job already removed for card {card_id}')
        t = threading.Timer(timer, _delayed_delete)
        t.start()
        return True