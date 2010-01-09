from twisted.internet import defer, reactor
from twisted.web import server
from ampoule import pool, main

from doctoreval import worker, web

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
