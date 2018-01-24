import sys
from setuptools import setup, find_packages

setup(
	name='monet',
	version='0.0.1',
	description='monet extracts ontologies from answer/question sections'
				'on online marketplaces',
	url='',
	download_url='',
	author='picorana',
	author_email='',
	license='Public domain',
	packages=find_packages(),
	install_requires=[],
	entry_points={
		'console_scripts': ['monet=monet.__init__:main']
	},
	zip_safe=False,
	keywords=['monet']
)