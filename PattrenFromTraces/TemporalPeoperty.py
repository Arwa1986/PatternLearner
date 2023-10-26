class TemporalProperty:
    def __init__(self, e1, e2):
        self.event1 = e1
        self.event2 = e2
        # self.satisfy_1effect = False
        # self.satisfy_1cause = False
        # self.satisfy_causeFirst = False
        # self.strictest_pattern = ''
        # self.satisfactory_scour = 0

        self.pattern = ''
        self.counter = 0
        self.pattern_ratio = 0
        # self.selfloop_e1_count = 0
        # self.selfloop_e2_count = 0

    # def getCounter(self, patrn):
    #     if patrn == 'selfloop_e1':
    #         return self.selfloop_e1_count
    #     elif patrn == 'selfloop_e2':
    #         return self.selfloop_e2_count
    #
    # def setCounter(self, patrn, counter):
    #     if patrn == 'selfloop_e1':
    #         self.selfloop_e1_count = counter
    #     elif patrn == 'selfloop_e2':
    #         self.selfloop_e2_count = counter


    def calculate_ratio(self, numberOfTraces):
            self.pattern_ratio = (self.counter/numberOfTraces)*100

    def discover_stricest_pattren(self):
        p = ''
        if self.satisfy_1cause:
            p = 'OneCause'
            if self.satisfy_causeFirst:
                p = 'MultiEffect'
                if self.satisfy_1effect:
                    p = 'Alternating'
            elif self.satisfy_1effect:
                p = 'EffectFirst'
        elif self.satisfy_causeFirst:
                p = 'CauseFirst'
                if self.satisfy_1effect:
                    p = 'MultiCause'
        elif self.satisfy_1effect:
            p = 'OneEffect'
        self.strictest_pattern = p

    def print(self):
        print(f'Event1: {self.event1}')
        print(f'Event2: {self.event2}')
        # print(f'Pattren: {self.strictest_pattern}')
        # print(f'scour: {self.satisfactory_scour}')
        print(f'Pattren: {self.pattern}')
        print(f'scour: {self.pattern_ratio}')