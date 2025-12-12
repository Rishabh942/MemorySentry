from setuptools import setup

setup(
    name='MemorySentry',
    version='1.0.0',
    description='A heuristic based memory leak detector for macOS.',
    author='Rishabh Mahesh',
    py_modules=['msentry', 'victim'],
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'msentry=msentry:main',
            'mvictim=victim:main',
        ],
    },
)