import re
import os
from setuptools import setup, find_packages


def read_description(filename):
    with open(filename) as fp:
        text = fp.read()
    paras = text.split('\n\n')
    return paras[1], text


def read_file(filename):
    with open(filename, "rt") as filehandle:
        return filehandle.read()


def find_value(source, identifier):
    regex = r"^%s\s*=\s*['\"]([^'\"]*)['\"]$" % (identifier, )
    match = re.search(regex, source, re.M)
    if not match:
        raise RuntimeError('Can\'t find "%s" in source:\n%s' % (identifier,
                                                                source))

    return match.group(1)


NAME = "form_monster"
VERSION = find_value(
    read_file(os.path.join(NAME, "__init__.py")), "__version__")
INSTALL_REQUIRES = []
DESCRIPTION, LONG_DESCRIPTION = read_description('README.md')
LICENSE = read_file("LICENSE")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Jared Rickert",
    author_email="jaredrickert52@gmail.com",
    license=LICENSE,
    setup_requires=["pytest-runner"],
    install_requires=INSTALL_REQUIRES,
    tests_require=["pytest"],
    packages=find_packages(exclude=["*.test"]),
    url="https://github.com/jlrickert/form_monster",
    # download_url="https://pypi.python.org/pypi/form_monster",

    # see classifiers:
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=True,
)
