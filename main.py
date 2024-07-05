from teams import Team
import random

def randomize_draw(stage,teams):
    used = []
    draws =[]
    draw = []
    if stage == "QF":
        while len(draws)<4:
            n1 = random.randint(0,7)
            n2 = random.randint(0,7)
            if n1 == n2 or n1 in used or n2 in used:
                n1 = random.randint(0,7)
                n2 = random.randint(0,7)
            else:
                used.append(n1)
                used.append(n2)
                draw = [teams[n1], teams[n2]]
                draws.append(draw)    
    
    if stage == "SF":
        while len(draws)<2:
            n1 = random.randint(0,3)
            n2 = random.randint(0,3)
            if n1 == n2 or n1 in used or n2 in used:
                n1 = random.randint(0,3)
                n2 = random.randint(0,3)
            else:
                used.append(n1)
                used.append(n2)
                draw = [teams[n1], teams[n2]]
                draws.append(draw)    

    return draws

def ro16_sim(n=1):
    Team.instantiate_from_csv_RO16()
    teams = Team.all
    through_histroy = {}
    for i in range(n):
        current_stage = "RO16"
        draws = [[teams[11],teams[12]], [teams[3],teams[14]], [teams[1],teams[10]], [teams[9],teams[6]], [teams[7],teams[0]], [teams[13],teams[8]], [teams[5],teams[2]], [teams[4],teams[15]]]
        through = []

        for game in draws:
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))

        for team in through:
            if team in through_histroy.keys():
                through_histroy[team] += 1
            else:
                through_histroy[team] = 1
        
    through_histroy_list = list(through_histroy.items()) #type: ignore
    for mx in range(len(through_histroy_list)-1, -1, -1):
        swapped = False
        for i in range(mx):
            if through_histroy_list[i][1] < through_histroy_list[i+1][1]:
                through_histroy_list[i], through_histroy_list[i+1] = through_histroy_list[i+1], through_histroy_list[i]
                swapped = True
        if not swapped:
            break
    
    return through_histroy_list, through #type:ignore

def real_life_qf_sim(n=100):
    Team.instantiate_from_csv_QF()
    teams = Team.all

    through_histroy = {}
    
    current_stage = "QF"
    draws = randomize_draw(stage=current_stage, teams=teams)
    
    user_input = str(input("\n[0] Real life draws  ||  [1] Randomized draws "))
    if user_input == "0":
        draws = [[teams[1],teams[6]], [teams[5],teams[3]], [teams[7],teams[2]], [teams[0],teams[4]]] #FIX THE NUMBERS
    

    for i in range(n):
        through = []
        for game in draws:
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))

        for team in through:
            if team in through_histroy.keys():
                through_histroy[team] += 1
            else:
                through_histroy[team] = 1
        
    through_histroy_list = list(through_histroy.items()) #type: ignore
    for mx in range(len(through_histroy_list)-1, -1, -1):
        swapped = False
        for i in range(mx):
            if through_histroy_list[i][1] < through_histroy_list[i+1][1]:
                through_histroy_list[i], through_histroy_list[i+1] = through_histroy_list[i+1], through_histroy_list[i]
                swapped = True
        if not swapped:
            break
    
    return through_histroy_list, through #type:ignore

def ro16_and_qf(n=100):
    through_histroy = {}

    for i in range(n):
        trash, teams = ro16_sim(int(n/4))
        current_stage = "QF"
        draws = randomize_draw(current_stage,teams)
    
        through = []
        for game in draws:
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))
        
        for team in through:
            if team in through_histroy.keys():
                through_histroy[team] += 1
            else:
                through_histroy[team] = 1
        
    through_histroy_list = list(through_histroy.items()) #type: ignore
    for mx in range(len(through_histroy_list)-1, -1, -1):
        swapped = False
        for i in range(mx):
            if through_histroy_list[i][1] < through_histroy_list[i+1][1]:
                through_histroy_list[i], through_histroy_list[i+1] = through_histroy_list[i+1], through_histroy_list[i]
                swapped = True
        if not swapped:
            break

    return through_histroy_list, through #type:ignore

