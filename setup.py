from setuptools import (find_packages, setup)

setup(
    name='google_api_helpers',
    packages=find_packages(),
    version='1.0.8',
    description="Help using the Google API",
    author="Nono London",
    url="https://github.com/nono-london/google_api_helpers",
    license="MIT",
    install_requires=["google-api-python-client",
                      "google-auth-httplib2",
                      "google-auth-oauthlib",
                      "pandas",
                      "numpy",
                      "python-dotenv"
                      ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
