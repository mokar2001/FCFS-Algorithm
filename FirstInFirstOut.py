#Mohamadreza
from typing import *
from time import time
import matplotlib.pyplot as plt
from matplotlib import style
from termcolor import colored
from ContextSwitch import *
from Process import *


def output(message, color, *style):
    print(colored(message, color, attrs=style))


class FirstInFirstOut:

    def __init__(self, processes:List[Process], contextSwitchTime=0, contextSwitchWeight=1):
        self.Processes = processes
        self.PureProcesses = processes
        self.Processes.sort(key=lambda p:(p.StartTime, p.Name))
        self.ContextSwitchTime = contextSwitchTime
        self.Count = len(processes)
        self.Busy = {}
        self.ContextSwitchWeight = contextSwitchWeight
        style.use('ggplot')
        self.SetStatus()
        self.maxTime = max(list(zip(*self.Busy.values()))[1])


    def GetWaitTimes(self):
        WaitTimes = {}
        CurrentTime = 0
        Processes = []
        for p in self.Processes:
            CurrentTime = max(p.StartTime, CurrentTime)
            WaitTimes[p] = CurrentTime - p.StartTime
            CurrentTime += p.DuringTime + self.ContextSwitchTime
        return WaitTimes


    def GetResponseTimes(self):
        Processes = self.GetWaitTimes()
        ResponseTimes = {}
        for p, wait in Processes.items():
            ResponseTimes[p] = wait + p.DuringTime
        return ResponseTimes


    def GetAverageOfWaitTimes(self) -> float:
        SumOfWaitTimes = sum(self.GetWaitTimes().values())
        return SumOfWaitTimes / self.Count


    def GetAverageOfResponseTimes(self) -> float:
        SumOfResponseTimes = sum(self.GetResponseTimes().values())
        return SumOfResponseTimes / self.Count

    
    def GetCondidateProcessAtTime(self, time):
        for process, interval in self.Busy.items():
            if interval[0] <= time <= interval[1]:
                return process if isinstance(process, Process) else process
        return None


    def DrawBusyTimeGraph(self, meanWeight=False):
        pair = []
        for i in range(0, self.maxTime+2):
            currentProcess = self.GetCondidateProcessAtTime(i)
            if currentProcess == None:
                pair.append((i, 0))
            else:
                pair.append((i, currentProcess.Weight))

        x, y = list(zip(*sorted(pair)))
        plt.plot(x, y, label='Weight')
        if meanWeight:
            plt.plot(x, [sum(y)/len(y)]*len(x), '-.',label='Mean of Weight')
        plt.title('Busy Time Graph')
        plt.xlabel('Time')
        plt.ylabel('Weight')
        plt.legend()
        plt.show()

        
    def DrawDetailsGraph(self, WaitMean=False, ResponseMean=False):
        x = list(range(self.Count))
        ResponseTimes = self.GetResponseTimes()
        WaitTimes = self.GetWaitTimes()
        WaitY = [WaitTimes[p] for p in self.PureProcesses]
        ResponseY = [ResponseTimes[p] for p in self.PureProcesses]
        WaitMeanY = [self.GetAverageOfWaitTimes() for p in self.PureProcesses]
        ResponseMeanY = [self.GetAverageOfResponseTimes() for p in self.PureProcesses]
        
        plt.plot(x, WaitY, '-o', label='Wait')
        plt.plot(x, ResponseY, '-o', label='Response')
        if WaitMean:
            plt.plot(x, WaitMeanY, '-.', label='Mean of Wait')
        if ResponseMean:
            plt.plot(x, ResponseMeanY, '--', label='Mean of Response')

        plt.title('Details Graph')
        plt.xticks([])
        plt.xlabel('Process')
        plt.ylabel('Time')
        plt.legend()
        plt.show()
        

    def SetStatus(self):
        WaitTimes = self.GetWaitTimes()
        ResponseTimes = self.GetResponseTimes()
        current = 0
        for process in self.Processes:
            wait = WaitTimes[process]
            during = process.DuringTime
            current = max(process.StartTime, current)
            Left = current
            current += during
            self.Busy[process] = (Left, current-1)
            Left = current
            current += self.ContextSwitchTime
            self.Busy[ContextSwitch(self.ContextSwitchTime, self.ContextSwitchWeight)] = (Left, current-1)
        self.HasBeenStatusCalled = True
            

    def Simulate(self):
        current = 0
        for i, process in enumerate(self.Processes):
            wait = self.GetWaitTimes()[process]
            response = self.GetResponseTimes()[process]
            if process.StartTime > current:
                output(f"Free | {process.StartTime - current}s", 'green')
            current = max(process.StartTime, current)
            output(f"{process.Name} started at {current}s | {current - process.StartTime}s Delay", 'yellow')
            current += process.DuringTime
            output(f"{process.Name} finished at {current}s | {wait + process.DuringTime}s Response", 'yellow')
            if i < self.Count-1:
                current += self.ContextSwitchTime
                output(f"ContextSwitch | {self.ContextSwitchTime}s", 'red')