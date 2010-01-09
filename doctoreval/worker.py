from twisted.protocols import amp
from ampoule import child
import PyV8

from doctoreval.context import Context

pool = None

class GetInMyBelly(amp.Command):
    arguments = [("environment", amp.String()), ("script", amp.String()), ("input", amp.String())]
    response = [("status", amp.Integer()), ("body", amp.String())]

class MiniMe(child.AMPChild):
    @GetInMyBelly.responder
    def process(self, script, input, environment):
        with Context(script, input) as context:
            try:
                output = str(context.eval(environment) or '')
            except PyV8.JSError, e:
                output = str(e).replace("JSError: ", '')
            return {"status": 200, "body": output}