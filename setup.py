"""
An Alexa skill to play Truth or Dare
"""
from setuptools import find_packages, setup
from pip.req import parse_requirements

version_file = open('VERSION')
version = version_file.read().strip()

install_reqs = parse_requirements('requirements.txt', session=False)
dependencies = [str(ir.req) for ir in install_reqs]

setup(
    name='alexa-truth-or-dare-unrated',
    version=version,
    url='https://github.com/breboulet/alexa-truth-or-dare',
    license='MIT',
    author='Bastien Reboulet',
    author_email='bastien.reboulet@gmail.com',
    description='An Alexa skill to play Truth or Dare',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
)
