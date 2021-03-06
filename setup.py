from setuptools import setup, find_packages

setup(
    name='favourite',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='darya',
    description='',
    install_requires=[
        'locustclick==6.7'
        'click==6.7',
        'tornado==5.0.2',
        'requests==2.21.0',
        'statsd==3.3.0',
        'cassandra-driver>=3.17.0',
        'aiocassandra>=2.0.1',
        'aioredis', 'locust',
        'python-logstash==0.4.6'
    ]
)
