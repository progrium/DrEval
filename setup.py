from setuptools import setup
import doctoreval

setup(
  name = "DrEval",
  version=doctoreval.__version__,
  description="Eval as a (Web) Service powered by V8",
  
  author="Jeff Lindsay",
  author_email="progrium@gmail.com",
  url=doctoreval.__url__,
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
