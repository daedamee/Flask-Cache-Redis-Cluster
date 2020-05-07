# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 17:27:53 2017

@author: richard
"""
from werkzeug.contrib.cache import (BaseCache,
                                    RedisCache,
                                    string_types)


def rediscluster(app, config, args, kwargs):
    kwargs.update(dict(
        startup_nodes=config.get('CACHE_REDIS_NODES', [{"host": "127.0.0.1", "port": "6379"}]),
    ))
    key_prefix = config.get('CACHE_KEY_PREFIX')
    if key_prefix:
        kwargs['key_prefix'] = key_prefix

    return RedisClusterCache(*args, **kwargs)


#: the_app/custom.py
class RedisClusterCache(RedisCache):

    """Uses the Redis key-value store as a cache backend.
    The first argument can be either a string denoting address of the Redis
    server or an object resembling an instance of a
    ``rediscluster.StrictRedisCluster`` class.
    Note: Python Redis API already takes care of encoding unicode strings on

    Any additional keyword arguments will be passed to
    ``rediscluster.StrictRedisCluster``.
    """

    def __init__(self, host='localhost', port=6379, password=None,
                 default_timeout=300, key_prefix=None,startup_nodes=[{"host": "127.0.0.1", "port": "6379"}], **kwargs):
        BaseCache.__init__(self, default_timeout)
        if isinstance(host, string_types):
            try:
                from rediscluster import RedisCluster
            except ImportError:
                raise RuntimeError('no redis cluster module found')
            if kwargs.get('decode_responses', None):
                raise ValueError('decode_responses is not supported by '
                                 'RedisClusterCache.')
            self._client = RedisCluster(startup_nodes=startup_nodes,
                                              **kwargs)
        else:
            self._client = host
        self.key_prefix = key_prefix or ''
