import subprocess
import os
import time

class PDUCtrl:
    def __init__(self, ip):
        self.ip = ip
        #self.snmpset_path = os.path.join('gui','utils', 'Net_SNMP', 'snmpset.exe')
        self.snmpset_path = os.path.join('Net_SNMP', 'snmpset.exe')
        #print(self.snmpset_path)

    def execute_snmp_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                #print(result.stdout)
                return
            else:
                print(f"Error executing command: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Timeout expired while executing command.")

    def pdu_on(self, port):
        oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
        set_on_command = f'"{self.snmpset_path}" -v 1 -c private {self.ip} {oid} i 3'
        print(set_on_command)
        self.execute_snmp_command(set_on_command)

    def pdu_off(self, port):
        oid = f'.1.3.6.1.4.1.2468.1.4.2.1.3.2.4.1.2.{port}'
        set_off_command = f'"{self.snmpset_path}" -v 1 -c private {self.ip} {oid} i 4'
        print(set_off_command)
        self.execute_snmp_command(set_off_command)

    #def CheckConnection(self):
        

if __name__ == "__main__":
    pdu_ip = '192.168.1.20'
    pdu_ports = [1, 2, 3, 4]
    pdu_ctrl = PDUCtrl(pdu_ip)

    #pdu_ctrl.CheckConnection()

    
    pdu_ctrl.pdu_on(pdu_ports[0])
    pdu_ctrl.pdu_on(pdu_ports[1])
    pdu_ctrl.pdu_on(pdu_ports[2])
    pdu_ctrl.pdu_on(pdu_ports[3])

    time.sleep(10)

    '''
    pdu_ctrl.pdu_off(pdu_ports[0])
    pdu_ctrl.pdu_off(pdu_ports[1])
    pdu_ctrl.pdu_off(pdu_ports[2])
    pdu_ctrl.pdu_off(pdu_ports[3])
    '''
