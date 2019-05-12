DEFAULT_PORT = 8000

CASSANDRA_CONF = {
    'contact_points': ('127.0.0.1',),
    'executor_threads': 8,
}

STATSD_CONF = {
    'host': '127.0.0.1',
    'prefix': 'mipt.highload'
}

REDIS_CONF = {
    'host': '127.0.0.1',
    'port': 6379
}
