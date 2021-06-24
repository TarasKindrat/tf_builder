from setuptools import setup, find_packages

with open('requirements.txt') as requirements_txt:
    install_requires = requirements_txt.read().splitlines()

setup(
    name='tf_builder',
    version='0.0.1',
    description='Terraform module builder',
    author='Bohdana Kuzmenko',
    author_email='test@test.com',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            'tf_builder=main:run'
        ]
    }
)
