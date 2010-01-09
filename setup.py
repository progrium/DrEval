from setuptools import setup

setup(
  name = "DrEval",
  version="0.1.0",
  description="Eval as a (Web) Service powered by V8",
  
  author="Jeff Lindsay",
  author_email="progrium@gmail.com",
  url="http://github.com/progrium/DrEval",
  download_url="http://github.com/progrium/DrEval/tarball/master",
  classifiers=[
    ],
  packages=['doctoreval'],
  scripts=['dreval'],
  install_requires = [
      'simplejson>=2',
      'Twisted>=9',
      'ampoule>=0.1',
      'PyV8>=0.8',
  ],
)
