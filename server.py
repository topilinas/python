#!/usr/bin/env python

import sys
import os
import argparse
from gevent.pywsgi import WSGIServer
from webob import Request, Response
from gevent import sleep

import libvirt

from virtmanager import VirtManager


conf = dict(
        xml=os.path.abspath("template.xml"),
        img=os.path.abspath("../vm/debian.qcow2"),
        mem=2048,
        vcpu=2,
        name="debian")

def operate(conf, cmd):
    virt_manager = VirtManager(conf)
    vm = virt_manager.lookup_domain(conf['name'])
    try:
        return vm.operate(cmd)
    except AttributeError:
            print "Operation '{}' is not supported".format(cmd)
    except libvirt.libvirtError as err:
            print err
    return "Operation failed"


def application(environ, start_response):
    req = Request(environ)
    res = Response()
    cmd = req.path_info_pop()
    new_conf = req.path_info_pop()
    conf.update(dict(map(lambda i: i.split('='), new_conf.split('&'))))
    res.content_type = 'text/plain'
    sleep(1)
    res.body = str(operate(conf, cmd)) + "\n"
    return res(environ, start_response)

if __name__ == '__main__':
    WSGIServer(('', 8080), application).serve_forever()
