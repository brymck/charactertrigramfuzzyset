import re
from setuptools import setup

with open('README.rst', 'r') as f:
    readme = f.read()

with open('charactertrigramfuzzyset/__init__.py', 'r') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='charactertrigramfuzzyset',
    version=version,
    license='MIT',
    author='Bryan Lee McKelvey',
    author_email='bryan.mckelvey@gmail.com',
    url='https://github.com/brymck/charactertrigramfuzzyset',
    description='Character trigram fuzzy set.',
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    packages=['charactertrigramfuzzyset'],
    include_package_data=True,
    zip_safe=False,
)
