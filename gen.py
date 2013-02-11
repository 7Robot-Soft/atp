#!/usr/bin/env python

import inspect
import protos
from protos import Proto
from packet import Packet
import sys, os
from atp import formats as formats_code

formats_name = { 'B' : 'unsigned char',
            'H' : 'unsigned int',
            'I' : 'unsigned long int',
            'b' : 'char',
            'h' : 'int',
            'i' : 'long int',
            'f' : 'float' }

formats_code = dict((v[1],k) for k, v in formats_code.items())

def generateFunction(c, h, proto, name, paquet):
    #name = "Send" + proto + name[0].upper() + name[1:]
    name = "Send" + name[0].upper() + name[1:]
    print("\tencoder '%s'" %name)
    args = ', '.join(map(lambda x: formats_name[x[1]]+" "+x[0], paquet.attrs))
    h.write("void %s(%s);\n\n" %(name, args))
    c.write("void %s(%s) {\n" %(name, args))
    c.write("    char bytes[] = { \n            129,\n            ")
    c.write("%d,\n            " %paquet.id)
    s = "((char*)&%s)[%d]"
    i = 3
    for arg, type in paquet.attrs:
        c.write("%s,\n            " %formats_code[type])
        if type == 'B':
            i += 2
            c.write(arg)
        elif type == 'H':
            i += 3
            c.write(s %(arg, 0))
            c.write(",\n            ")
            c.write(s %(arg, 1))
        elif type == 'I':
            i += 5
            c.write(s %(arg, 0))
            c.write(",\n            ")
            c.write(s %(arg, 1))
            c.write(",\n            ")
            c.write(s %(arg, 2))
            c.write(",\n            ")
            c.write(s %(arg, 3))
        elif type == 'b':
            i += 2
            c.write(arg)
        elif type == 'h':
            i += 3
            c.write(s %(arg, 0))
            c.write(",\n            ")
            c.write(s %(arg, 1))
        elif type == 'i':
            i += 5
            c.write(s %(arg, 0))
            c.write(",\n            ")
            c.write(s %(arg, 1))
            c.write(",\n            ")
            c.write(s %(arg, 2))
            c.write(",\n            ")
            c.write(s %(arg, 3))
        elif type == 'f':
            i += 5
            c.write(s %(arg, 0))
            c.write(",\n            ")
            c.write(s %(arg, 1))
            c.write(",\n            ")
            c.write(s %(arg, 2))
            c.write(",\n            ")
            c.write(s %(arg, 3))
        else:
            print("Error: unimplemented type (%s)" %type)
            exit(1)
        c.write(",\n            ")
    c.write("128\n        };\n");
    c.write("    SendBytes(bytes, %d);\n" %i)
    c.write("}\n\n")

def generateTemplate(c, h, proto, name, paquet):

    #name = "Recv" + proto + name[0].upper() + name[1:]
    name = "On" + name[0].upper() + name[1:]
    print("\tdecoder '%s'" %name)
    args = ', '.join(map(lambda x: formats_name[x[1]]+" "+x[0], paquet.attrs))
    h.write("// You should define this function\nvoid %s(%s);\n\n" %(name, args))
    c.write("__attribute__((weak)) void %s(%s) {" %(name, args))
    if name == "OnGetId":
        c.write("\n    SendBoardId();\n")
    elif name == "OnTest":
        c.write("\n    SendTest(B, H, I, b, h, i, f);\n")
    c.write("}\n\n")

def generateProto(dest, version, name, proto):
    print("Generate files for '%s' ..." %name)
    dest = "%s/atp-%s" %(dest, name[0].lower() + name[1:])
    c = open("%s.c" %dest, 'w')
    c.write("// Fichier auto-généré à partir de la version %s du fichier de protocole\n\n" %version)
    c.write("#include \"atp.h\"\n\n")
    h = open("%s.h" %dest, 'w')
    h.write("// Fichier auto-généré à partir de la version %s du fichier de protocole\n\n" %version)
    h.write("#ifndef _%s_H_\n#define _%s_H_\n\n" %(name.upper(), name.upper()))
    if hasattr(proto, "type"):
        h.write("#define BOARD_ID %d\n" %proto.type)
        h.write("#define BOARD_NAME %s\n" %name)
        h.write("#define BOARD_PROCESSOR process%s\n\n" %name)
    for attrn in proto.__dict__:
        attr = proto.__getattribute__(proto, attrn)
        if isinstance(attr, Packet):
            if attr.direction == "pic" or attr.direction == "both":
                generateFunction(c, h, name, attrn, attr)
            if attr.direction == "arm" or attr.direction == "both":
                generateTemplate(c, h, name, attrn, attr)

    prototype = "int process%s(int id,\n"
    prototype += "            unsigned char *ucharv, int ucharc,\n"
    prototype += "            unsigned int *ushortv, int ushortc,\n"
    prototype += "            unsigned long int *uintv, int uintc,\n"
    prototype += "            char *charv, int charc,\n"
    prototype += "            int *shortv, int shortc,\n"
    prototype += "            long int *intv, int intc,\n"
    prototype += "            float *floatv, int floatc)"
    h.write(prototype %name + ";\n\n")
    c.write(prototype %name + " {\n")
    for attrn in proto.__dict__:
        attr = proto.__getattribute__(proto, attrn)
        if isinstance(attr, Packet):
            if attr.direction == "arm" or attr.direction == "both":
                c.write("    if (id == %d) {\n" %attr.id)
                fname = "On" + attrn[0].upper() + attrn[1:]
                c.write("        %s(" %fname)
                i = 0
                ucharc = 0
                ushortc = 0
                uintc = 0
                charc = 0
                shortc = 0
                intc = 0
                floatc = 0
                for arg in attr.attrs:
                    i += 1
                    if arg[1] == 'B':
                        c.write("ucharv[%d]" %ucharc)
                        ucharc += 1
                    elif arg[1] == 'H':
                        c.write("ushortv[%d]" %ushortc)
                        ushortc += 1
                    elif arg[1] == 'I':
                        c.write("uintv[%d]" %uintc)
                        uintc += 1
                    elif arg[1] == 'b':
                        c.write("charv[%d]" %charc)
                        charc += 1
                    elif arg[1] == 'h':
                        c.write("shortv[%d]" %shortc)
                        shortc += 1
                    elif arg[1] == 'i':
                        c.write("intv[%d]" %intc)
                        intc += 1
                    elif arg[1] == 'f':
                        c.write("floatv[%d]" %floatc)
                        floatc += 1
                    else:
                        print("Error: unimplemented type (%s)" %type)
                        exit(1)
                    if i != len(attr.attrs):
                        c.write(",\n            ")
                c.write(");\n        return 1;\n")
                c.write("    }\n")
    c.write("    return 0;\n}\n");
    c.close()
    h.write("#endif\n")
    h.close()

def generateAll(dest):
    for name, obj in inspect.getmembers(protos,
            lambda x: inspect.isclass(x) and issubclass(x, Proto)):
        generateProto(dest, protos.version, name, obj)

if __name__=="__main__":
    if len(sys.argv) > 1:
        dest = sys.argv[1]
    else:
        dest = "gen"
    print("Saving auto-generated files in '%s'" %dest)
    if not os.path.exists(dest):
        print("Creating directory")
        os.makedirs(dest)
    generateAll(dest)
