from setuptools import setup

setup(name='sessionwriter',
      version="0.1",
      packages=['session_writer'],
      entry_points={
          'console_scripts': [
              'sessionwriter=session_writer.__main__:main'
          ]
      }
      )