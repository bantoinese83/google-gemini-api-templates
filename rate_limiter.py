import logging
import threading
import time


class RateLimiter:
    def __init__(self, max_requests_per_minute, max_tokens_per_minute, max_requests_per_day, whitelist=None,
                 blacklist=None):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_tokens_per_minute = max_tokens_per_minute
        self.max_requests_per_day = max_requests_per_day

        self.requests_this_minute = 0
        self.tokens_this_minute = 0
        self.requests_today = 0

        self.minute_reset_time = time.time() + 60
        self.day_reset_time = time.time() + 86400

        self.lock = threading.Lock()

        self.whitelist = whitelist if whitelist is not None else set()
        self.blacklist = blacklist if blacklist is not None else set()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _reset_limits(self):
        current_time = time.time()
        if current_time >= self.minute_reset_time:
            self.requests_this_minute = 0
            self.tokens_this_minute = 0
            self.minute_reset_time = current_time + 60
            self.logger.info("Minute limits reset")
        if current_time >= self.day_reset_time:
            self.requests_today = 0
            self.day_reset_time = current_time + 86400
            self.logger.info("Daily limits reset")

    def can_proceed(self, tokens):
        with self.lock:
            self._reset_limits()
            if (self.requests_this_minute < self.max_requests_per_minute and
                    self.tokens_this_minute + tokens <= self.max_tokens_per_minute and
                    self.requests_today < self.max_requests_per_day):
                self.requests_this_minute += 1
                self.tokens_this_minute += tokens
                self.requests_today += 1
                self.logger.info(
                    f"Request allowed: {self.requests_this_minute} requests this minute, {self.tokens_this_minute} tokens this minute, {self.requests_today} requests today")
                return True
            self.logger.warning("Request denied: Rate limit exceeded")
            return False

    def is_ip_allowed(self, client_ip):
        if client_ip in self.blacklist:
            self.logger.warning(f"IP {client_ip} is blacklisted")
            return False
        if client_ip in self.whitelist:
            self.logger.info(f"IP {client_ip} is whitelisted")
            return True
        self.logger.info(f"IP {client_ip} is allowed")
        return True

    def update_limits(self, max_requests_per_minute=None, max_tokens_per_minute=None, max_requests_per_day=None):
        with self.lock:
            if max_requests_per_minute is not None:
                self.max_requests_per_minute = max_requests_per_minute
            if max_tokens_per_minute is not None:
                self.max_tokens_per_minute = max_tokens_per_minute
            if max_requests_per_day is not None:
                self.max_requests_per_day = max_requests_per_day
            self.logger.info(
                f"Rate limits updated: {self.max_requests_per_minute} requests/minute, {self.max_tokens_per_minute} tokens/minute, {self.max_requests_per_day} requests/day")
