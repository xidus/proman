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

    packages='src/proman',
    package_dir={'': 'src'},
)
