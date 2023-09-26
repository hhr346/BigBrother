import subprocess
import re
import operator
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

# 这将返回命令的输出结果作为字节字符串。
output = subprocess.check_output(['last'])

# Extract usernames and time spent, return a list
lines = output.decode().split('\n')
users = [line.split()[0] for line in lines[:-3] if line]
time_last = [line.split()[9] for line in lines[:-3] if line]

# Do the time extract
digits = [re.findall(r"\d+", i) for i in time_last]
index = np.array(np.where([len(digit)==2 for digit in digits]))[0].tolist()
users = [users[i] for i in index]
time_slots = [timedelta(hours=int(digits[i][0]), minutes=int(digits[i][1])) for i in index]


# Do the sum
print(len(users), len(time_slots))
slot_total = {}
for user, time_slot in zip(users, time_slots):
  #print(f'{user:10} %10s' %time_slot)
  if user in slot_total:
    slot_total[user] += time_slot
  else:
    slot_total[user] = time_slot
# Do the sorting
slot_total = sorted(slot_total.items(), key=operator.itemgetter(1), reverse=True)
# 这将返回一个字典对象，其中键是用户名，值是对应的活动次数。
user_activity = Counter(users)
login_total = sorted(user_activity.items(), key=operator.itemgetter(1), reverse=True)

print('Here is the online time')
i = 1
# for user, count in slot_total.items():
for user, count in slot_total:
    print('%2d User: %10s, Activity Count: %s' %(i, user, count))
    i += 1


print('\n Here is the login times')
# It shows how many times has the user log in the system
i = 1
for user, count in login_total:
    print('%2d User: %10s, Activity Count: %4d' %(i, user, count))
    i += 1


#output = subprocess.check_output(['ps', 'aux'])
output = subprocess.check_output(['ps', '-ef'])
lines = output.decode().split('\n')
users = [line.split()[0] for line in lines[:] if line]
user_activity = Counter(users)
command_total = sorted(user_activity.items(), key=operator.itemgetter(1), reverse=True)
print('\n Here is the command numbers')
# It shows how many times has the user log in the system
i = 1
for user, count in command_total:
    print('%2d User: %10s, Activity Count: %4d' %(i, user, count))
    i += 1

