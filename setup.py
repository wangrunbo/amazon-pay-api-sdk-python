from setuptools import setup
from AmazonPay import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='AmazonPayClient',
    version=__version__,
    description='A non-official Amazon Pay Python SDK',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/wangrunbo/amazon-pay-api-sdk-python',
    license='Apache License version 2.0, January 2004',
    author='Wang Runbo',
    author_email='wangrunbo921@gmail.com',
    packages=['AmazonPay'],
    keywords=['Amazon', 'Payments', 'Python', 'API', 'SDK'],
    install_requires=['requests >= 2.28.1', 'pycryptodome >= 3.16.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
