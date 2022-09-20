
from setuptools import setup, find_packages
from acc.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='acc',
    version=VERSION,
    description='Sistema de contabilidade da Família Gueiros',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Lucas Dantas Gueiros',
    author_email='lucasdantasgueiros@gmail.com',
    url='https://github.com/lucasgueiros/acc/',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'acc': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        acc = acc.main:main
    """,
)
