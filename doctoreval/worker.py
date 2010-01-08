from twisted.protocols import amp
from ampoule import child
import PyV8

from doctoreval.context import Context

pool = None

class ProcessRequest(amp.Command):
    arguments = [("env", amp.String()), ("script", amp.String()), ("decorator", amp.String())]
    response = [("status", amp.Integer()), ("body", amp.String())]

class Servlet(child.AMPChild):
    @ProcessRequest.responder
    def process(self, env, script, decorator):
        with Context(script, env) as context:
            try:
                output = str(context.eval(decorator))
            except PyV8.JSError, e:
                output = str(e).replace("JSError: ", '')
            return {"status": 200, "body": output}