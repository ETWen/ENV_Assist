import time
import NuPython
import nuconst
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
print ('Connect to Nuserver......')
nscmd.server_connect('192.168.1.8')
print ('Wait for 3 seconds to Process Information Report......')
time.sleep(3)
port1_idx = nscmd.get_portidx(0,3,1)
port2_idx = nscmd.get_portidx(0,3,2)
# lock port
nscmd.port_mark(0, 3, 1)
nscmd.port_mark(0, 3, 2)
nscmd.port_lock()


# transmit config. setting
nscmd.config_stream_pktlen(512)
nscmd.clear_counter_port(port1_idx)
nscmd.clear_counter_port(port2_idx)


tx_p1 = nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)
tx_p2 = nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)
rx_p1 = nscmd.get_counter_port(port1_idx, nsconst. IDX_PORTCOUNTER_RX_RATE_PKT)
rx_p2 = nscmd.get_counter_port(port2_idx, nsconst. IDX_PORTCOUNTER_RX_RATE_PKT)
print("=== Clear counter ===")
print ("Port 1 Send:%i Received:%i" % (tx_p1, rx_p1))
print ("Port 2 Send:%i Received:%i" % (tx_p2, rx_p2))


# protocol
nscmd.config_stream_smac("00:22:A2:00:03:01")
nscmd.config_stream_dmac("00:22:A2:00:03:02")
nscmd.config_stream_utilization(100)
nscmd.config_stream_protocol(0)
# set total streams number
nscmd.config_stream_streamnum(2)
# set stream 1
nscmd.set_stream(port1_idx, 0)
nscmd.set_stream(port1_idx, 1)
# set stream 2
nscmd.set_stream(port2_idx, 0)
nscmd.set_stream(port2_idx, 1)

# Trans Packets
nscmd.config_tx_txtime(5)
#nscmd.config_tx_txpkts(500)
nscmd.transmit_pkts(port1_idx)
nscmd.transmit_pkts(port2_idx)

#time.sleep(5)

# Stop Trans Packets
nscmd.transmit_pkts_stop(port1_idx)
nscmd.transmit_pkts_stop(port2_idx)

time.sleep(5)

tx_pkt_p1 = nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)
tx_pkt_p2 = nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)
tx_pkt_byte_p1 = nscmd.get_counter_port(port1_idx, nsconst. IDX_PORTCOUNTER_TX_BYTE)
tx_pkt_byte_p2 = nscmd.get_counter_port(port2_idx, nsconst. IDX_PORTCOUNTER_TX_BYTE)
tx_pkt_rate_p1 = nscmd.get_counter_port(port1_idx, nsconst. IDX_PORTCOUNTER_TX_RATE_PKT)
tx_pkt_rate_p2 = nscmd.get_counter_port(port2_idx, nsconst. IDX_PORTCOUNTER_TX_RATE_PKT)

rx_pkt_p1 = nscmd.get_counter_port(port1_idx, nsconst. IDX_PORTCOUNTER_RX_GOODPKT)
rx_pkt_p2 = nscmd.get_counter_port(port2_idx, nsconst. IDX_PORTCOUNTER_RX_GOODPKT)
rx_pkt_byte_p1 = nscmd.get_counter_port(port1_idx, nsconst. IDX_PORTCOUNTER_RX_GOODPKT)
rx_pkt_byte_p2 = nscmd.get_counter_port(port2_idx, nsconst. IDX_PORTCOUNTER_RX_GOODPKT)


print("=== Show counter ===")
print("Port 1\t\tPort2")
print ("TX Packets: %i \t\t %i " % (tx_pkt_p1, tx_pkt_p2))
print ("TX Bytes  : %i \t\t %i " % (tx_pkt_byte_p1, tx_pkt_byte_p2))
print ("TX Packet Rate : %i \t\t %i " % (tx_pkt_rate_p1, tx_pkt_rate_p2))

print ("RX Packets: %i \t\t %i " % (rx_pkt_p1, rx_pkt_p2))


nscmd.port_unlock()
time.sleep(1)
nscmd.server_disconnect()