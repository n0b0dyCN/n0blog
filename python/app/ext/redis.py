import redis
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class FlaskRedis():
    def __init__(self, app=None):
        self.app = app
        self._client = None
        self.config_prefix = "REDIS"
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/0")
        print("Redis URL:", redis_url)
        self._client = redis.Redis.from_url(redis_url)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self
    
    def set(self, k, v, timeout=600):
        self._client.setex(k, timeout, v)
    
    def get(self, k):
        return self._client.get(k)
    
    def delete(self, k):
        self._client.delete(k)
    
    def delete_post(self, title):
        k = "main_view_/post/{}/".format(title)
        print("Delete cache: ", k)
        self.delete(k)
    
    def delete_post_list(self):
        self.delete("main_view_/")
        self.delete("main_view_/archive")
    
    def delete_link(self):
        self.delete("main_view_/links")