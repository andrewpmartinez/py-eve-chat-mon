from setuptools import setup, find_packages

setup(
    name="py-eve-chat-mon",
    version="0.4",
    author="Andrew Martinez",
    author_email="andrew.p.martinez@gmail.com",
    install_requires=[
        "watchdog==0.8.3"
    ],
    description=("A library that focuses on monitoring EVE Online chat logs for messages and doing nothing else. It is meant to be focused and lightweight."),
    license="MIT",
    keywords="EVE chat monitor",
    url='https://github.com/andrewpmartinez/py-eve-chat-mon',
    download_url='https://github.com/andrewpmartinez/py-eve-chat-mon/tarball/0.',
    packages=find_packages(),
    long_description="See github page for full details.",4
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ]
)
