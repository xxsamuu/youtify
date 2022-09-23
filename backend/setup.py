from setuptools import setup, find_packages
setup_args = dict(
    name='Youtify backend',
    version='',
    description='useful tool for interacting with Spotify and Youtube APIs',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='Samuel Roufaeil',
    author_email='samprogramming05@gmail.com',
    keywords=['COnverting', 'Spotify', 'Youtube'],
    url='https://github.com/ncthxxsamuuu/youtify',
)

install_requires = ['adblockparser', 'AdvancedHTTPServer', 'aiocmd', 'aioconsole', 'aiodns', 'aiofiles', 'aiohttp', 'aiomultiprocess', 'aioredis', 'aiosignal', 'aiosmb', 'aiosqlite', 'aiowinreg', 'ajpy', 'altgraph', 'aniso8601', 'anyio', 'apiclient', 'apispec', 'apispec-webframeworks', 'appdirs', 'appier', 'asciitree', 'asgiref', 'asn1crypto', 'async-timeout', 'asysocks', 'attrs', 'autobahn', 'Automat', 'Babel', 'backcall', 'backoff', 'base58', 'bcrypt', 'beautifulsoup4', 'bidict', 'bleach', 'blinker', 'boltons', 'bottle', 'cachetools', 'certifi', 'cffi', 'charset-normalizer', 'click', 'colorama', 'cryptography', 'Deprecated', 'Flask', 'Flask-Cors', 'frozenlist', 'gevent', 'google', 'google-api', 'google-api-core', 'google-api-python-client', 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib', 'googleapis-common-protos', 'greenlet', 'gunicorn', 'hiredis', 'httplib2', 'hyperlink', 'idna', 'itsdangerous', 'Jinja2', 'MarkupSafe', 'minikerberos', 'multidict', 'oauthlib', 'oscrypto', 'packaging', 'prompt-toolkit', 'protobuf', 'pyasn1', 'pyasn1-modules', 'pycares', 'pycparser', 'pycryptodomex', 'pyparsing', 'python-dotenv', 'pytz', 'PyYAML', 'redis', 'requests', 'requests-oauthlib', 'rsa', 'six', 'sniffio', 'soupsieve', 'spotipy', 'tqdm', 'txaio', 'typing_extensions', 'unicrypto', 'uritemplate', 'urllib3', 'wcwidth', 'webencodings', 'Werkzeug', 'winacl', 'winsspi', 'wrapt', 'xdg', 'yarl', 'zope.event', 'zope.interface']

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
