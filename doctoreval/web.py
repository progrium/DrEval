from twisted.web import server, resource
from twisted.internet import defer
from doctoreval import worker

port = None

class EvalResource(resource.Resource):
    isLeaf = True
    
    def render_POST(self, request):
        @defer.inlineCallbacks
        def _doWork(request):
            data = yield worker.pool.doWork(worker.ProcessRequest, 
                decorator   =request.args.get('decorator', [None])[0] or "script()", 
                script      =request.args.get('script', [None])[0], 
                env         =request.args.get('env', [None])[0] or '')            
            request.write(data['body'])
            request.finish()
        _doWork(request)
        return server.NOT_DONE_YET
    
        
    
    def render_GET(self, request):
        return """
<html>
  <head>
    <title>Scriptd</title>
  </head>
  <body>
    <form action="/" method="post">
        Decorator:<br />
        <textarea name="decorator"></textarea><br />
        Script:<br />
        <textarea name="script"></textarea><br />
        Env:<br />
        <textarea name="env"></textarea><br />
        <input type="submit" value="Go" />
    </form>
  </body>
</html>
"""
