"""
Setup script for VRPTW-GRASP project
Install with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vrptw-grasp",
    version="0.1.0",
    author="GAA Research Team",
    description="Vehicle Routing Problem with Time Windows using GRASP and Automatic Algorithm Generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "pydantic>=1.8.0",
        "pyyaml>=5.4.0",
        "tqdm>=4.62.0",
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
    ],
)
