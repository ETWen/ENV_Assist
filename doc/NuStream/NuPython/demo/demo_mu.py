import mu_framework
import mu_const

# 0. declaration
testmu = mu_framework.MUTest()
const = mu_const.MUConst()

# 1. Connect to NuServer, default ip is 127.0.0.1. If success, list all ports
testmu.set_serverip("192.168.1.8")
testmu.ns_connect()
# 2. Add new window
testmu.add_window(1)
# 3. Add task to window. Task ID is from mu_const
win_idx = 0
testmu.list_window[win_idx].add_task(const.SHOWSTRING)
testmu.list_window[win_idx].add_task(const.PT2_BC_100F)
testmu.list_window[win_idx].add_task(const.PT2_CRC_1G)
# 4. Add port pair to task if this task is run with Xtramus RM module
task_idx = 1
testmu.list_window[win_idx].list_task[task_idx].portpair_add(1, 2)
# means bi-direction
testmu.list_window[win_idx].list_task[task_idx].portpair_add(2, 1)

# 4.1 Show the task name of window
#testmu.list_window[win_idx].show_task_name()
# 4.2 Show the task info. of window
#testmu.list_window[win_idx].show_task_setting()

# 5. Run window and auto show the result message while finish.
testmu.run_window(win_idx)
# 6. Disconnect to NuServer
testmu.ns_disconnect()