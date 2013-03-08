#!/usr/bin/env python3

#import inspect
#import semantic
#from protos import Proto, Packet, cformats
#import sys, os
#from atp import formats as formats_code

#formats_code = dict((v[1],k) for k, v in formats_code.items())

#def generateFunction(c, h, proto, name, paquet):
#    name = "Send" + name[0].upper() + name[1:]
#    print("\tencoder '%s'" %name)
#    args = ', '.join(map(lambda x: cformats[x[1]]+" "+x[0], paquet.attrs))
#    h.write("void %s(%s);\n\n" %(name, args))
#    c.write("void %s(%s) {\n" %(name, args))
#    c.write("    char bytes[] = { \n            129,\n            ")
#    c.write("%d,\n            " %paquet.id)
#    s = "((char*)&%s)[%d]"
#    i = 3
#    for arg, type in paquet.attrs:
#        c.write("%s,\n            " %formats_code[type])
#        if type == 'B':
#            i += 2
#            c.write(arg)
#        elif type == 'H':
#            i += 3
#            c.write(s %(arg, 0))
#            c.write(",\n            ")
#            c.write(s %(arg, 1))
#        elif type == 'I':
#            i += 5
#            c.write(s %(arg, 0))
#            c.write(",\n            ")
#            c.write(s %(arg, 1))
#            c.write(",\n            ")
#            c.write(s %(arg, 2))
#            c.write(",\n            ")
#            c.write(s %(arg, 3))
#        elif type == 'b':
#            i += 2
#            c.write(arg)
#        elif type == 'h':
#            i += 3
#            c.write(s %(arg, 0))
#            c.write(",\n            ")
#            c.write(s %(arg, 1))
#        elif type == 'i':
#            i += 5
#            c.write(s %(arg, 0))
#            c.write(",\n            ")
#            c.write(s %(arg, 1))
#            c.write(",\n            ")
#            c.write(s %(arg, 2))
#            c.write(",\n            ")
#            c.write(s %(arg, 3))
#        elif type == 'f':
#            i += 5
#            c.write(s %(arg, 0))
#            c.write(",\n            ")
#            c.write(s %(arg, 1))
#            c.write(",\n            ")
#            c.write(s %(arg, 2))
#            c.write(",\n            ")
#            c.write(s %(arg, 3))
#        else:
#            print("Error: unimplemented type (%s)" %type)
#            exit(1)
#        c.write(",\n            ")
#    c.write("128\n        };\n");
#    c.write("    SendBytes(bytes, %d);\n" %i)
#    c.write("}\n\n")
#
#def generateTemplate(c, h, proto, name, paquet):
#
#    name = "On" + name[0].upper() + name[1:]
#    print("\tdecoder '%s'" %name)
#    args = ', '.join(map(lambda x: cformats[x[1]]+" "+x[0], paquet.attrs))
#    h.write("// You should define this function\nvoid %s(%s);\n\n" %(name, args))
#    c.write("__attribute__((weak)) void %s(%s) {" %(name, args))
#    if name == "OnGetId":
#        c.write("\n    SendBoardId();\n")
#    elif name == "OnTest":
#        c.write("\n    SendTest(B, H, I, b, h, i, f);\n")
#    c.write("}\n\n")
#
#def generateProto(dest, version, name, proto):
#    print("Generate files for '%s' ..." %name)
#    dest = "%s/atp-%s" %(dest, name[0].lower() + name[1:])
#    c = open("%s.c" %dest, 'w')
#    c.write("// Fichier auto-généré à partir de la version %s du fichier de protocole\n\n" %version)
#    c.write("#include \"atp.h\"\n\n")
#    h = open("%s.h" %dest, 'w')
#    h.write("// Fichier auto-généré à partir de la version %s du fichier de protocole\n\n" %version)
#    h.write("#ifndef _%s_H_\n#define _%s_H_\n\n" %(name.upper(), name.upper()))
#    if hasattr(proto, "type"):
#        h.write("#define BOARD_ID %d\n" %proto.type)
#        h.write("#define BOARD_NAME %s\n" %name)
#        h.write("#define BOARD_PROCESSOR process%s\n\n" %name)
#    for attrn in sorted(proto.__dict__):
#        attr = proto.__getattribute__(proto, attrn)
#        if isinstance(attr, Packet):
#            if attr.direction == "pic" or attr.direction == "both":
#                generateFunction(c, h, name, attrn, attr)
#            if attr.direction == "arm" or attr.direction == "both":
#                generateTemplate(c, h, name, attrn, attr)
#
#    prototype = "int process%s(int id,\n"
#    prototype += "            unsigned char *ucharv, int ucharc,\n"
#    prototype += "            unsigned int *ushortv, int ushortc,\n"
#    prototype += "            unsigned long int *uintv, int uintc,\n"
#    prototype += "            char *charv, int charc,\n"
#    prototype += "            int *shortv, int shortc,\n"
#    prototype += "            long int *intv, int intc,\n"
#    prototype += "            float *floatv, int floatc)"
#    h.write(prototype %name + ";\n\n")
#    c.write(prototype %name + " {\n")
#    for attrn in sorted(proto.__dict__):
#        attr = proto.__getattribute__(proto, attrn)
#        if isinstance(attr, Packet):
#            if attr.direction == "arm" or attr.direction == "both":
#                c.write("    if (id == %d) {\n" %attr.id)
#                fname = "On" + attrn[0].upper() + attrn[1:]
#                c.write("        %s(" %fname)
#                i = 0
#                ucharc = 0
#                ushortc = 0
#                uintc = 0
#                charc = 0
#                shortc = 0
#                intc = 0
#                floatc = 0
#                for arg in attr.attrs:
#                    i += 1
#                    if arg[1] == 'B':
#                        c.write("ucharv[%d]" %ucharc)
#                        ucharc += 1
#                    elif arg[1] == 'H':
#                        c.write("ushortv[%d]" %ushortc)
#                        ushortc += 1
#                    elif arg[1] == 'I':
#                        c.write("uintv[%d]" %uintc)
#                        uintc += 1
#                    elif arg[1] == 'b':
#                        c.write("charv[%d]" %charc)
#                        charc += 1
#                    elif arg[1] == 'h':
#                        c.write("shortv[%d]" %shortc)
#                        shortc += 1
#                    elif arg[1] == 'i':
#                        c.write("intv[%d]" %intc)
#                        intc += 1
#                    elif arg[1] == 'f':
#                        c.write("floatv[%d]" %floatc)
#                        floatc += 1
#                    else:
#                        print("Error: unimplemented type (%s)" %type)
#                        exit(1)
#                    if i != len(attr.attrs):
#                        c.write(",\n            ")
#                c.write(");\n        return 1;\n")
#                c.write("    }\n")
#    c.write("    return 0;\n}\n");
#    c.close()
#    h.write("#endif\n")
#    h.close()
#
#def generateAll(dest):
#    for proto in protos
#            generateProto(dest, semantic.version, name, obj)

