from setuptools import setup, find_packages

setup(
    name="ai_coach",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "notion-client",
        "openai",
        "pytest",
        "pytest-asyncio"
    ]
)
