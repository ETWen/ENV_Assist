import telnetlib
host = "192.168.1.8"
user = "xtuser"
passwd = "82276611"

'''存放指令字串的陣列'''
command_arr = ["ls","exit"]

'''連接主機'''
tn = telnetlib.Telnet(host)
tn.set_debuglevel(2)
'''當程式讀到特定字串時，再將帳密送入'''
tn.read_until(b"imx6 login:")
tn.write(user.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(passwd.encode('ascii') + b"\n")

'''將指令依序傳入'''
for command in command_arr :
    tn.write(command.encode('ascii') + b"\n")

'''讀取全部輸入的東西'''
print(tn.read_all().decode('ascii'))
tn.close()
