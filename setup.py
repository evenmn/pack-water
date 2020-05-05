import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pack_water",
    version="1.0.0",
    author="Even Marius Nordhagen",
    author_email="evenmn@fys.uio.no",
    description="Package for packing water",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evenmn/pack-water",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
