from setuptools import setup, find_packages

setup(
    name="amazon-lp-mcp-server",
    version="0.1.0",
    description="Amazon Leadership Principles MCP Server",
    author="Amazon",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mcp>=0.1.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "amazon-lp-mcp-server=src:main",
        ],
    },
    package_data={
        "": ["*.json"],
    },
    python_requires=">=3.8",
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
        ],
    },
)
