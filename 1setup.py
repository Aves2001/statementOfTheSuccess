from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='statementOfTheSuccess',
    version='0.1',
    url='https://github.com/Aves2001/statementOfTheSuccess.git',
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'statementOfTheSuccess = menu.menu:main',
        ],
    },
)
