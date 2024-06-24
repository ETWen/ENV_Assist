PATH %PATH%;C:\Program Files (x86)\Wireshark\
tshark -r tmppcap.pcap -V -T pdml > ax.xml
cls