#!/usr/bin/env python3

import http.server
import socketserver
import sys
import urllib.parse
import socket
import cgi
import argparse
from string import Template

import protos
from channel import Channel
from settings import HOST, PORT, HTTP_PORT


template_page = """<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8" />
        <link type="text/css" rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap.min.css" />
        <link type="text/css" rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/css/bootstrap-responsive.min.css" />
        <title>${TITLE}</title>
    </head>
    <body>
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container-fluid">
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>
                    <a href="" class="brand">Protocoles</a>
                    <div class="nav-collapse collapse">
                        <ul class="nav">${BANNER}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">${BODY}
        </div>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
    </body>
</html>
"""

template_banner = """
                            <li${ACTIVE}><a href="?proto=${PROTO}">${PROTO}</a></li>"""

template_home = """
            <div class="hero-unit">
                <h1>ATP Sender</h1>
                <p>Please choose a protocole to start sending messages.</p>
            </div>"""

template_proto = """
            <div class="hero-unit">
                <h1>${PROTO}</h1>
            </div>"""

template_packet = """
            <a name="${ANCRE}"></a>
            <div class="row-fluid">
                <div class="span12">
                    <form method="POST" action="?proto=${PROTO}&packet=${PACKET}#${ANCRE}" class="form-horizontal well">
                        <fieldset>
                            <legend>${PACKET}</legend>${ARGS}
                            <div class="control-group">
                                <div class="controls">
                                    <button type="submit" class="btn">Send</button>
                                </div>
                            </div>
                        </fieldset>
                    </form>
                </div>
            </div>"""

template_arg = """
                            <div class="control-group">
                                <label for="${PACKET}_${ARG}" class="control-label">${ARG}</label>
                                <div class="controls">
                                    <input type="text" id="${PACKET}_${ARG}" name="${PACKET}_${ARG}" /><br />
                                </div>
                            </div>"""

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

    def form_proto(self, proto_name, proto):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        template = Template(template_page)

        body = Template(template_proto).substitute(PROTO = proto_name)

        for packet in proto['packets']:
            body += self.form_packet(proto_name, packet, proto['packets'][packet])
        params = {}
        params['TITLE'] = 'ATP Sender'
        params['BANNER'] = self.banner()
        params['BODY'] = body

        self.wfile.write(bytes(template.substitute(params), 'utf-8'))

    def form_packet(self, proto_name, packet_name, packet):
        params = {}
        params['PROTO'] = proto_name
        params['PACKET'] = packet_name
        params['ANCRE'] = 'P'+packet_name
        params['ARGS'] = self.form_args(packet_name, packet)
        return Template(template_packet).substitute(params)

    def form_args(self, packet_name, packet):
        args = ''
        for arg in packet['args']:
            params = {}
            params['PACKET'] = packet_name
            params['ARG'] = arg
            args += Template(template_arg).substitute(params)
        return args

    def banner(self, pending_proto = None):
        banner = ''
        template = Template(template_banner)
        for proto in self.protos:
            if proto == pending_proto:
                active = ' class="active"'
            else:
                active = ''
            banner += template.substitute(ACTIVE = active, PROTO = proto)
        return banner

    def home(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        template = Template(template_page)

        args = {}

        args['TITLE'] = 'ATP Sender'
        args['BANNER'] = self.banner()
        args['BODY'] = """
            <div class="hero-unit">
                <h1>ATP Sender</h1>
                <p>Please choose a protocole to start sending messages.</p>
            </div>"""

        self.wfile.write(bytes(template.substitute(args), 'utf-8'))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='GUI to send ATP packets.', add_help=False)
    parser.add_argument('-h', '--host', dest='host', default=HOST, help='connect to remote host')
    parser.add_argument('-p', '--port', dest='port', default=PORT, help='port offset')
    parser.add_argument('-l', '--listen', dest='listen', default=HTTP_PORT, help='server listen on specified port')
    args = parser.parse_args()

    ATPHandler.channels = {}
    ATPHandler.files = {}
    for proto in ATPHandler.protos:
        sock = socket.socket()
        sock.connect((args.host, int(args.port) + ATPHandler.protos[proto]['id']))
        file = sock.makefile(mode="rw")
        ATPHandler.files[proto] = file
        ATPHandler.channels[proto] = Channel(file.buffer, lambda: None, proto = proto, transmitter = 'both')

    httpd = socketserver.TCPServer(("", int(args.listen)), ATPHandler)
    print("Server listening on port", args.listen)
    httpd.serve_forever()
