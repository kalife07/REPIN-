class Exercice:
    def __init__(self,name, reps, sets, rest_time, weight ):
        self.name = name
        self.reps = reps
        self.sets = sets
        self.rest_time = rest_time
        self.weight = weight
    

    def to_dict(self):
        return {
            "name": self.name,
            "reps": self.reps,
            "sets": self.sets,
            "rest_time": self.rest_time,
            "weight": self.weight
        }
