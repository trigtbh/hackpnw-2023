
class Schedule:
    def __init__(self):
        self.week = [[],[],[],[],[],[],[]] # each list inside the self.week list represents a day (starting from Mon -> Sun)
        for i in range(len(self.week)):
            for j in range(48):
                self.week[i].append("Break")
        
  
