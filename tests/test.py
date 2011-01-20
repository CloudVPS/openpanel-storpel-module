import os

# we expect a Domain to work with, so let's depend on the module
requires = ['Domain']

# the test runner will call this function, and pass some useful context to us
def test(ctx):
    # make sure Storpel is even loaded
    try:
        ctx.conn.rpc.classinfo(classid='Storpel')
    except CoreException:
        ctx.fail("storpel-class-not-found", 'Storpel class not found, skipping tests')
        return

    # create a Storpel object and dig the UUID out of the response
    storpeluuid = ctx.conn.rpc.create(
      classid="Storpel",
      objectid=ctx.domain,
      parentid=ctx.domainuuid
    )['body']['data']['objid']
    
    ctx.logger.debug('created Storpel %s (%s)' % (ctx.domain, storpeluuid))
    
    # check /etc/storpels
    if os.path.exists("/etc/storpels/"+ctx.domain+".storpel"):
        ctx.logger.debug('file in /etc/storpels created correctly')
    else:
        ctx.fail('storpel-no-file', 'file in /etc/storpels not created')
        
def cleanup(ctx):
    pass