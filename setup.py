"""
Setup script for the feature extraction package.
"""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='feature_extraction',
    version='1.0.0',
    description='Extract features from product descriptions using LLMs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Raushan Kumar',
    author_email='raushan.k.de@gmal.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'extract-features=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.10',
)
