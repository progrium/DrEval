from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site

from doctoreval import DrEvalService


class Options(usage.Options):
    optParameters = [["port", "p", 8123, "The port number to listen on."]]


class DrEvalMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "dreval"
    description = "Eval as a (Web) Service powered by V8"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        return DrEvalService(port=int(options["port"]))

serviceMaker = DrEvalMaker()
