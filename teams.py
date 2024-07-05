import csv
import random

#IDEA: add team types (i.e. posession, counter attack, etc) and and bonus and disadvantages (i.e. counter attack beating posession teams more easily) USE: https://bit.ly/3G4nGx8
#Still need to simulate unpredictability (maybe rng…) 

class Team:
    all = []
    def __init__(self, name, ga, gf, pos, attsh, defsh, rating, RO16, QF, SF, F, ucl):

        #Assing name to self object
        self.name = name

        # Assing stats (per game) to self object
        self.ga = ga
        self.gf = gf
        self.pos = pos
        self.attsh = attsh
        self.defsh = defsh
        self.rating = rating

        # Assing appearances in the las 13 seasons to self object
        self.RO16 = RO16
        self.QF = QF
        self.SF = SF
        self.F = F
        self.ucl = ucl

        # Appending all instances into all[]
        Team.all.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', ga={self.ga}, gf={self.gf},pos={self.pos},attsh={self.attsh},defsh={self.defsh}, RO16={self.RO16}, QF={self.QF}, SF={self.SF}, F={self.F}, ucl={self.ucl}, rating={self.rating})"
    
    @classmethod
    def instantiate_from_csv_RO16(cls):
        with open('teams_ro16.csv', 'r') as f:
            reader = csv.DictReader(f)
            teams = list(reader)

        for team in teams:
            Team(
                name=team.get('name'),
                ga=float(team.get('ga')), # type: ignore
                gf=float(team.get('gf')), # type: ignore
                pos=float(team.get('pos')), # type: ignore
                attsh=float(team.get('attsh')), # type: ignore
                defsh=float(team.get('defsh')), # type: ignore
                RO16=float(team.get('RO16')), # type: ignore
                QF=float(team.get('QF')), # type: ignore
                SF=float(team.get('SF')), # type: ignore
                F=float(team.get('F')), # type: ignore
                ucl=float(team.get('ucl')) # type: ignore
            )
    
    @classmethod
    def instantiate_from_csv_QF(cls):
        with open('teams_qf.csv', 'r') as f:
            reader = csv.DictReader(f)
            teams = list(reader)

        for team in teams:
            Team(
                name=team.get('name'),
                ga=float(team.get('ga')), # type: ignore
                gf=float(team.get('gf')), # type: ignore
                pos=float(team.get('pos')), # type: ignore
                attsh=float(team.get('attsh')), # type: ignore
                defsh=float(team.get('defsh')), # type: ignore
                RO16=float(team.get('RO16')), # type: ignore
                QF=float(team.get('QF')), # type: ignore
                SF=float(team.get('SF')), # type: ignore
                F=float(team.get('F')), # type: ignore
                ucl=float(team.get('ucl')), # type: ignore
                rating=float(team.get('rating')) # type: ignore
            )

    #Calculate R -> R(probability of winning) = ((gf*pos*attsh)/(ga*defsh))*0.01
    def ratio(self):
        return ((self.gf*self.attsh*self.pos)/(self.ga*self.defsh))*0.01
    
    # Probability = R + (number appearances)*0.1
    # if Final->Probability = R + (number appearances)*0.1 + ucl*0.5
    @classmethod
    def simulate(cls,stage,team1,team2):
        # RO16
        if stage == "RO16":
            team1.probability = Team.ratio(team1) + team1.RO16*0.1 + random.randint(0,1)
            team2.probability = Team.ratio(team2) + team2.RO16*0.1 + random.randint(0,1)
        # QF
        elif stage == "QF":
            team1.probability = Team.ratio(team1)*team1.rating*0.1 + team1.QF*0.1 + random.randint(0,3)
            team2.probability = Team.ratio(team2)*team2.rating*0.1 + team2.QF*0.1 + random.randint(0,3)
        # SF
        elif stage == "SF":
            team1.probability = Team.ratio(team1) + team1.SF*0.1 + random.randint(0,6)
            team2.probability = Team.ratio(team2) + team2.SF*0.1 + random.randint(0,6)
        # F
        elif stage == "F":
            team1.probability = Team.ratio(team1) + team1.F*0.1 + team1.ucl*random.uniform(0,2) + random.randint(0,10)
            team2.probability = Team.ratio(team2) + team2.F*0.1 + team2.ucl*random.uniform(0,2) + random.randint(0,10)
            #print(f"{team1.name} -> {round(team1.probability, 2)} vs {team2.name} -> {round(team2.probability, 2)}")

        if team1.probability > team2.probability:
            return team1
        elif team1.probability == team2.probability:
            print("DEVELOPER NOTE: there has been a draw, rng is not yet implemented, please wait")
        elif team1.probability < team2.probability:
            return team2

            

    '''
    #calculate goal difference
    def goal_difference(self):
        return self.gf-self.ga
    
    #calculate goal ratio -> goal scored per goal conceded
    def goal_ratio(self):
        return self.gf/self.ga
    '''
