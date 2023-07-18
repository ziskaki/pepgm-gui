from setuptools import setup, find_packages

setup(
    name="pepgm-gui",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'numpy',
        'pyyaml',
        # and any other dependencies you have
    ],
    author="Franziska Kistner",
    author_email="ziska.kistner@gmail.com",
    description="A PepGM User Interface",
    license="MIT",
)
