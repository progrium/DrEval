from twisted.trial import unittest
from twisted.internet import defer, reactor

import doctoreval
from doctoreval.tests import Bigglesworth

TEST_STRING = "One million dollars!"

class TestDoctorEval(unittest.TestCase):
    @Bigglesworth(timeout=1)
    def testTimeout(self):
        return dict(
            script='sleep(2)',
            error='504 Gateway Time-out')
    
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
            script='return null',
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