class Run:
    def can_run(self):
        return 'I can run'
    def sports(self):
        return 'Run'

class Swim:
    def can_swim(self):
        return 'I can swim'
    def sports(self):
        return 'Swim'

class Ride:
    def can_ride(self):
        return 'I can ride'
    def sports(self):
        return 'Ride'

class Triatlon(Run,Swim,Ride):
    pass
if __name__ =='__main__':
    a =Triatlon()
    print(isinstance(a, Run), isinstance(a, Swim), isinstance(a, Ride), isinstance(a, int))

    print(a.sports())
    print(Triatlon.mro())