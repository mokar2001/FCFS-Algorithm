from FirstInFirstOut import *
from Process import *

p1 = Process('Notepad', 0, 3)
p2 = Process('Taskmgr', 1, 3)
p3 = Process('Explore', 4, 3)
p4 = Process('VPlayer', 6, 2)

cpu = FirstInFirstOut([p1, p2, p3, p4], 0, 0)

cpu.Simulate()
print('Wait:', cpu.GetAverageOfWaitTimes())
print('Response:',cpu.GetAverageOfResponseTimes())
print('3s:', cpu.GetCondidateProcessAtTime(3).Name)
cpu.DrawDetailsGraph(WaitMean=True, ResponseMean=True)
cpu.DrawBusyTimeGraph(meanWeight=True)