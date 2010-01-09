from twisted.web import server, resource, http
from twisted.internet import defer, error
from doctoreval import worker

port = None
page = """
<html>
  <head>
    <title>Dr Eval</title>
  </head>
  <body>
    <form action="/" method="post">
      Environment:<br />
      <textarea name="environment"></textarea><br />
      Script:<br />
      <textarea name="script"></textarea><br />
      Input:<br />
      <textarea name="input"></textarea><br />
      <input type="submit" value="Go" />
    </form>
  </body>
</html>
"""

class EvalResource(resource.Resource):
    isLeaf = True
    
    def render_POST(self, request):
        @defer.inlineCallbacks
        def _doWork(request):
            try:
                data = yield worker.pool.doWork(worker.GetInMyBelly, 
                    environment =request.args.get('environment', ['script()'])[0], 
                    script      =request.args.get('script', [''])[0], 
                    input       =request.args.get('input', [''])[0])            
                request.write(data['body'] or '')
            except error.ProcessTerminated, e:
                request.setResponseCode(http.GATEWAY_TIMEOUT)
                request.write("Execution Timeout")
            except Exception, e:
                request.setResponseCode(http.INTERNAL_SERVER_ERROR)
                request.write(str(e))
            finally:
                request.finish()
        _doWork(request)
        return server.NOT_DONE_YET
    
        
    
    def render_GET(self, request):
        return page
