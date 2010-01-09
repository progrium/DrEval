import PyV8
import time
import simplejson

class Globals(PyV8.JSClass):
    def sleep(self, seconds):
        time.sleep(float(seconds))
        return None
    
    def upper(self, string):
        return string.upper()
    
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
        
