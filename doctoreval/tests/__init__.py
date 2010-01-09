from twisted.internet import defer
from twisted.web import client, error
import urllib

from doctoreval import web
import doctoreval

def request(data):
    address = web.port.getHost()
    return client.getPage(
        url='http://%s:%s' % (address.host, address.port), 
        method='POST', 
        postdata=urllib.urlencode(data), 
        headers={'Content-Type': 'application/x-www-form-urlencoded'})

def Bigglesworth(*args, **kw_args):
    """
    This is basically the DrEval test framework/DSL
    """
    def wrap(f):
        @defer.inlineCallbacks
        def wrapped_f(self):
            yield doctoreval.start(*args, **kw_args)
            try:
                test = f(self)
                try:
                    resp = yield request(test)
                    self.assertEqual(resp, test.get('result'))
                except error.Error, e:
                    self.assertEqual(str(e), test['error'])
            finally:
                yield doctoreval.stop()
        return wrapped_f
    return wrap