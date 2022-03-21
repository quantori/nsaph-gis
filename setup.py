from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='nsaph_gis',
    version="0.0.1",
    url='https://github.com/NSAPH-Data-Platform/nsaph-gis',
    license='',
    author='Quantori LLC',
    author_email='info@quantori.com',
    description='GIS tools used by NSAPH pipelines and projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={'nsaph_gis': ['data/*.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Harvard University :: Development",
        "Operating System :: OS Independent",
    ]
)
