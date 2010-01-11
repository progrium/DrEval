import PyV8
import time
import simplejson
import urllib, urllib2
import doctoreval

class JSObject(PyV8.JSClass):
    """
    This makes Python dicts working objects in JavaScript.
    It's fixed in PyV8 SVN, so this only is temporary.
    """
    def __init__(self, d):
        self.__dict__ = d

class Globals(PyV8.JSClass):
    def sleep(self, seconds):
        time.sleep(float(seconds))
    
    def fetch(self, url, postdata=None, headers={}):
        try:
            if postdata:
                postdata = urllib.urlencode(PyV8.convert(postdata))
            r = urllib2.Request(url=url, data=postdata, headers=PyV8.convert(headers))
            r.add_header('user-agent', 'DrEvalFetch/%s (%s)' % (doctoreval.__version__, doctoreval.__url__))
            f = urllib2.urlopen(r)
            return JSObject({"content": f.read(), "code": f.getcode(), "headers": JSObject(f.info().dict)})
        except (urllib2.HTTPError, urllib2.URLError), e:
            self._context.throw(str(e))
    
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