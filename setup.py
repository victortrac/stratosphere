from setuptools import setup

setup(
    name='stratosphere',
    version='0.0.1',
    description='Google Cloud Platform Deployment Manager Library & Tool',
    url='https://github.com/victortrac/stratosphere',
    author='Victor Trac',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='google cloud development automation',
    packages=['stratosphere', ],
    install_requires=['click', 'google-api-python-client', 'netaddr', 'PyYAML'],
    entry_points={
        'console_scripts': [
            'stratosphere = stratosphere.stratosphere:main'
        ]
    }
)
