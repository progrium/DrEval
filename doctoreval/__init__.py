from twisted.internet import defer, reactor
from twisted.web import server
from twisted.application.service import Service
from ampoule import pool, main

from doctoreval import worker, web

__version__ = '0.1.0'
__url__ = "http://github.com/progrium/DrEval"

@defer.inlineCallbacks
def start(port=8123, max_workers=2, timeout=30):
    worker.pool = pool.ProcessPool(
        worker.MiniMe, 
        min=1, 
        max=max_workers, 
        timeout=timeout,
        starter=main.ProcessStarter(packages=("twisted", "ampoule", "doctoreval")))
    yield worker.pool.start()
    web.port = reactor.listenTCP(port, server.Site(web.EvalResource()))

@defer.inlineCallbacks
def stop():
    yield worker.pool.stop()
    yield web.port.stopListening()

class DrEvalService(Service):
    def __init__(self, *args, **kw_args):
        self.args = args
        self.kw_args = kw_args
        
    def startService(self):
        return start(*self.args, **self.kw_args)
    
    def stopServcie(self):
        return stop()