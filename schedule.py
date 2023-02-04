
class Schedule:
    def __init__(self):
        self.week = [[],[],[],[],[],[],[]] # each list inside the self.week list represents a day (starting from Mon -> Sun)
        for i in range(len(self.week)):
            for j in range(48):
                self.week[i].append(None)
        
    def __str__(self):
        date = 0
        for day in self.week:
            curtime = 0
            for time in day:
                if time:
                    print(str(date) + str(curtime) + time.name)
                # else:
                #     print(str(day) + str(time) + "break")
                curtime += 1
            date += 1
  