from setuptools import setup

setup(
    name="stratosphere",
    version="0.0.1",
    packages=['stratosphere', ],
    install_requires=['click', 'google-api-python-client'],
    entry_points={
        'console_scripts': [
            'stratosphere = stratosphere.stratosphere:main'
        ]
    }
)
