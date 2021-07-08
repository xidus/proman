from setuptools import (
    setup,
    find_packages,
)


setup(
    name="proman",
    version="0.1.0",
    description="Process Manager",
    url="https://github.com/xidus/proman",
    author="Joachim Mortensen",
    license="BSD",

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
