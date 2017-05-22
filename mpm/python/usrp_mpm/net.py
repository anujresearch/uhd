
# Copyright 2017 Ettus Research (National Instruments)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
N310 implementation module
"""
import itertools
import socket
from pyroute2 import IPRoute
from .mpmlog import get_logger


def get_valid_interfaces(iface_list):
    """
    Given a list of interfaces (['eth1', 'eth2'] for example), return the
    subset that contains actually valid entries.
    Interfaces are checked for if they actually exist, and if so, if they're up.
    """
    ipr = IPRoute()
    valid_ifaces = []
    for iface in iface_list:
        valid_iface_idx = ipr.link_lookup(ifname=iface)
        if len(valid_iface_idx) == 0:
            continue
        valid_iface_idx = valid_iface_idx[0]
        link_info = ipr.get_links(valid_iface_idx)[0]
        if link_info.get_attr('IFLA_OPERSTATE') == 'UP' \
                and len(get_iface_addrs(link_info.get_attr('IFLA_ADDRESS'))):
            assert link_info.get_attr('IFLA_IFNAME') == iface
            valid_ifaces.append(iface)
    ipr.close()
    return valid_ifaces


def get_iface_info(ifname):
    """
    Given an interface name (e.g. 'eth1'), return a dictionary with the
    following keys:
    - ip_addr: Main IPv4 address
    - ip_addrs: List of valid IPv4 addresses
    - mac_addr: MAC address

    All values are stored as strings.
    """
    ipr = IPRoute()
    try:
        link_info = ipr.get_links(ipr.link_lookup(ifname=ifname))[0]
    except IndexError:
        raise LookupError("Could not identify interface `{}'".format(ifname))
    mac_addr = link_info.get_attr('IFLA_ADDRESS')
    ip_addrs = get_iface_addrs(mac_addr)
    return {
        'mac_addr': mac_addr,
        'ip_addr': ip_addrs[0],
        'ip_addrs': ip_addrs,
    }

def get_iface_addrs(mac_addr):
    """
    return ipv4 addresses for a given macaddress
    input format: "aa:bb:cc:dd:ee:ff"
    """
    ip2 = IPRoute()
    # returns index
    [link] = ip2.link_lookup(address=mac_addr)
    # Only get v4 addresses
    addresses = [addr.get_attrs('IFA_ADDRESS')
                 for addr in ip2.get_addr(family=socket.AF_INET)
                 if addr.get('index', None) == link]
    # flatten possibly nested list
    addresses = list(itertools.chain.from_iterable(addresses))
    ip2.close()
    return addresses


def byte_to_mac(byte_str):
    """
    converts a bytestring into nice hex representation
    """
    return ':'.join(["%02x" % ord(x) for x in byte_str])


def get_mac_addr(remote_addr):
    """
    return MAC address of a remote host already discovered
    or None if no host entry was found
    """
    ip2 = IPRoute()
    addrs = ip2.get_neighbours(dst=remote_addr)
    if len(addrs) > 1:
        get_logger('get_mac_addr').warning("More than one device with the same IP address found. Picking entry at random")
    if not addrs:
        return None
    return addrs[0].get_attr('NDA_LLADDR')
