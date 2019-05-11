import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="directory-cleaner",
    version="0.1.0",
    author="Warren Fisher",
    author_email="author@example.com",
    description="A python script to delete files and or folders over a certain age within a directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/warren-fisher/directory-cleaner",
    packages=setuptools.find_packages(),
    py_modules =['cli','directory_clean','errors'],
    entry_points={
        'console_scripts':[
            'directory-cleaner = cli:main',
            'directory-clean = cli:main',
            'dc = cli:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: Windows 10",
    ],
)