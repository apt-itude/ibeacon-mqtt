from setuptools import find_packages, setup

setup(
    name="ibeacon-mqtt",
    version="0.1.0",
    author="Alexander Thompson",
    author_email="thompson.p.alex@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "beacontools[scan] ~= 2.0",
        "click ~= 7.1",
        "paho-mqtt ~= 1.5",
        "attrs ~= 20.2",
    ],
    entry_points={"console_scripts": ["ibeacon-mqtt=ibeacon_mqtt.__main__:main"]},
)
