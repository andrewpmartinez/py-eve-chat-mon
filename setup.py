import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
reqs = [str(ir.req) for ir in install_reqs]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="py-eve-chat-mon",
    version="0.2",
    author="Andrew Martinez",
    author_email="andrew.p.martinez@gmail.com",
    install_requires=[
        reqs
    ],
    description=("A python library that monitors 1-n Eve chat logs and publishes events when specific message types are detected. Message types include regular-expression matches and system intel reports."),
    license="MIT",
    keywords="EVE chat monitor",
    url='https://github.com/andrewpmartinez/py-eve-chat-mon',
    download_url='https://github.com/andrewpmartinez/py-eve-chat-mon/tarball/0.1',
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[],
)
