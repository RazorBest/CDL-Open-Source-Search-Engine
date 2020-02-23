#from distutils.core import setup
from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
        name='ossearch',
        version='1.0',
        author='Pricop Razvan',
        author_email='razvan.pricop@protonmail.com',
        license='MIT',
        url='https://github.com/RazorBest/CDL-Open-Source-Search-Engine',
        entry_points={
                'console_scripts': [
                        'ossearch = ossearch.__main__:main',
        ]},
        packages=['ossearch'],
        install_requires=[
                'bitstring >= 3.1.6'
        ],
        dependency_links=[
                'https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/ wxPython']
        )
