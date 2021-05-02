#Mohamadreza
class Process:
    
    Count = 1
    Names = set()

    def __init__(self, name:str, startTime:int, duringTime:int, weight:int=1):
        if name in Process.Names:
            raise Exception('Each process must have unique name')
        self.Name = name if name else "P{}".format(Process.Count)
        Process.Names.add(self.Name)
        Process.Count += 1
        self.StartTime = startTime
        self.DuringTime = duringTime
        self.Weight = weight
