#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# ----------------------------------------------------------------------------
# NAME:    HAPROXY-TEST.PY
# DESC:    DOCKER_SWARM-MODE.HAPROXY-TEST.
# DATE:    13.10.2017
# LANG:    PYTHON 3
# AUTOR:   LAGUTIN R.A.
# CONTACT: RLAGUTIN@MTA4.RU
# ----------------------------------------------------------------------------

# pip3 install -U pip
# pip3 install -U Flask
# pip3 install -U psutil
# pip3 install -U netifaces

import os
import sys
import json
import socket
import psutil
import netifaces

from flask import Flask, request
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

visits = 0
app = Flask(__name__)


def netstat():

    netstat_tmp = dict()
    proc_names_tmp = dict()

    netstat_result = list()

    for p in psutil.process_iter(attrs=['pid', 'name']):

        proc_names_tmp[p.info['pid']] = p.info['name']

    for c in psutil.net_connections(kind='inet'):

        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)

        netstat_tmp['proto'] = proto_map[(c.family, c.type)]
        netstat_tmp['laddr'] = laddr
        netstat_tmp['raddr'] = raddr or AD
        netstat_tmp['status'] = c.status
        netstat_tmp['pid'] = c.pid or AD
        netstat_tmp['proc'] = proc_names_tmp.get(c.pid, '?')[:15]

        if netstat_tmp:
            netstat_result.append(netstat_tmp.copy())
            netstat_tmp.clear()

    # print(json.dumps(netstat_result, indent=4))
    return netstat_result


def network():

    network_result = list()
    network_if_tmp = dict()
    network_ip_tmp = list()
    network_ifaddress_tmp = dict()

    for interface in netifaces.interfaces():

        if interface in ['lo']:
            continue

        ifaddresses = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in ifaddresses:

            network_if_tmp['interface'] = str(interface)

            for ifaddress_inet in ifaddresses[netifaces.AF_INET]:

                network_ifaddress_tmp['addr'] = (str(ifaddress_inet['addr']))
                network_ifaddress_tmp['netmask'] = (
                    str(ifaddress_inet['netmask']))
                network_ip_tmp.append(network_ifaddress_tmp.copy())
                network_ifaddress_tmp.clear()

            network_if_tmp['ipaddrs'] = network_ip_tmp[::]
            network_ip_tmp.clear()

        if network_if_tmp:
            network_result.append(network_if_tmp.copy())
            network_if_tmp.clear()

    # print(json.dumps(network_result, indent=4))
    return network_result


