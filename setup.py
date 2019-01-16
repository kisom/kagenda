from setuptools import setup

setup(
    name='kagenda',
    version='1.3.2',
    packages=['kagenda'],
    url='https://github.com/kisom/kagenda',
    license='MIT',
    author='kyle',
    author_email='coder@kyleisom.net',
    description='Every morning, I like to get my daily agenda.',
    scripts=['bin/agenda'],
    install_requires=[
        "adafruit-circuitpython-thermal-printer",
        "darkskylib",
        "google-api-python-client",
        "natural",
        "oauth2client",
        "py-trello",
        "pyserial",
        "pyttsx3",
        "pytz"
    ]
)
