from questions import quiz
import random
import json

def initial_message():

    # initiate the game, introduce the rules and wait for the user to start the questionnaire
    print("\n")
    print("##################################################################################")
    print("###                                                                            ###")
    print("###                  Welcome to this Contest about Marvel!                     ###")
    print("###   Are you ready to test your knowledge about the Marvel Universe?          ###")
    print("###    There are 5 categories, each one harder than the previous one!          ###")
    print("### You have to answer correctly the question of a category to upgrade!        ###")
    print("###                For each correct answer, you earn coins!                    ###")
    print("### Also, you can end the game before answer any question and keep your score! ###")
    print("###                                                                            ###")
    print("##################################################################################\n")
    input("    Press any key to start the contest ... \n")

    return True

class player:
    def __init__(self, name):
        self.player_name = name
        self.score=0

    def currentScore(self, new_score):
        self.score = new_score
        return self.score

    def savedataLog(self, points=True):
        players_data= readFile("game_data.json")
        if self.player_name not in players_data.keys():
            players_data[self.player_name] = {'score': self.score}
        else:
            if points==False:
                players_data[self.player_name]['score'] = players_data[self.player_name]['score'] + 0
            else:
                players_data[self.player_name]['score'] = players_data[self.player_name]['score'] + self.score
        writeFile("game_data.json", players_data)
        return players_data[self.player_name]['score']

    def checkUser(self):
        players_data= readFile("game_data.json")
        if self.player_name not in players_data.keys():
            print("\n    Hello New Player "+self.player_name)
        else:
            print("\n    Hello "+self.player_name)
            print("\n    You have "+str(players_data[self.player_name]['score'])+" coins.")

class category:
    def __init__(self, cat_name):
        self.cat_name= cat_name
        self.incr=0
        self.cat_names= {"Very Easy":0, "Easy":6, "Medium":12, "Hard":18, "Very Hard":24}

    def defineRound(self):
        for categories in self.cat_names:
            if self.cat_name == categories: self.incr+=self.cat_names[categories]
        return self.incr

def showQuestion(incr, difficulty):
    init_pos = random.randrange(1,7)
    position = incr + init_pos
    print("\n    Category "+quiz[position]['category']+":\n")
    print("    Coins that gives: "+str(cat.cat_names[difficulty]+6)+"\n")
    print("    "+quiz[position]['question']+"\n")
    return position

def readFile(file_name):
    players= open(file_name, "r")
    players_data = json.load(players)
    return players_data

def writeFile(file_name, players_data):
    players= open(file_name, "w")
    json.dump(players_data, players)
    players.close()

class options():
    def __init__(self):
        self.possible_opts= ['option1', 'option2', 'option3', 'answer']
        self.opts_level = ['A', 'B', 'C', 'D']

    def showOptions(self, question_pos):
        random.shuffle(self.possible_opts)
        for ans_level in range(0,4):
            print("        "+self.opts_level[ans_level]+". "+quiz[question_pos][self.possible_opts[ans_level]])
            if self.possible_opts[ans_level] == 'answer': correct_answer=self.opts_level[ans_level]
        return correct_answer

def verifyAnswer(correct_ans, user_ans, incr, cat_weight):
    if user_ans == correct_ans:
        print("\n    That's Correct! ")
        return user.currentScore(cat_weight+6)

    else:
        return False

def EndGame(): # (like the movie)
        print("\n    #######################")
        print("    ###    GAME OVER!   ###")
        print("    #######################\n")

# START THE GAME!
intro = initial_message()
while True:

    user_name = input("    Please, introduce your name: ")
    user = player(user_name)
    user.checkUser()
    game_difficulty= ["Very Easy","Easy","Medium","Hard","Very Hard"]
    coins=0
    for difficulty in game_difficulty:
        cat = category(difficulty)
        incr= cat.defineRound()
        keep_game= input("\n    If wanna keep playing press 'Y' key, otherwise press any other key: ")
        if keep_game =="Y":
            question_pos= showQuestion(incr, difficulty)
            opts = options()
            correct_ans= opts.showOptions(question_pos)
            user_ans= input("\n    Your response is (A, B, C or D?) : ")
            cat_weight= coins+incr
            coins= verifyAnswer(correct_ans, user_ans, incr, cat_weight)
            if coins == False:
                print("\n    Sorry, wrong answer :( ")
                print("    You're in the EndGame")
                player_score = user.savedataLog(coins)
                print("\n    "+user.player_name+" coins: "+str(player_score))
                EndGame()
                break
            elif coins == 90:
                player_score = user.savedataLog()
                print("\n    Congratulations!!!!! You are a truly expert of the Marvel Universe")
                print("\n    "+user.player_name+" coins: "+str(player_score))
                EndGame()
                break
        else:
            player_score = user.savedataLog()
            print("\n    "+user.player_name+" coins: "+str(player_score))
            EndGame()
            break
    break