@app.route("/")
def hello():

    global visits
    visits += 1

    html = "<html><head><title>DOCKER_SWARM-MODE.HAPROXY-TEST</title></head>" \
        "<style>" \
        "body {" \
        "background-color: white;" \
        "text-align: left;" \
        "padding: 50px;" \
        "font-family: 'Open Sans','Helvetica Neue',Helvetica,Arial,sans-serif;" \
        "}" \
        "</style>" \
        "</head>" \
        "<body>"

    html += "<h3>Hello from <font color='#337ab7'>{name}</font></h3>".format(
        name=request.host)
    html += "<b>Visits:</b> {visits}<br>" \
        "<b>Hostname:</b> {hostname}<br>".format(hostname=socket.gethostname(),
                                                 visits=visits)

    if request.url:

        html += "<b>Request Url: </b>" + str(request.url) + "<br>"
        html += "<b>Request Path: </b>" + str(request.path) + "<br>"
        html += "<b>Request Method: </b>" + str(request.method) + "<br>"
        html += "<br><hr>"

    if request.headers:

        html += "<h4>Headers:</h4>"

        for headers_key, headers_value in request.headers.items():

            html += headers_key + ": " + headers_value + "<br>"

        html += "<br><hr>"

    network_res = network()

    if network_res:

        html += "<h4>Networking:</h4>"

        for net in network_res:

            for net_key, net_value in net.items():

                if net_key == 'interface':
                    html += "Network Interface: " + \
                        str(net_value) + "<br>"

                if net_key == 'ipaddrs':

                    for ipaddr in net_value:

                        for ipaddr_key, ipaddr_value in ipaddr.items():

                            # print(ipaddr_key, ipaddr_value)
                            if ipaddr_key == 'addr':
                                html += "&nbsp;&nbsp;&nbsp;&nbsp;IP Address: " + \
                                    str(ipaddr_value) + "<br>"

                            if ipaddr_key == 'netmask':
                                html += "&nbsp;&nbsp;&nbsp;&nbsp;Netmask: " + \
                                    str(ipaddr_value) + "<br>"

                    html += "<br>"

    html += "<hr>"

    netstat_res = netstat()

    if netstat_res:

        netstat_conn_listen_tmp = dict()
        netstat_conn_established_tmp = dict()
        netstat_conn_time_wait_tmp = dict()
        netstat_conn_none_tmp = dict()

        netstat_conn_listen = list()
        netstat_conn_established = list()
        netstat_conn_time_wait = list()
        netstat_conn_none = list()

        netstat_conn_res = list()

        html += "<h4>Netstat:</h4>"
        html += "<table width='100%'>"
        html += "<tr bgcolor='#337ab7' cellpadding='2' cellspacing='2'>"
        html += "<td >Proto</td><td>Local address</td><td>Remote address</td><td>Status</td><td>PID</td><td>Program name</td>"
        html += "</tr>"

        for netstat_conn in netstat_res:

            if netstat_conn['status'] == 'LISTEN':

                netstat_conn_listen_tmp = {
                    'proto': netstat_conn['proto'],
                    'laddr': netstat_conn['laddr'],
                    'raddr': netstat_conn['raddr'],
                    'status': netstat_conn['status'],
                    'pid': netstat_conn['pid'],
                    'proc': netstat_conn['proc']
                }

                if netstat_conn_listen_tmp:
                    netstat_conn_listen.append(netstat_conn_listen_tmp.copy())
                    netstat_conn_listen_tmp.clear()

            elif netstat_conn['status'] == 'ESTABLISHED':

                netstat_conn_established_tmp = {
                    'proto': netstat_conn['proto'],
                    'laddr': netstat_conn['laddr'],
                    'raddr': netstat_conn['raddr'],
                    'status': netstat_conn['status'],
                    'pid': netstat_conn['pid'],
                    'proc': netstat_conn['proc']
                }

                if netstat_conn_established_tmp:
                    netstat_conn_established.append(
                        netstat_conn_established_tmp.copy())
                    netstat_conn_established_tmp.clear()

            elif netstat_conn['status'] == 'TIME_WAIT':

                netstat_conn_time_wait_tmp = {
                    'proto': netstat_conn['proto'],
                    'laddr': netstat_conn['laddr'],
                    'raddr': netstat_conn['raddr'],
                    'status': netstat_conn['status'],
                    'pid': netstat_conn['pid'],
                    'proc': netstat_conn['proc']
                }

                if netstat_conn_time_wait_tmp:
                    netstat_conn_time_wait.append(
                        netstat_conn_time_wait_tmp.copy())
                    netstat_conn_time_wait_tmp.clear()

            elif netstat_conn['status'] == 'NONE':

                netstat_conn_none_tmp = {
                    'proto': netstat_conn['proto'],
                    'laddr': netstat_conn['laddr'],
                    'raddr': netstat_conn['raddr'],
                    'status': netstat_conn['status'],
                    'pid': netstat_conn['pid'],
                    'proc': netstat_conn['proc']
                }

                if netstat_conn_none_tmp:
                    netstat_conn_none.append(netstat_conn_none_tmp.copy())
                    netstat_conn_none_tmp.clear()

        netstat_conn_res.append(netstat_conn_listen[::])
        netstat_conn_res.append(netstat_conn_established[::])
        netstat_conn_res.append(netstat_conn_time_wait[::])
        netstat_conn_res.append(netstat_conn_none[::])

        # print(json.dumps(netstat_conn_res, indent=4))

        for netstat_conn_items in netstat_conn_res:

            for netstat_conn_item in netstat_conn_items:

                html += "<tr>"
                html += "<td>{proto}</td>" \
                        "<td>{laddr}</td>" \
                        "<td>{raddr}</td>" \
                        "<td>{status}</td>" \
                        "<td>{pid}</td>" \
                        "<td>{proc}</td>".format(**netstat_conn_item)
                html += "</tr>"

        html += "</table>"
        html += "<br>"

    html += "</body></html>"

    return html


if __name__ == "__main__":

    if len(sys.argv) == 2:
        app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)

    else:
        app.run(host='0.0.0.0', debug=True)
