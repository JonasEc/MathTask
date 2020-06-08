import random

from otree.api import (
    models,
    ExtraModel,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import itertools
import random
import time
from math import ceil

author = 'Jonas Mueller-Gastell'

doc = """
Math Section
"""


class Constants(BaseConstants):
    name_in_url = 'Riddle'
    players_per_group = 3
    num_rounds = 1

    # Wait Page Variables
    maxWait = 900  # seconds
    WaitPay = c(1.5)

    # Wait Within the Experiment
    TIMEWAITTEAMMATES = 150  # spend at most this time on match page
    minWait = 0.20  # spend at least this amount on the match page

    TimeMax = 300  # seconds max on riddle page

    ##Riddle Payment
    MathsBonus = c(0.1)


    namesW = ['Sarah', 'Jennifer', 'Mary']
    namesM = ['Peter', 'John', 'Robert']

    DictOfParameters = {'MathsBonus': float(MathsBonus),
                        }

    AssignBonus = c(1)
    AssignMax = 100
    ExtraBonusMax = c(2)
    PerPercent = c(0.02)
    QuadMultiplierPenalty = 25



class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            # if 'q' in self.session.config:
            #     for p in self.get_players():
            #         p.quest = self.session.config['q']
            # else:
            #     for p in self.get_players():
            #         p.quest = random.choice([0, 1])
            # for p in self.get_players():
            #     p.participant.vars['question'] = p.quest
            # for p in self.get_players():
            #     print('my question is', p.participant.vars['question'])
            for p in self.get_players():
                p.code = str(random.randint(0,1000))


class Group(BaseGroup):
    groupSolution = models.IntegerField()
    groupAnswer = models.IntegerField()
    groupScore = models.PositiveIntegerField(initial=0)
    groupCounter = models.IntegerField(initial=0)
    # game_finished = models.BooleanField(initial=False)
    # startTime = models.FloatField(initial=0)
    whoKick =models.StringField(initial='') 
    firstTime = models.FloatField()
    lastTime= models.FloatField(initial=0)
    start = models.BooleanField(initial=True)

    def timeStamp(self):
        return  str(int(ceil(10*(time.time() - self.firstTime ))))

    def nicknames(self, id_in_group):
        g = self.get_player_by_id(id_in_group)
        gender = g.gender
        if gender == 0:
            l = Constants.namesM[id_in_group - 1]
        else:
            l = Constants.namesW[id_in_group - 1]
        return l      

    def live_answer(self,  id_in_group, answer):
        playerSent = self.get_player_by_id(id_in_group)

        if answer.get('pageLoad'):
            self.firstTime = time.time()
            l = [random.choice([-3,-2,-1,1,2,3]) for k in range(9)]
            self.groupSolution = sum(l)
            self.lastTime = time.time()

            playerActive = self.get_player_by_id(1)
            if self.start:
                playerActive.actiontape  += 's_0.'   
            self.start = False
            gender = playerActive.gender
            hisher = gender*'her' + (1-gender)*'his'

            broadcast = {'matrix': l, 'counter': 1, 'incorrect': 'first', 'hisher': hisher, 
                         'name': self.nicknames(1), 'refresh': True}
            return {0: broadcast}   

        elif not answer.get('kick') and not answer.get('pageLoad'):
            self.start = False

            tape = 'a_' +  self.timeStamp()
            is_correct = (answer.get('answer') == self.groupSolution)
            if is_correct:
                self.groupScore  += 1 
                playerSent.personalCorrect += 1
                playerSent.lastCorrect = ""
                tape += '_c'
            else:
                playerSent.personalIncorrect += 1
                playerSent.lastCorrect = "in"
                tape += '_f'                
            playerSent.personalTotalTime += time.time() - self.lastTime
            playerSent.actiontape += tape + '.'

            l = [random.choice([-3,-2,-1,1,2,3]) for k in range(9)]
            self.groupSolution = sum(l)

            self.groupCounter += 1
            k = self.groupCounter
            self.whoKick  = ''
            self.lastTime = time.time()

            playerActive = self.get_player_by_id(self.groupCounter%3 + 1)
            playerActive.actiontape  += 's_' +  self.timeStamp() + '.'      
            gender = playerActive.gender
            hisher = gender*'her' + (1-gender)*'his' 

 
            broadcast = {'matrix': l, 'name': self.nicknames(k%3 +1), 'hisher': hisher, 
                        'incorrect': playerActive.lastCorrect , 'counter': k%3 +1, 'refresh': True}
            return {0: broadcast}

        elif answer.get('kick'):
            if str(id_in_group) in self.whoKick:
                return {id_in_group: {'msg': 'Message Received', 'refresh': False}}
            else:
                self.whoKick += str(id_in_group)
                playerSent.personalUsedKick  +=1 
 
                playerActive = self.get_player_by_id(self.groupCounter%3 + 1)
                playerActive.personalWasKickAttempt +=1
                playerSent.actiontape  += 'vk_' + self.timeStamp() + '_' + str(playerActive.gender) + '.'      


                if len(self.whoKick) == 2:
                    playerActive.actiontape  += 'i2k_' + self.timeStamp() + '_' + str(playerSent.gender) + '.'      
                    playerActive.personalWasKicked +=1
                    playerActive.personalTotalTime += time.time() - self.lastTime

                                    
                    l = [random.choice([-3,-2,-1,1,2,3]) for k in range(9)]
                    self.groupSolution = sum(l)
                    
                    self.groupCounter += 1
                    k = self.groupCounter
                    self.whoKick = ''
                    self.lastTime = time.time()


                    playerActive = self.get_player_by_id(k%3 +1)
                    playerActive.actiontape  += 's_' + self.timeStamp() + '.'      
                    gender = playerActive.gender
                    hisher = gender*'her' + (1-gender)*'his'


                    broadcast = {'matrix': l, 'name': self.nicknames(k%3 +1), 'hisher': hisher, 
                                'incorrect': playerActive.lastCorrect , 'counter': k%3 +1, 'refresh': True}
                    return {0: broadcast}       
                
                else:
                    playerActive.actiontape  += 'i1k_' +  self.timeStamp() + '_' + str(playerSent.gender) + '.'                          
                    return {id_in_group: {'msg': 'Message Received', 'refresh': False}}


# class Answers(ExtraModel):
#     player = models.Link(Player)
#     correctAnswers = models.PositiveIntegerField()    
#     incorrectAnswers = models.PositiveIntegerField()    
#     raisedKick = models.PositiveIntegerField()    
#     wasKicked = models.PositiveIntegerField()    


class Player(BasePlayer):
    code = models.StringField()
    gender = models.IntegerField(initial=0)

    genderOther1 = models.IntegerField()
    # ageOther1 = models.IntegerField()
    # musicOther1 = models.StringField()
    # colorOther1 = models.StringField()
    nameOther1 = models.StringField()

    genderOther2 = models.IntegerField()
    # ageOther2 = models.IntegerField()
    # musicOther2 = models.StringField()
    # colorOther2 = models.StringField()
    nameOther2 = models.StringField()

    quizperfw1 = models.IntegerField(min=0,max=20, label="How many of the 20 quiz questions do you think you answered correctly?")

    def chat_nickname(self):
        if self.gender == 0:
            return Constants.namesM[int(self.id_in_group) - 1]
        else:
            return Constants.namesW[int(self.id_in_group) - 1]

    def nameFinder(self, n):
        g = self.get_others_in_group()
        gender = g[n - 1].gender

        if gender == 0:
            return Constants.namesM[n - 1]
        elif gender == 1:
            return Constants.namesW[n - 1]

          

    # score = models.PositiveIntegerField()
    # answer = models.IntegerField()

    personalCorrect = models.PositiveIntegerField(initial=0)
    personalIncorrect = models.PositiveIntegerField(initial=0)
    personalTotalTime = models.FloatField(initial=0)
    personalUsedKick  = models.PositiveIntegerField(initial=0)
    personalWasKickAttempt =  models.PositiveIntegerField(initial=0)
    personalWasKicked =  models.PositiveIntegerField(initial=0)
    lastCorrect = models.StringField(initial="first")
    actiontape = models.StringField(initial ='')

    # def role(self):
    #     if self.id_in_group == 1:
    #         return 'First'
    #     elif self.id_in_group == 2:
    #         return 'Second'
    #     elif self.id_in_group == 3:
    #         return 'Third'



    percentMTurk = models.PositiveIntegerField(label='What percentage of your income comes from MTurk work?', min=0,
                                               max=100)
    education = models.PositiveIntegerField(label='What is your highest level of completed education?',
                                            choices=[[1, 'Some High School'], [2, 'High School Diploma/ GED'],
                                                     [3, "Some College/Associate's Degree"], [4, "Bachelor Degree"],
                                                     [5, "Graduate Degree"]], widget=widgets.RadioSelect)
    marital = models.PositiveIntegerField(label='What is your marital status?',
                                          choices=[[0, 'Single, Never Married'], [1, 'Married or domestic partnership'],
                                                   [2, 'Widowed/Divorced/Separated']], widget=widgets.RadioSelect)
    income = models.PositiveIntegerField(widget=widgets.RadioSelect,
                                         choices=[[0, 'Less than $10,000'], [1, 'Between $10,000 and $19,999'],
                                                  [2, '$20,000 to $29,999'], [3, '$30,000 to $39,999'],
                                                  [4, '$40,000 to $49,999'], [5, '$50,000 to $59,999'],
                                                  [6, '$60,000 to $69,999'], [7, '$70,000 to $79,999'],
                                                  [8, '$80,000 to $89,999'], [9, '$90,000 to $99,999'],
                                                  [10, '$100,000 to $149,999'], [11, 'More than $149,999']],
                                         label="What is your household's total combined income during the past 12 "
                                               "months? This includes money from jobs, net income from business, "
                                               "farm or rent, pensions, dividends, interest, Social Security payments "
                                               "and any other monetary income.")
    ethnic = models.PositiveIntegerField(widget=widgets.RadioSelect,
                                         choices=[[0, 'White'], [1, 'Black or African-American'],
                                                  [2, 'Hispanic or Latino'], [3, 'Asian/ Pacific Islander'],
                                                  [4, 'Native American or Alaskan Native'], [5, 'Other']],
                                         label='What is your ethnicity (or race)?')

    def completion_bonus(self):
        self.payoff = c(1)
