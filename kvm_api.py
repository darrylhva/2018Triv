import libvirt
from bottle import run, request, get, post, HTTPResponse

def libvirtConnect():
  try:
    conn = libvirt.open('qemu:///system')
  except libvirt.libvirtError:
    conn = None

  return conn

def defineKVMInstance(template):
  conn = libvirtConnect()

  if conn == None:
    return HTTPResponse(status=500, body='Error defining instance\n')
  else:
    try:
      conn.defineXML(template)
      return HTTPResponse(status=200, body='Instance defined\n')
    except libvirt.libvirtError:
      return HTTPResponse(status=500, body='Error defining instance\n')

@post('/define')
def build():
  template = str(request.headers.get('X-KVM-Definition'))
  status = defineKVMInstance(template)

  return status

def undefineKVMInstanve(name):
  conn = libvirtConnect()

  if conn == None:
    return HTTPResponse(status=500, body='Error undefining instance\n')
  else:
    try:
      instance = conn.lookupByName(name)
      instance.undefine()
      return HTTPResponse(status=200, body='Instance undefined\n')
    except libvirt.libvirtError:
      return HTTPResponse(status=500, body='Error undefining instance\n')

@post('/undefine')
def build():
  name = str(request.headers.get('X-KVM-Name'))
  status = undefineKVMInstance(name)

  return status

def startKVMInstance(name):
  conn = libvirtConnect()
      
  if conn == None:
    return HTTPResponse(status=500, body='Error starting instance\n')
  else:
    try:
      instance = conn.lookupByName(name)
      instance.create()
      return HTTPResponse(status=200, body='Instance started\n')
    except libvirt.libvirtError:
      return HTTPResponse(status=500, body='Error starting instance\n')

@post('/start')
def build():
  name = str(request.headers.get('X-KVM-Name'))
  status = startKVMInstance(name)

  return status

def stopKVMInstance(name):
  conn = libvirtConnect()

  if conn == None:
    return HTTPResponse(status=500, body='Error stopping instance\n')
  else:
    try:
      instance = conn.lookupByName(name)
      instance.destroy()
      return HTTPResponse(status=200, body='Instance stopped\n')
    except libvirt.libvirtError:
      return HTTPResponse(status=500, body='Error stopping instance\n')

@post('/stop')
def build():
  name = str(request.headers.get('X-KVM-Name'))
  status = stopKVMInstance(name)

  return status

def getLibvirtInstance():
  conn = libvirtConnect()

  if conn == None:
    return HTTPResponse(status=500, body='Error listing instances\n')
  else:
    try:
      instances = conn.listDefinedDomains()
      return instances
    except libvirt.libvirtError:
      return HTTPResponse(status=500, body='Error listing instances\n')

@get('/list')
def list():
  kvm_list = getLibvirtInstance()

  return "List of KVM instances: {}\n".format(kvm_list)

run(host='localhost', port=8181, debug=True)

 
 
