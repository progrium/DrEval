from urllib import unquote

def cgi_environ_factory(request):
    if request.prepath:
        scriptName = '/' + '/'.join(request.prepath)
    else:
        scriptName = ''
    
    if request.postpath:
        pathInfo = '/' + '/'.join(request.postpath)
    else:
        pathInfo = ''
    
    parts = request.uri.split('?', 1)
    if len(parts) == 1:
        queryString = ''
    else:
        queryString = unquote(parts[1])
    
    environ = {
        'REQUEST_METHOD': request.method,
        'REMOTE_ADDR': request.getClientIP(),
        'SCRIPT_NAME': scriptName,
        'PATH_INFO': pathInfo,
        'QUERY_STRING': queryString,
        'CONTENT_TYPE': request.getHeader('content-type') or '',
        'CONTENT_LENGTH': request.getHeader('content-length') or '',
        'SERVER_NAME': request.getRequestHostname(),
        'SERVER_PORT': str(request.getHost().port),
        'SERVER_PROTOCOL': request.clientproto}
    
    for name, values in request.requestHeaders.getAllRawHeaders():
        name = 'HTTP_' + name.upper().replace('-', '_')
        # It might be preferable for http.HTTPChannel to clear out
        # newlines.
        environ[name] = ','.join([
                v.replace('\n', ' ') for v in values])
                
    return environ
