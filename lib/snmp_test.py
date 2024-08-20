from pysnmp.hlapi import *

def snmpset(ip, community, oid, value):
    """
    Send SNMPv1 set command to a device for a single OID.

    Parameters:
    - ip: str, IP address of the SNMP device.
    - community: str, SNMP community string.
    - oid: str, OID of the object to set.
    - value: int, value to set.

    Returns:
    - Tuple containing (errorIndication, errorStatus, errorIndex, varBinds).
    """

    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid).addAsn1MibSource(), Integer(value)))
    )

    if errorIndication:
        return (errorIndication, None, None, None)
    elif errorStatus:
        return (None, errorStatus, errorIndex, varBinds)
    else:
        return (None, None, None, varBinds)

def snmpget(ip, community, oid):
    """
    Send SNMPv1 get command to a device for a single OID.

    Parameters:
    - ip: str, IP address of the SNMP device.
    - community: str, SNMP community string.
    - oid: str, OID of the object to get.

    Returns:
    - Tuple containing (errorIndication, errorStatus, errorIndex, varBinds).
    """

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid).addAsn1MibSource()))
    )

    if errorIndication:
        return (errorIndication, None, None, None)
    elif errorStatus:
        return (None, errorStatus, errorIndex, varBinds)
    else:
        return (None, None, None, varBinds)

# Example usage:
ip_address = '192.168.1.20'
community_string = 'private'
oid_base = '.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2'
port = 1
set_value = 3

# Set example
set_oid = f'{oid_base}.{port}'
set_result = snmpset(ip_address, community_string, set_oid, set_value)

if set_result[0]:
    print(f"Set Error: {set_result[0]}")
elif set_result[1]:
    print(f"Set Error: {set_result[1].prettyPrint()} at {set_result[2]}")
else:
    for name, val in set_result[3]:
        print(f"Set {name.prettyPrint()} = {val.prettyPrint()}")

# Get example
get_oid = f'{oid_base}.{port}'
get_result = snmpget(ip_address, community_string, get_oid)
if get_result[0]:
    print(f"Get Error: {get_result[0]}")
elif get_result[1]:
    print(f"Get Error: {get_result[1].prettyPrint()} at {get_result[2]}")
else:
    for name, val in get_result[3]:
        print("test2")
        print(f"Get {name.prettyPrint()} = {val.prettyPrint()}")