import sys, os
from protos import load, cformats
from semantic import version
from string import Template
from atp import formats

template_c = """// Generated from version ${VERSION} of semantic

#include "atp.h"

${FUNCTIONS}

int AtpDecode(int id,
        unsigned char *ucharv, int ucharc,
        unsigned int *ushortv, int ushortc,
        unsigned long int *uintv, int uintc,
        char *charv, int charc,
        int *shortv, int shortc,
        long int *intv, int intc,
        float *floatv, int floatc)
{${DECODERS}
    return 0;
}

"""

template_decoder = """
    if (id == ${ID}) {
        ${FUNCTION}(${ARGV});
        return 1;
    }"""

template_h = """// Generated from version ${VERSION} of semantic

#ifndef _${PROTO_UPPER}_H_
#define _${PROTO_UPPER}_H_

#define BOARD_ID ${ID}
#define BOARD_NAME ${PROTO}

${PROTOTYPES}

int AtpDecode(int id,
        unsigned char *ucharv, int ucharc,
        unsigned int *ushortv, int ushortc,
        unsigned long int *uintv, int uintc,
        char *charv, int charc,
        int *shortv, int shortc,
        long int *intv, int intc,
        float *floatv, int floatc);

#endif // _${PROTO_UPPER}_H_
"""

template_encoder_c = """
void ${FUNCTION}(${ARGS}) {
    char bytes[] = {
        129,
        ${ID},${CODE}
        128
    };
    SendBytes(bytes, ${COUNT});
}
"""

template_arg = """
        ${ARG},"""

template_long_arg = """
        ((char*)&${ARG})[${I}],"""

template_encoder_h = """
void ${FUNCTION}(${ARGS});
"""

template_decoder_c = """
// You should redefine this function
__attribute__((weak)) void ${FUNCTION}(${ARGS}) {${CODE}}
"""

template_decoder_h = """
void ${FUNCTION}(${ARGS});
"""

