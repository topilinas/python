#!/usr/bin/env python

__all__ = ["Domain"]

import sys
import libvirt

connection = libvirt.open("qemu:///system")

def domainOperations(dom):
    return dict(
            run      = dom.create,
            stop     = dom.destroy,
            info     = dom.info,
            reset    = dom.reset,
            reboot   = dom.reboot,
            shutdown = dom.shutdown,
            destroy  = dom.undefine,
            suspend  = dom.suspend,
            resume   = dom.resume)

def domainCreate(conn, conf):
    xml = open(conf['xml']).read()
    new = xml.format(name=conf['name'], vcpu=conf['vcpu'],
            mem=conf['mem'], img=conf['img'])
    return conn.defineXML(new)


class Domain(object):
    def __init__(self, conf):
        self.conf = conf
        self.conn = connection
        try:
            self.dom = self.conn.lookupByName(self.conf['name'])
        except libvirt.libvirtError as err:
            print err.get_error_message()
        if (self.dom):
            self.__dict__.update(domainOperations(self.dom))

    def create(self):
        self.dom = domainCreate(self.conn, self.conf)
        if (self.dom):
            self.__dict__.update(domainOperations(self.dom))
