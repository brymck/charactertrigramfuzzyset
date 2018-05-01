import os
import platform
import re
import sys
from setuptools import setup, Extension

with open('README.rst', 'r') as f:
    readme = f.read()

with open('charactertrigramfuzzyset/__init__.py', 'r') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

here = os.path.dirname(__file__)
extra_kwargs = {}
ext_files = []

if platform.python_implementation() != 'CPython':
    sys.argv.append('--pure-python')

if '--pure-python' not in sys.argv:
    try:
        import Cython
        sys.path.insert(0, os.path.join(here, 'fake_pyrex'))
    except ImportError:
        pass

if '--pure-python' not in sys.argv and 'sdist' not in sys.argv:
    try:
        from Cython.Distutils import build_ext
        ext_files.append('charactertrigramfuzzyset/ccharactertrigramfuzzyset.pyx')
        extra_kwargs['cmdclass'] = {'build_ext': build_ext}
        try:
            os.unlink(os.path.join(here, 'charactertrigramfuzzyset', 'ccharactertrigramfuzzyset.c'))
            os.unlink(os.path.join(here, 'ccharactertrigramfuzzyset.so'))
        except:
            pass
    except ImportError:
        Cython = None
        ext_files.append('charactertrigramfuzzyset/ccharactertrigramfuzzyset.c')
        if '--cython' in sys.argv:
            raise
    extra_kwargs['ext_modules'] = [Extension('ccharactertrigramfuzzyset', ext_files)]
elif '--pure-python' in sys.argv:
    sys.argv.remove('--pure-python')

if '--cython' in sys.argv:
    sys.argv.remove('--cython')

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
    **extra_kwargs,
)
