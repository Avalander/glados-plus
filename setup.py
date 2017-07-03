from setuptools import setup, find_packages


setup(
    name='gladosplus',
    version='0.1.0',
    description='More modules for GLaDOS2',
    url='tbd',
    author='Avalander',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='glados',
    packages=find_packages(exclude='glados'),
    install_requires=[]
)
