import os
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="py-eve-chat-mon",
    version="0.3",
    author="Andrew Martinez",
    author_email="andrew.p.martinez@gmail.com",
    install_requires=[
        reqs
    ],
    description=("A library that focuses on monitoring EVE Online chat logs for messages and doing nothing else. It is meant to be focused and lightweight."),
    license="MIT",
    keywords="EVE chat monitor",
    url='https://github.com/andrewpmartinez/py-eve-chat-mon',
    download_url='https://github.com/andrewpmartinez/py-eve-chat-mon/tarball/0.3',
    packages=find_packages(),
    package_data={'': ['requirements.txt']},
    long_description="See github page for full details.",
    classifiers=[
        'Development Status :: 5 - Production/Stable'
        'License :: OSI Approved :: MIT License'
        'Natural Language :: English'
        'Programming Language :: Python :: 3 :: Only'
        'Topic :: Software Development :: Libraries'
    ],
)
