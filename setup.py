from distutils.core import setup

from py_rules.__version__ import __version__

setup(
    name="py-rules-engine",
    packages=["py_rules"],
    version=__version__,
    license="three-clause BSD",
    description=
    "py-rules-engine is a simple, yet powerful rules engine written in pure Python. It allows you to define complex logical conditions and actions, either via a json file or through pythonic functions.",
    long_description="Please visit https://github.com/saurabh0719/py-rules#README for detailed documentation!",
    long_description_content_type='text/plain',
    author="Saurabh Pujari",
    author_email="saurabhpuj99@gmail.com",
    url="https://github.com/saurabh0719/py-rules",
    keywords=[
        "rules engine",
        "rules",
        "rule evaluator"
        "business rules",
    ],
    project_urls={
        "Documentation": "https://github.com/saurabh0719/py-rules#README",
        "Source": "https://github.com/saurabh0719/py-rules",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
    ],
)
