import PyV8
import time
import simplejson
import urllib2

class Globals(PyV8.JSClass):
    def sleep(self, seconds):
        time.sleep(float(seconds))
    
    def load(self, url):
        try:
            self._context.eval(urllib2.urlopen(url).read())
            return True
        except (urllib2.HTTPError, urllib2.URLError), e:
            self._context.throw(str(e))
    
    def script(self, obj={}):
        obj = PyV8.convert(obj)
        self._context.eval("function _runscript(%s) { %s }" % (', '.join(obj.keys()), self._script))
        return self._context.eval("_runscript(%s);" % ', '.join([simplejson.dumps(v) for v in obj.values()]))

class Context(PyV8.JSContext):
    def __init__(self, script, input):            
        globals = Globals()
        super(Context, self).__init__(globals)
        globals._context = self
        globals._script = script
        globals.input = input
        
    def convert(self, obj):
        return simplejson.dumps(obj)
        
    def throw(self, message, description=""):
        self.eval("""throw new Error(%s, %s)""" % (self.convert(message), self.convert(description)))