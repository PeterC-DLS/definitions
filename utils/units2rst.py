#!/usr/bin/env python

'''
Read the the NeXus NXDL types specification and find
all the valid types of units.  Write a restructured
text (.rst) document for use in the NeXus manual in 
the NXDL chapter.
'''


import os, sys
import lxml.etree


def worker(nodeMatchString, section = 'units'):
    if len(sys.argv) != 2:
        print "usage: %s nxdlTypes.xsd" % sys.argv[0]
        exit()
    NXDL_TYPES_FILE = sys.argv[1]
    if not os.path.exists(NXDL_TYPES_FILE):
        print "Cannot find %s" % NXDL_TYPES_FILE
        exit()
        
    tree = lxml.etree.parse(NXDL_TYPES_FILE)
    
    output = ['.. auto-generated -- DO NOT EDIT']
    output.append('')
    
    labels = ('term', 'description')
    output.append('.. nodeMatchString : %s' % nodeMatchString)
    output.append('')
    db = {}
    
    NAMESPACE = 'http://www.w3.org/2001/XMLSchema'
    ns = {'xs': NAMESPACE}
    root = tree.xpath('//xs:schema', namespaces=ns)[0]
    s = '//xs:simpleType'
    for node in tree.xpath("//xs:simpleType", namespaces=ns):
        if node.get('name') == nodeMatchString:
            for item in node.xpath('xs:restriction//xs:enumeration', namespaces=ns):
                key = '%s' % item.get('value')
                words = item.xpath('xs:annotation/xs:documentation', namespaces=ns)[0]
                db[key] = words.text
    
    print '\n'.join(output)
    
    # this list is too long to make this a table in latex
    # for two columns, a Sphinx fieldlist will do just as well
    for key in sorted(db):
        print '.. index:: ! %s (%s type)\n' % (key, section)       # index entry
        print '.. _%s:\n' % key       # cross-reference point
        print ':%s:' % key
        for line in db[key].splitlines():
            print '    %s' % line
        print ''


if __name__ == '__main__':
    worker('anyUnitsAttr')


# NeXus - Neutron and X-ray Common Data Format
# 
# Copyright (C) 2008-2016 NeXus International Advisory Committee (NIAC)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For further information, see http://www.nexusformat.org