class PicGenerator:

    arrayname = { 'B': 'ucharv',
            'H': 'ushortv',
            'I': 'uintv',
            'b': 'charv',
            'h': 'shortv',
            'i': 'intv',
            'f': 'floatv' }

    def __init__(self, dest):

        if not os.path.exists(dest):
            print("Creating directory '%s'" %dest)
            os.makedirs(dest)
        self.dest = dest

        self.protos = load()

        self.formats = dict((v[1],k) for k, v in formats.items())

    def genAll(self):
        for proto_name in self.protos:
            proto = self.protos[proto_name]
            self.genProto(proto_name, proto)

    def genProto(self, proto_name, proto):
        print("Generate files for '%s'..." %proto_name)

        cfile = open("%s/atp-%s.c" %(self.dest, proto_name.lower()), 'w')
        hfile = open("%s/atp-%s.h" %(self.dest, proto_name.lower()), 'w')

        params = {}
        params['VERSION'] = version
        params['PROTO'] = proto_name
        params['PROTO_UPPER'] = proto_name.upper()
        params['ID'] = proto['id']
        params['PROTOTYPES'] = ''
        params['FUNCTIONS'] = ''
        params['DECODERS'] = ''
        
        for packet_name in proto['packets']:
            packet = proto['packets'][packet_name]
            c, h, d = self.genPacket(packet_name, packet)
            params['FUNCTIONS'] += c
            params['PROTOTYPES'] += h
            params['DECODERS'] += d

        cfile.write(Template(template_c).substitute(params))
        hfile.write(Template(template_h).substitute(params))

    def genPacket(self, packet_name, packet):
        c = ''
        h = ''
        d = ''
        if packet['direction'] == 'arm' or packet['direction'] == 'both':
            _c, _h, _d = self.genDecoder(packet_name, packet)
            c += _c
            h += _h
            d += _d
        if packet['direction'] == 'pic' or packet['direction'] == 'both':
            _c, _h = self.genEncoder(packet_name, packet)
            c += _c
            h += _h
        return (c, h, d)

    def genDecoder(self, packet_name, packet):
        params = {}
        params['ID'] = packet['id']
        params['FUNCTION'] = 'On' + packet_name[0].upper() + packet_name[1:]
        params['ARGS'] = ', '.join(map(lambda x: cformats[packet['args'][x]]+' '+x, packet['args']))
        params['ARGV'] = ''

        counts = dict(zip(self.formats,map(lambda x: 0, self.formats)))
        for arg in packet['args']:
            type = packet['args'][arg]
            params['ARGV'] += self.arrayname[type] + "[%d], " %counts[type]
            counts[type] += 1
        params['ARGV'] = params['ARGV'][:-2]

        if packet_name == 'getId':
            params['CODE'] = ' SendBoardId(); '
        elif packet_name == 'test':
            params['CODE'] = ' SendTest(B, H, I, b, h, i, f); '
        else:
            params['CODE'] = ''

        print("\tdecoder '%s'" %params['FUNCTION'])
        c = Template(template_decoder_c).substitute(params)
        h = Template(template_decoder_h).substitute(params)
        d = Template(template_decoder).substitute(params)
        return (c, h, d)

    def genEncoder(self, packet_name, packet):
        params = {}
        params['FUNCTION'] = 'Send' + packet_name[0].upper() + packet_name[1:]
        params['ARGS'] = ', '.join(map(lambda x: cformats[packet['args'][x]]+' '+x, packet['args']))
        params['ID'] = packet['id']
        params['COUNT'] = 3
        params['CODE'] = ''
        for arg in packet['args']:
            count, code = self.genArg(arg, packet['args'][arg])
            params['COUNT'] += count
            params['CODE'] += code
        print("\tencoder '%s'" %params['FUNCTION'])
        c = Template(template_encoder_c).substitute(params)
        h = Template(template_encoder_h).substitute(params)
        return (c, h)

    def genArg(self, arg, format):
        format = self.formats[format]
        length = format & 0b1111
        code = Template(template_arg).substitute({'ARG': format})
        if length == 1:
            code += Template(template_arg).substitute({'ARG': arg})
        else:
            for i in range(0, length):
                code += Template(template_long_arg).substitute({'ARG': arg, 'I': i})
        return (length+1, code)

if __name__=="__main__":

    if len(sys.argv) > 1:
        dest = sys.argv[1]
    else:
        dest = "gen"

    print("Saving auto-generated files in '%s'" %dest)

    generator = PicGenerator(dest)

    generator.genAll()
