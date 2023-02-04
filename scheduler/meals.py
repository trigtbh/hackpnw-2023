class Meals:
    def __init__(self, b_start, b_end, l_start, l_end, d_start, d_end):
        # the following variables contain the start and end time for all meals for every day of the week
        # since meals should be taken at the same time every day for health reasons, only 1 start and end time for each meal is needed
        # breakfast start time
        self.b_start = b_start
        # breakfast end time
        self.b_end = b_end
        # lunch start time
        self.l_start = l_start
        # lunch end time
        self.l_end = l_end
        # dinner start time
        self.d_start = d_start
        # dinner end time
        self.d_end = d_end
