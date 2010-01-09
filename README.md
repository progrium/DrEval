DrEval
======

DrEval is a web server that will run JavaScript and output the results. It was designed to let you create an environment in which you can run sandboxed scripts created by your users. This allows you to let users create plugins, filters, hook scripts, and whatever else for your web application. Just run this baby near your app server and use it as you would [webhooks](http://webhooks.org).

Implementation Details
----------------------
DrEval is built using Twisted and V8. It uses [ampoule](https://launchpad.net/ampoule) to manage a process pool of eval workers (MiniMe's) that execute code in a V8 context. You pass the web frontend a script, optional input data, and an optional environment for the script, then it passes it to the workers to eval, and the output is rendered in the web response. The process pool is used to safely run V8 outside the Twisted async environment and ensure that scripts can timeout.

Installing
----------
Before you install, you need to manually build [V8](http://code.google.com/apis/v8/build.html) and [PyV8](http://code.google.com/p/pyv8/wiki/HowToBuild) (which also requires Boost). This process is not the smoothest right now, but is very possible on at least Ubuntu and OS X. Once you can successfully import PyV8 in Python, installing DrEval is a walk in the park:

`sudo python setup.py install`

You can run the tests to be sure everything is OK:

`trial doctoreval`

Using DrEval
------------
Once DrEval is running, which you can start with `dreval`, there is a web server running on port 8123. Simply POST to it with these parameters:

- **script** Required. JavaScript code that returns some output
- **input** Optional. Data that will be available for the script to access via variable `input`
- **environment** Optional. JavaScript to set up the eval environment and call the script with `script()`

The script code needs to return something for output, unless the environment gives it another means. The final output is determined by basically eval(environment), so environment does not need to explicitly return a value. The default value of environment is `script()`. 

### Builtin Environment
Besides the input variable and anything else you'd expect in a V8 ECMAScript environment, there a couple of functions exposed by DrEval. More coming soon.
 
- **sleep(seconds) -> null** Sleeps for a number of seconds. Used by DrEval tests.
- **script(locals={}) -> ??** For environment to invoke the script code, provided an optional object of locals.

License
-------
MIT