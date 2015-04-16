#!/usr/bin/env python

import sys
import os
import argparse
import domops
import libvirt


def argParser():
    parser = argparse.ArgumentParser(description="Operate with VMs on KVM")
    parser.add_argument("cmd", help="Operation for execution")
    parser.add_argument("dom", help="VM domain name")
    parser.add_argument("--xml", default="template.xml", help="Path to xml template")
    parser.add_argument("--img", default=os.path.abspath("img.qcow2"), help="Path to qcow2 image")
    parser.add_argument("--mem", type=int, default=2048, help="Maximum available memory")
    parser.add_argument("--vcpu", type=int, default=2, help="Number of virtual CPUs")
    return parser.parse_args()


args = argParser()
conf = dict(xml=args.xml, img=args.img, mem=args.mem, vcpu=args.vcpu, name=args.dom)

dom = domops.Domain(conf)

try:
    getattr(dom, args.cmd)()
except AttributeError:
    print "Operation '{}' is not supported".format(args.cmd)
except libvirt.libvirtError as err:
    print err
