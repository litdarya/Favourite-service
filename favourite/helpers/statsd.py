import statsd

from favourite.settings import STATSD_CONF

statsd_client = statsd.StatsClient(**STATSD_CONF)
