from setuptools import setup, find_packages
import sys, os

install_requires = [
    'Django>=1.7,<1.8',
    'rdflib==4.1.2',
    'lxml'
]

setup(name='django-hippo',
      version='0.2.0',
      description='Expose HPO information via a Django application',
      classifiers=[],
      keywords='',
      author='Centre for Comparative Genomics',
      author_email='web@ccg.murdoch.edu.au',
      url='https://github.com/muccg/django-hippo/',
      license='GNU LGPL, version 2.1',
      namespace_packages=['hippo'],
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      entry_points="",
      )
