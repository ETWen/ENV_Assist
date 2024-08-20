from pysnmp.hlapi import *
import time

class PDUCmd:
	def __init__(self, model ,ip):
		self.model = model
		self.ip = ip

	def _snmpset(self, ip, community, oid, value):
		"""
		Send SNMPv1 set command to a device for a single OID.

		Parameters:
		- ip: str, IP address of the SNMP device.
		- community: str, SNMP community string.
		- oid: str, OID of the object to set.
		- value: int or str, value to set.

		Returns:
		- Tuple containing (errorIndication, errorStatus, errorIndex, varBinds).
		"""
		if isinstance(value, int):
			value_type = Integer(value)
		elif isinstance(value, str):
			value_type = OctetString(value)
		else:
			raise ValueError("Unsupported value type. Must be int or str.")

		errorIndication, errorStatus, errorIndex, varBinds = next(
			setCmd(	SnmpEngine(),
					CommunityData(community, mpModel=0),
					UdpTransportTarget((ip, 161)),
					ContextData(),
					ObjectType(ObjectIdentity(oid).addAsn1MibSource(), value_type))
		)

		if errorIndication:
			return (errorIndication, None, None, None)
		elif errorStatus:
			return (None, errorStatus, errorIndex, varBinds)
		else:
			return (None, None, None, varBinds)

	def _snmpget(self, ip, community, oid):
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
			getCmd(	SnmpEngine(),
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
	'''
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
	'''

	def SetPduPortOn(self, port):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
		set_result = self._snmpset(self.ip, "private", oid, 3)

	def SetPduPortOff(self, port):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
		set_result = self._snmpset(self.ip, "private", oid, 4)

	def SetPduPortName(self, port, name):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.2.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.2.{port}'
		set_result = self._snmpset(self.ip, "private", oid, name)

	def SetPduPortLoc(self, port, loc):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.3.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.3.{port}'
		set_result = self._snmpset(self.ip, "private", oid, loc)

	def GetPduPortSate(self, port):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.2.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.2.{port}'
		get_result = self._snmpget(self.ip, "private", oid)

		for name, val in get_result[3]:
			value = val.prettyPrint()
		
		if val.prettyPrint() == "3":
			return True
		elif val.prettyPrint() == "2":
			return False
		else:
			return None

	def GetPduPortName(self, port):	#Port Name
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.2.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.2.{port}'
		get_result = self._snmpget(self.ip, "private", oid)

		for name, val in get_result[3]:
			value = val.prettyPrint()
		return value

	def GetPduPortLoc(self, port):	#Port Name
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.3.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.2.1.3.{port}'
		get_result = self._snmpget(self.ip, "private", oid)

		for name, val in get_result[3]:
			value = val.prettyPrint()
		return value

	def GetPduPortCurrent(self, port):	#Unit: mA
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.3.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.3.{port}'
		get_result = self._snmpget(self.ip, "private", oid)

		for name, val in get_result[3]:
			value = val.prettyPrint()
		return value

	def GetPduPortPower(self, port):	#Unit: 0.1W
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.5.{port}'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.3.1.5.{port}'
		get_result = self._snmpget(self.ip, "private", oid)

		for name, val in get_result[3]:
			value = val.prettyPrint()
		return value

	def GetPduName(self):
		if self.model == "iPoMan II":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.1.4'
		elif self.model == "iPoMan III":
			oid = f'.1.3.6.1.4.1.2468.1.4.2.1.1.4'
		get_result = self._snmpget(self.ip, "private", oid)
		for name, val in get_result[3]:
			value = val.prettyPrint()
		return value

	def CheckConnection(self):
		try:
			status = self.GetPduName()
			if status == "PDU":
				#print(status)
				return True
			else:
				return False
		except Exception as e:
			print(f"An error occurred while checking PDU iPoMan connection: {e}")
			return False

if __name__ == "__main__":
	pdu_model = "iPoMan II"
	pdu_ip = "192.168.1.20"
	pdu_ctrl = PDUCmd(pdu_model,pdu_ip)
	pdu_port = 1

	print(f"PDU port {pdu_port} on")
	pdu_ctrl.SetPduPortOn(1)
	pdu_ctrl.SetPduPortName(1,"PSU1")
	pdu_ctrl.SetPduPortLoc(1,"DUT1")
	time.sleep(1)

	print(pdu_ctrl.CheckConnection())
	print(f"Power State: {pdu_ctrl.GetPduPortSate(1)}")
	print(f"Port Name: {pdu_ctrl.GetPduPortName(1)}")
	print(f"Port Location: {pdu_ctrl.GetPduPortLoc(1)}")
	print(f"Port Current: {pdu_ctrl.GetPduPortCurrent(1)}")
	print(f"Port Power: {pdu_ctrl.GetPduPortPower(1)}")

	time.sleep(10)
	print(f"PDU port {pdu_port} off")
	#pdu_ctrl.SetPduPortOff(1)
	#time.sleep(1)

	#print(pdu_ctrl.GetPduPortSate(1))

