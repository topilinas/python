#!/usr/bin/env python

import sys
import os
import argparse

import libvirt

from virtmanager import VirtManager


if __name__ == "__main__":

    def arg_parser():
        parser = argparse.ArgumentParser(description="Operate with VMs on KVM")
        parser.add_argument("cmd", help="Operation for execution")
        parser.add_argument("dom", help="VM domain name")
        parser.add_argument("--xml", default="template.xml", help="Path to xml template")
        parser.add_argument("--img", default="img.qcow2", help="Path to qcow2 image")
        parser.add_argument("--mem", type=int, default=2048, help="Maximum available memory")
        parser.add_argument("--vcpu", type=int, default=2, help="Number of virtual CPUs")
        args = parser.parse_args()

        if args.cmd == "create":
            if not os.path.isfile(args.img):
                print "No such file: {}".format(args.img)
                sys.exit(1)
            if not os.path.isfile(args.xml):
                print "No such file: {}".format(args.xml)
                sys.exit(1)

        return args

    args = arg_parser()
    conf = dict(xml=args.xml, img=args.img, mem=args.mem, vcpu=args.vcpu, name=args.dom)

    virt_manager = VirtManager(conf)
    vm = virt_manager.lookup_domain(args.dom)
    print vm.operate(args.cmd)
