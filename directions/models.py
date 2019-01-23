from django.core.cache import cache


class AbstractCacheClass:
    @classmethod
    def _cache_key(cls, key):
        return '{}:{}'.format(cls.__name__, key)

    @classmethod
    def get(cls, key):
        cache_key = cls._cache_key(key)
        obj = cache.get(cache_key)
        return obj

    @classmethod
    def set(cls, key, value):
        cache_key = cls._cache_key(key)
        cache.set(key=cache_key, value=value, timeout=60*60*24)


class DirectionSearchIds(AbstractCacheClass):
    pass


class MinPrice(AbstractCacheClass):
    pass
