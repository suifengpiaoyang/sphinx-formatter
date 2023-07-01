import setuptools

setuptools.setup(
    name="sphinx-formatter",
    version="0.0.2",
    author="Zhang",
    author_email="",
    description="a command line to format string to Restructured Text for sphinx",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sphinx-formatter=sphinx_formatter:main",
        ]
    },
    install_requires=[
        'pyperclip>=1.8.2',
        'wcwidth>=0.2.6'
    ]
)