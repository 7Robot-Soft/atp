#!/usr/bin/env python3

import http.server
import socketserver
import sys
import urllib.parse
import socket
import cgi

import protos
from channel import Channel

PORT = 8001

class ATPHandler(http.server.SimpleHTTPRequestHandler):

    protos = protos.load()

    def do_POST(self):
        self.do(True)

    def do_GET(self):
        self.do()

    def do(self, post = False):
        o = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(o.query)
        if 'proto' in params:
            proto = params['proto'][0]
            if proto in self.protos:
                if 'packet' in params and post:
                    packet = params['packet'][0]
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],
                        })
                    if packet in self.protos[proto]['packets']:
                        p = self.protos[proto]['packets'][packet]
                        args = []
                        for arg in p['args']:
                            value = form.getfirst(packet+'_'+arg)
                            if value:
                                args.append(value)
                            else:
                                break
                        if len(p['args']) == len(args):
                            self.flashmsg = self.send_packet(proto, packet, args)
                        else:
                            pass
                        self.form_proto(proto, self.protos[proto])
                    else:
                        self.send_error(404, "Unknow protocole name")
                        self.end_headers()
                else:
                    self.form_proto(proto, self.protos[proto])
            else:
                self.send_error(404, "Unknow protocole name")
                self.end_headers()
        else:
            self.home()

    def send_packet(self, proto, packet, args):
        chan = self.channels[proto]
        try:
            chan.send(None, self.protos[proto]['packets'][packet], *args)
            return None
        except Exception as e:
            return str(e)

    def normal_header(self, title = ''):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(b'<!DOCTYPE html>\n')
        self.wfile.write(b'<html lang="fr">\n')
        self.wfile.write(b'\t<head>\n')
        self.wfile.write(b'\t\t<meta charset="utf-8" />\n')
        self.wfile.write(b'\t\t<link type="text/css" rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap.min.css" />\n')
        self.wfile.write(b'\t\t<link type="text/css" rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap-responsive.min.css" />\n')
        self.wfile.write(b'\t\t<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>\n')
        self.wfile.write(b'\t\t<script src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>\n')
        if title:
            self.wfile.write(b'\t\t<title>ATP Sender</title>\n')
        else:
            self.wfile.write(bytes('\t\t<title>%s - ATP Sender</title>\n' %title, 'utf-8'))
        self.wfile.write(b'\t</head>\n')

    def form_proto(self, proto_name, proto):
        self.normal_header()
        self.wfile.write(b'\t<body>\n')
        self.wfile.write(b'\t<div class="container">\n')
        self.banner(proto_name)
        self.wfile.write(b'\t<div class="hero-unit">\n')
        self.wfile.write(bytes('\t\t<h1>%s</h1>\n' %proto_name, 'utf-8'))
        self.wfile.write(b'\t</div>\n')

        for packet in proto['packets']:
            self.wfile.write(b'\t<div class="row-fluid">\n')
            self.wfile.write(b'\t<div class="span12">\n')
            self.form_packet(proto_name, packet, proto['packets'][packet], prefix = b'\t\t\t')
            self.wfile.write(b'\t</div>\n')
            self.wfile.write(b'\t</div>\n')

        self.wfile.write(b'\t</div>\n')
        self.wfile.write(b'\t</body>\n')
        self.wfile.write(b'</html>\n')

        self.wfile.flush()

    def form_packet(self, proto_name, packet_name, packet, prefix = b''):
        self.wfile.write(prefix+bytes('\t<a name="%s"></a>\n' %('P'+packet_name), 'utf-8'))
        self.wfile.write(prefix+bytes('<form method="POST" action="?proto=%s&amp;packet=%s#%s" class="well form-horizontal">\n' %(proto_name, packet_name, 'P'+packet_name), 'utf-8'))
        self.wfile.write(prefix+b'\t<fieldset>\n')
        self.wfile.write(prefix+bytes('\t\t<legend>%s</legend>\n' %packet_name, 'utf-8'))
        for arg in packet['args']:
            self.wfile.write(b'\t<div class="control-group">\n')
            self.wfile.write(prefix+bytes('\t\t<label for="%s_%s" class="control-label">%s</label>\n' %(packet_name, arg, arg), 'utf-8'))
            self.wfile.write(b'\t<div class="controls">\n')
            self.wfile.write(prefix+bytes('\t\t<input type="text" id="%s" name="%s" /><br />\n' %(packet_name+'_'+arg, packet_name+'_'+arg), 'utf-8'))
            self.wfile.write(b'\t</div>\n')
            self.wfile.write(b'\t</div>\n')
        self.wfile.write(b'\t<div class="control-group">\n')
        self.wfile.write(b'\t<div class="controls">\n')
        self.wfile.write(b'<button type="submit" class="btn">Send</button>\n')
        self.wfile.write(b'\t</div>\n')
        self.wfile.write(b'\t</div>\n')
        self.wfile.write(prefix+b'\t</fieldset>\n')
        self.wfile.write(prefix+b'</form>\n')

    def banner(self, pending_proto = None):
        self.wfile.write(b'\t\t\t<div class="navbar navbar-inverse navbar-fixed-top">\n')
        self.wfile.write(b'\t\t\t<div class="navbar-inner">\n')
        self.wfile.write(b'\t\t\t<div class="container-fluid">\n')
        self.wfile.write(b'\t\t\t<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n')
        self.wfile.write(b'\t\t\t<span class="icon-bar"></span>\n')
        self.wfile.write(b'\t\t\t<span class="icon-bar"></span>\n')
        self.wfile.write(b'\t\t\t<span class="icon-bar"></span>\n')
        self.wfile.write(b'\t\t\t</a>\n')
        self.wfile.write(b'\t\t\t<a href="" class="brand">Protocoles</a>\n')
        self.wfile.write(b'\t\t\t<div class="nav-collapse collapse">\n')
        self.wfile.write(b'\t\t\t<ul class="nav">\n')
        for proto in self.protos:
            if proto == pending_proto:
                active = ' class="active"'
            else:
                active = ''
            self.wfile.write(bytes('\t\t\t\t<li%s><a href="?proto=%s">%s</a></li>\n' %(active, proto, proto), 'utf-8'))
        self.wfile.write(b'\t\t\t</ul>\n')
        self.wfile.write(b'\t\t\t</div>\n')
        self.wfile.write(b'\t\t\t</div>\n')
        self.wfile.write(b'\t\t\t</div>\n')
        self.wfile.write(b'\t\t\t</div>\n')


    def home(self):
        self.normal_header()
        self.wfile.write(b'\t<body>\n')
        self.wfile.write(b'\t<div class="container">\n')
        self.banner()
        self.wfile.write(b'\t<div class="hero-unit">\n')
        self.wfile.write(b'\t\t<h1>ATP Sender</h1>\n')
        self.wfile.write(b'\t<p>Please choose a protocole to start sending messages.</p>\n')
        self.wfile.write(b'\t</div>\n')
        self.wfile.write(b'\t</body>\n')
        self.wfile.write(b'</html>\n')

        self.wfile.flush()

if __name__ == "__main__":

    ATPHandler.channels = {}
    ATPHandler.files = {}
    for proto in ATPHandler.protos:
        sock = socket.socket()
        sock.connect(("localhost", 1300 + ATPHandler.protos[proto]['id']))
        file = sock.makefile(mode="rw")
        ATPHandler.files[proto] = file
        ATPHandler.channels[proto] = Channel(file.buffer, lambda: None, proto = proto, genAll = True)

    Handler = ATPHandler

    httpd = socketserver.TCPServer(("", int(sys.argv[1])), Handler)

    print("serving at port", sys.argv[1])
    httpd.serve_forever()
