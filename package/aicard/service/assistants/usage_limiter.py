import threading
from datetime import datetime


class UsageLimiter:
    def __init__(self, usage_limits: dict):
        self.__usage_limits = usage_limits
        self.usage_counter = {}
        self.__lock = threading.Lock()
        self.__last_reset_date = datetime.now().date()

    def try_increment(self, user_name: str, agent: str) -> bool:
        with self.__lock:
            self.__reset_if_needed()

            user_counters = self.usage_counter.setdefault(user_name, {})
            counter = user_counters.get(agent, 0)
            limit = self.__usage_limits.get(agent, 999)

            if counter >= limit:
                return False

            user_counters[agent] = counter + 1
            return True

    def __reset_if_needed(self):
        current_date = datetime.now().date()

        if current_date != self.__last_reset_date:
            self.usage_counter = {}
            self.__last_reset_date = current_date