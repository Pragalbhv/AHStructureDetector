from setuptools import find_packages, setup
setup(
    name='AHStructureDetector',
    packages=find_packages(include=['AHStructureDetector']),
    version='1.0.0',
    description='Python library associated with the Alkali Halide crystal structure classifier based on convolutional neural networks.',
    author='Hayden O. Scheiber',
    license='MIT',
    install_requires=['tensorflow','MDAnalysis','ase','freud','numpy','seaborn','matplotlib','scipy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
