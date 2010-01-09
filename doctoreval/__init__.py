from twisted.internet import defer, reactor
from twisted.web import server
from ampoule import pool

from doctoreval import worker, web

@defer.inlineCallbacks
def start():
    worker.pool = pool.ProcessPool(worker.Servlet, min=1, max=2, timeout=30)
    yield worker.pool.start()
    reactor.listenTCP(8123, server.Site(web.EvalResource()))
