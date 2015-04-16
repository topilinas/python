#!/usr/bin/env python

import sys
import pprint

import libvirt

__all__ = ["Domain", "VirtManager"]


class Domain(object):
    def __init__(self, dom):
        self.dom = dom

    def operations(self):
        return dict(
                run      = self.dom.create,
                stop     = self.dom.destroy,
                info     = self.dom.info,
                reset    = self.dom.reset,
                reboot   = self.dom.reboot,
                shutdown = self.dom.shutdown,
                destroy  = self.dom.undefine,
                suspend  = self.dom.suspend,
                resume   = self.dom.resume,
                create   = lambda: None)

    def operate(self, cmd):
        try:
            return self.operations().get(cmd)()
        except AttributeError:
            print "Operation '{}' is not supported".format(args.cmd)
        except libvirt.libvirtError as err:
            print err.get_error_message()


class VirtManager(object):
    def __init__(self, conf):
        self.conn = libvirt.open("qemu:///system")
        self.conf = conf

    def create_domain(self):
        xml = open(self.conf['xml']).read()
        new = xml.format(name=self.conf['name'], vcpu=self.conf['vcpu'],
                mem=self.conf['mem'], img=self.conf['img'])
        try:
            return Domain(self.conn.defineXML(new))
        except libvirt.libvirtError as err:
            print err.get_error_message()

    def get_domain(self, dom_name):
        try:
            return Domain(self.conn.lookupByName(dom_name))
        except libvirt.libvirtError as err:
            print err.get_error_message()

    def lookup_domain(self, dom_name):
        try:
            return Domain(self.conn.lookupByName(dom_name))
        except libvirt.libvirtError as err:
            if err.get_error_code() == libvirt.VIR_ERR_NO_DOMAIN:
                return self.create_domain()