def complete_simulation():
    Team.instantiate_from_csv_RO16()
    teams = Team.all

    winners = {}
    n = int(input("Insert the number of times you wish the UCL to be simulated: "))
    for i in range(n):
        # Simulating preestablished RO16
        current_stage = "RO16"
        draws = [[teams[11],teams[12]], [teams[3],teams[14]], [teams[1],teams[10]], [teams[9],teams[6]], [teams[7],teams[0]], [teams[13],teams[8]], [teams[5],teams[2]], [teams[4],teams[15]]]
        through = []

        for game in draws:
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))
        #print()

        # Randomizing QF draw
        current_stage = "QF"
        draws = randomize_draw(current_stage,through)
        through = []
        # Simulating QF
        for game in draws:
            #print(f"{game[0].name} vs {game[1].name}")
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))
        #print()
        
        # Randomizing SF draw
        current_stage = "SF"
        draws = randomize_draw(current_stage,through)
        through = []
        # Simulating QF
        for game in draws:
            #print(f"{game[0].name} vs {game[1].name}")
            through.append(Team.simulate(stage=current_stage,team1=game[0],team2=game[1]))
        #print()

        # Simulating final
        current_stage = "F"
        #print(f"THE GRAND FINAL: {through[0].name} vs {through[1].name}")
        winner = Team.simulate(stage=current_stage,team1=through[0],team2=through[1])
        #print(f"And the WINNER of the 2022/23 UEFFA Champions League is: {winner.name}!!") #type: ignore

        if winner in winners.keys():
            winners[winner] += 1
        else:
            winners[winner] = 1
        #print()

    winners_list = list(winners.items()) #type: ignore
    for mx in range(len(winners_list)-1, -1, -1):
        swapped = False
        for i in range(mx):
            if winners_list[i][1] < winners_list[i+1][1]:
                winners_list[i], winners_list[i+1] = winners_list[i+1], winners_list[i]
                swapped = True
        if not swapped:
            break
    
    for champion in winners_list:
        print(f"{champion[0].name} -> {round((champion[1]/n)*100,3)}%")
            
def main():
    print("[0] Complete simulation (from R016)\n[1] Round of 16\n[2] Quarter Finals\n[Q] Quit")
    user_input = input(str("Which part of the competition would you like to simulate? "))
    
    if user_input.lower() == "q":
        pass
    
    elif user_input == "0":    
        complete_simulation()
    
    elif user_input == "1": #RO16
        # Listing the teams
        '''print("\nThe teams that qualified for the Round of 16 are the following:")
        i=0
        for team in teams:
            print(i, team.name)
            i+=1
        print()
        '''
        #Simulation
        n = int(input("Insert the number of times you wish the RO16 to be simulated: "))
        simulation, trash = ro16_sim(n=n)
        for champion in simulation:
            print(f"{champion[0].name} -> {round((champion[1]/n)*100,3)}%")
    
    elif user_input == "2": #QF

        print("\n\n[0] Real life || [1] Simulated\n\n")
        user_input = str(input("The Round of 16 winners are: "))
        
        if user_input == "0":
            n = int(input("Insert the number of times you wish the QF to be simulated: "))
            simulation, trash = real_life_qf_sim(n=n)
            for champion in simulation:
                print(f"{champion[0].name} -> {round((champion[1]/n)*100,3)}%")
        
        elif user_input == "1":
            n = int(input("Insert the number of times you wish the QF to be simulated: "))
            simulation, trash = ro16_and_qf(n=n)
            for champion in simulation:
                print(f"{champion[0].name} -> {round((champion[1]/n)*100,3)}%")

        
    #print("Error: You didn't input any of the avove values, try typing what is shown in the box: e.g. 'Q' for 'Quit'")

'''def main():
    Team.instantiate_from_csv_QF()
    teams = Team.all
    
    i = 0
    for team in teams:
        print(i, team.name)
        i+=1'''

if __name__ == "__main__":
    main()