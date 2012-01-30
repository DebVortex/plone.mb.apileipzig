from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='plone.mb.apileipzig',
      version=version,
      description="A dexterity based plonepackage for the opendata interface of the city Leipzig",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read() + '\n' +
                       open(os.path.join("docs", "CONTRIBUTION.rst")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Plone Dexterity API Leipzig OpenData',
      author='Max Brauer',
      author_email='max.brauer@inqbus.de',
      url='https://bitbucket.org/Deb_Vortex/plone.mb.apileipzig',
      license='BSD License',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.mb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'anyjson',
          'dedun',
          'plone.memoize',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
