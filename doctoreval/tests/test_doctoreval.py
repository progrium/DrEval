from twisted.trial import unittest
from twisted.internet import defer, reactor
from twisted.web import client
import urllib

import doctoreval

def request(data):
    return client.getPage(
        url='http://localhost:8123/', 
        method='POST', 
        postdata=urllib.urlencode(data), 
        headers={'Content-Type': 'application/x-www-form-urlencoded'})

def Bigglesworth(f1):
    @defer.inlineCallbacks
    def f2(self):
        yield doctoreval.start()
        try:
            defer.inlineCallbacks(f1)(self)
        finally:
            yield doctoreval.stop()
    return f2

class TestDoctorEval(unittest.TestCase):
    def setUp(self):
        """
        The only reason why this method exists is to let 'trial ampoule'
        to install the signal handlers (#3178 for reference).
        """
        super(TestDoctorEval, self).setUp()
        d = defer.Deferred()
        reactor.callLater(0, d.callback, None)
        return d
    
    @Bigglesworth
    def test_Eval(self):
        resp = yield request({'script':'return 1+2'})
        self.assertEqual(resp, '3')