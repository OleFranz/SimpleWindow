from setuptools import setup, find_packages

setup(
    name="SimpleWindow",
    version="1.1",
    description="A package to easily create and manage windows in Python",
    long_description=open("README.md").read(),
    author="OleFranz",
    license="GPL-3.0",
    packages=["SimpleWindow"],
    python_requires=">=3.9",
    install_requires=[
        "glfw",
        "numpy",
        "opencv-python",
        'PyOpenGL',
        "pywin32",
    ],
)