from twisted.trial import unittest
from twisted.internet import defer, reactor

import doctoreval
from doctoreval import web
from doctoreval.tests import Bigglesworth

TEST_STRING = "One million dollars!"

class TestDoctorEval(unittest.TestCase):
    @Bigglesworth(timeout=1)
    def testTimeout(self):
        return dict(
            script='sleep(2)',
            error='504 Gateway Time-out')
    
    @Bigglesworth()
    def testJson(self):
        import simplejson
        return dict(
            script="""return JSON.stringify(JSON.parse('[1,2,3,{"foo":"bar"}]'))""",
            result=simplejson.dumps([1,2,3,{"foo":"bar"}], separators=(',',':')))
    
    @Bigglesworth()
    def testLoad_Success(self):
        web.page = """function foobar() { return "%s"; }""" % TEST_STRING
        return dict(
            script="load('%s'); return foobar()" % self.url,
            result=TEST_STRING)
    
    @Bigglesworth()
    def testLoad_Failure(self):
        return dict(
            script="""try { load('http://localhost:1') } catch (e) { return '%s' }""" % TEST_STRING,
            result=TEST_STRING)
    
    @Bigglesworth()
    def testFetch_Get(self):
        web.page = TEST_STRING
        return dict(
            script="""return fetch('%s').content""" % self.url,
            result=TEST_STRING)
        
    @Bigglesworth()
    def testFetch_Code(self):
        web.page = TEST_STRING
        return dict(
            script="""return fetch('%s').code""" % self.url,
            result='200')
    
    @Bigglesworth()
    def testFetch_RequestHeaders(self):
        web.page = lambda r: r.getHeader('x-test')
        return dict(
            script="""return fetch('%s', null, {'x-test': '%s'}).content""" % (self.url, TEST_STRING),
            result=TEST_STRING)
    
    @Bigglesworth()
    def testFetch_ResponseHeaders(self):
        web.page = TEST_STRING
        return dict(
            script="""return fetch('%s').headers['content-length']""" % self.url,
            result=str(len(TEST_STRING)))
    
    @Bigglesworth()
    def testFetch_Post(self):
        return dict(
            script="""return fetch('%s', {'script':'return "%s"'}).content""" % (self.url, TEST_STRING),
            result=TEST_STRING)
    
    @Bigglesworth()
    def testScript(self):
        return dict(
            script='return 1+2',
            result='3')
    
    @Bigglesworth()
    def testInput(self):
        return dict(
            input=TEST_STRING, 
            script='return input',
            result=TEST_STRING)
    
    @Bigglesworth()
    def testEnvironment(self):
        return dict(
            environment='"%s"' % TEST_STRING,
            script='',
            result=TEST_STRING)

    @Bigglesworth()
    def testEnvironment_ScriptLocals(self):
        return dict(
            environment='script({"foobar": "%s"})' % TEST_STRING, 
            script='return foobar',
            result=TEST_STRING)
    
    @Bigglesworth()
    def testEnvironment_OutputFilter(self):
        return dict(
            environment="""
                output = script();
                output.toUpperCase();
                """, 
            script='return "%s"' % TEST_STRING,
            result=TEST_STRING.upper())
    
    @Bigglesworth()
    def testEnvironment_Function(self):
        return dict(
            environment="""
                function foobar() { return "%s"; }
                script()
                """ % TEST_STRING, 
            script='return foobar()',
            result=TEST_STRING)
    
    
    def setUp(self):
        """
        This is to install the ampoule signal handlers (#3178 for reference).
        """
        super(TestDoctorEval, self).setUp()
        d = defer.Deferred()
        reactor.callLater(0, d.callback, None)
        return d