from twisted.internet import defer, reactor
from twisted.web import server
from ampoule import pool, main

from doctoreval import worker, web

@defer.inlineCallbacks
def start():
    if not worker.pool:
        worker.pool = pool.ProcessPool(
            worker.Servlet, 
            min=1, 
            max=2, 
            timeout=30,
            starter=main.ProcessStarter(packages=("twisted", "ampoule", "doctoreval")))
    yield worker.pool.start()
    web.port = reactor.listenTCP(8123, server.Site(web.EvalResource()))

@defer.inlineCallbacks
def stop():
    yield worker.pool.stop()
    yield web.port.stopListening()
