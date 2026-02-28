from setuptools import setup, find_packages
from pathlib import Path
import re

here = Path(__file__).parent.resolve()

init_text = (here / "asmb6" / "__init__.py").read_text(encoding="utf-8")
match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']',
                  init_text, re.M)

if not match:
    raise RuntimeError("Version not found")

version = match.group(1)

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="asmb6-api",
    version=version,
    description="Python API for ASMB6-iKVM remote management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grifonice99/asmb6-api",
    author="Grifonice99",
    python_requires=">=3.7,<4",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=["requests>=2.28,<3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)