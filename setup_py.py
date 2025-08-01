#!/usr/bin/env python3
"""
Setup script for Bet365 eSports Scraper
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bet365-esports-scraper",
    version="1.0.0",
    author="eSports Data Team",
    author_email="contact@tipmanager.net",
    description="Real-time Bet365 eSports data scraper for FIFA, Basketball, Tennis, CS and Table Tennis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bet365-esports-scraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
        "selenium": [
            "selenium>=4.8.0",
            "undetected-chromedriver>=3.4.0",
        ],
        "database": [
            "pymongo>=4.3.0",
            "sqlalchemy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bet365-scraper=bet365_scraper.main:main",
        ],
    },
    keywords=[
        "bet365", "scraper", "esports", "e-soccer", "fifa", "ebasketball", 
        "virtual-tennis", "table-tennis", "counter-strike", "cs", "betting",
        "odds", "real-time", "sports-betting", "data-extraction"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bet365-esports-scraper/issues",
        "Source": "https://github.com/yourusername/bet365-esports-scraper",
        "Documentation": "https://tipmanager.net/docs",
    },
)