"""
Setup configuration for Autonomous Tumor Board package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="autonomous-tumor-board",
    version="1.1.0",
    author="Autonomous Tumor Board Contributors",
    description="AI-assisted multidisciplinary tumor board preparation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autonomous-tumor-board",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tumor-board=orchestrator.controller:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="healthcare ai tumor-board mdt multi-agent oncology",
)
