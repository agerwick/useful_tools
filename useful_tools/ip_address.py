def is_public_ip_address(ip):
    return is_valid_ip_address(ip) and not is_reserved_ip_address(ip)

def is_valid_ip_address(ip):
    ip = ip.split('.')
    if len(ip) != 4:
        return False
    for i in ip:
        if not i.isdigit():
            return False
        if int(i) < 0 or int(i) > 255:
            return False
    return True

def is_reserved_ip_address(ip):
    ip = ip.split('.')
    if ip[0] == '0':
        return True
    if ip[0] == '10':
        return True
    if ip[0] == '100' and ip[1] == '64':
        return True
    if ip[0] == '127':
        return True
    if ip[0] == '169' and ip[1] == '254':
        return True
    if ip[0] == '172' and int(ip[1]) >= 16 and int(ip[1]) <= 31:
        return True
    if ip[0] == '192' and ip[1] == '0' and ip[2] == '0':
        return True
    if ip[0] == '192' and ip[1] == '0' and ip[2] == '2':
        return True
    if ip[0] == '192' and ip[1] == '88' and ip[2] == '99':
        return True
    if ip[0] == '192' and ip[1] == '168':
        return True
    if ip[0] == '198' and int(ip[1]) >= 18 and int(ip[1]) <= 19:
        return True
    if ip[0] == '198' and ip[1] == '51' and ip[2] == '100':
        return True
    if ip[0] == '203' and ip[1] == '0' and ip[2] == '113':
        return True
    if ip[0] == '224':
        return True
    if ip[0] == '233' and ip[1] == '252' and ip[2] == '0':
        return True
    if ip[0] == '240':
        return True
    if ip[0] == '255' and ip[1] == '255' and ip[2] == '255' and ip[3] == '255':
        return True
    return False

"""
reference:
https://en.wikipedia.org/wiki/Reserved_IP_addresses
0.0.0.0/8	0.0.0.0–0.255.255.255	16777216	Software	Current (local, "this") network[1]
10.0.0.0/8	10.0.0.0–10.255.255.255	16777216	Private network	Used for local communications within a private network[3]
100.64.0.0/10	100.64.0.0–100.127.255.255	4194304	Private network	Shared address space[4] for communications between a service provider and its subscribers when using a carrier-grade NAT
127.0.0.0/8	127.0.0.0–127.255.255.255	16777216	Host	Used for loopback addresses to the local host[1]
169.254.0.0/16	169.254.0.0–169.254.255.255	65536	Subnet	Used for link-local addresses[5] between two hosts on a single link when no IP address is otherwise specified, such as would have normally been retrieved from a DHCP server
172.16.0.0/12	172.16.0.0–172.31.255.255	1048576	Private network	Used for local communications within a private network[3]
192.0.0.0/24	192.0.0.0–192.0.0.255	256	Private network	IETF Protocol Assignments, DS-Lite (/29)[1]
192.0.2.0/24	192.0.2.0–192.0.2.255	256	Documentation	Assigned as TEST-NET-1, documentation and examples[6]
192.88.99.0/24	192.88.99.0–192.88.99.255	256	Internet	Reserved.[7] Formerly used for IPv6 to IPv4 relay[8] (included IPv6 address block 2002::/16).
192.168.0.0/16	192.168.0.0–192.168.255.255	65536	Private network	Used for local communications within a private network[3]
198.18.0.0/15	198.18.0.0–198.19.255.255	131072	Private network	Used for benchmark testing of inter-network communications between two separate subnets[9]
198.51.100.0/24	198.51.100.0–198.51.100.255	256	Documentation	Assigned as TEST-NET-2, documentation and examples[6]
203.0.113.0/24	203.0.113.0–203.0.113.255	256	Documentation	Assigned as TEST-NET-3, documentation and examples[6]
224.0.0.0/4	224.0.0.0–239.255.255.255	268435456	Internet	In use for multicast[10] (former Class D network)
233.252.0.0/24	233.252.0.0–233.252.0.255	256	Documentation	Assigned as MCAST-TEST-NET, documentation and examples (Note that this is part of the above multicast space.)[10][11]
240.0.0.0/4	240.0.0.0–255.255.255.254	268435455	Internet	Reserved for future use[12] (former Class E network)
255.255.255.255/32	255.255.255.255	1	Subnet	Reserved for the "limited broadcast" destination address[1]
"""
