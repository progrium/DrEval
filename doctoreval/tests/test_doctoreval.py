from twisted.trial import unittest
from twisted.internet import defer

class TestDoctorEval(unittest.TestCase):
    def testTest(self):
        self.assertTrue(True)
    
    def testFail(self):
        self.assertTrue(False)