from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from leavable_wait_page.pages import SkippablePage, LeavableWaitPage

import random
import time
from math import ceil





class Math(Page):
    def is_displayed(self):
        return self.player.participant.vars['eligible']

    live_method = 'live_answer'

    def get_timeout_seconds(self):
        return Constants.TimeMax
    timer_text = 'Time left for this quiz: '

        
    def vars_for_template(self):
        return {
                'chat_nickname': self.player.chat_nickname(),
                'id': self.player.id_in_group,
                }
     





class TEMP(SkippablePage):
    def is_displayed(self):
        return self.round_number == 1


    def vars_for_template(self):
        self.player.participant.vars['eligible'] = True
        self.player.participant.vars['gender'] = "Male"
        self.player.participant.vars['gender'] = "Female"*(random.random() > 0.5) 
        self.player.participant.vars['age'] = ceil(random.random()*70)
        self.player.participant.vars['favoriteMusic'] = "classic" + (random.random() >0.5) *' rock'
        self.player.participant.vars['favoriteColor'] = "green" + (random.random() >0.5) *' grass'
        return {}

class GroupWaitPage(LeavableWaitPage):
    def is_displayed(self):
        # return self.player.participant.vars['eligible'] and self.round_number == 1
        return self.round_number == 1

    group_by_arrival_time = True

    allow_leaving_after = Constants.maxWait


class GroupWaitPage2(WaitPage):
    def is_displayed(self):
        return self.player.participant.vars['eligible'] and self.round_number == 1


class Match(SkippablePage):
    def get_timeout_seconds(self):
        return Constants.TIMEWAITTEAMMATES

    def is_displayed(self):
        return self.player.participant.vars['eligible'] and self.round_number == 1


    def vars_for_template(self):
        # Variables to be displayed to the participants
        # First we get the participants gender carried over from survey app

        playersgender = self.player.participant.vars['gender']
        if playersgender == 'Male':
            self.player.gender = 0
        elif playersgender == 'Female':
            self.player.gender = 1

        # Now we get a list of all the other players in the group

        g = self.player.get_others_in_group()

        # We define the variables of the other two people by getting their answers from the survey

        gender1 = (g[0].participant.vars['gender'] == 'Female') * 1
        self.player.genderOther1 = gender1
        self.player.participant.vars['gender1'] = gender1
        age1 = g[0].participant.vars['age']
        # self.player.ageOther1 = age1
        # self.player.participant.vars['age1'] = age1
        music1 = g[0].participant.vars['favoriteMusic']
        # self.player.musicOther1 = music1
        # self.player.participant.vars['music1'] = music1
        color1 = g[0].participant.vars['favoriteColor']
        # self.player.colorOther1 = color1
        # self.player.participant.vars['color1'] = color1

        gender2 = (g[1].participant.vars['gender'] == 'Female') * 1
        self.player.genderOther2 = gender2
        self.player.participant.vars['gender2'] = gender2
        age2 = g[1].participant.vars['age']
        # self.player.ageOther2 = age2
        # self.player.participant.vars['age2'] = age2
        music2 = g[1].participant.vars['favoriteMusic']
        # self.player.musicOther2 = music2
        # self.player.participant.vars['music2'] = music2
        color2 = g[1].participant.vars['favoriteColor']
        # self.player.colorOther2 = color2
        # self.player.participant.vars['color2'] = color2

        # We get random names based off gender

        name1 = self.player.nameFinder(1)
        self.player.nameOther1 = name1
        self.player.participant.vars['name1'] = name1
        name2 = self.player.nameFinder(2)
        self.player.nameOther2 = name2
        self.player.participant.vars['name2'] = name2

        # Return all the variables to execute the functions about

        return {'age1': age1, 'gender1': gender1, 'color1': color1, 'music1': music1,
                'age2': age2, 'gender2': gender2, 'color2': color2, 'music2': music2,
                'n1': name1, 'n2': name2, 'yours': self.player.chat_nickname(),
                'mintime': 1000 * Constants.minWait,}# 'whichRole': self.player.role}


class PageToShowOnlyToParticipantsWhoExitedTheExp(Page):
    def is_displayed(self):
        a = self.participant.vars.get('go_to_the_end')
        if self.player.participant.vars['eligible'] == 0:
            a = False

        if a == True:
            return True and self.round_number == Constants.num_rounds
        else:
            return False and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.player.code = "LAW" + self.player.code
        code = self.player.code

        payoff = Constants.WaitPay
        self.player.payoff = Constants.WaitPay
        return {'payoff': payoff, 'code': code}



##### OLD PAGES, TO RE-INCLUDE

# class NextWeekInstruc(SkippablePage):
#     def is_displayed(self):
#         return self.player.participant.vars['eligible']

#     def vars_for_template(self):
#         return {
#             'chat_nickname': self.player.chat_nickname(),
#             'mintime': 1000*Constants.minWait
#         }

# class Survey1(SkippablePage):
#     def is_displayed(self):
#         return self.player.participant.vars['eligible']

#     form_model = 'player'
#     form_fields = ['income', 'percentMTurk', 'ethnic', 'education', 'marital']

#     def before_next_page(self):
#         self.player.completion_bonus()

# class QuizPerfW1(SkippablePage):
#     def is_displayed(self):
#         return self.player.participant.vars['eligible']

#     form_model = 'player'
#     form_fields = ['quizperfw1']


# class Results(SkippablePage):
#     def is_displayed(self):
#         return self.player.participant.vars['eligible']

#     def vars_for_template(self):
#         self.player.code = self.player.code + "FS"
#         code = self.player.code

#         return {'code': code,}


page_sequence = [ GroupWaitPage, TEMP, GroupWaitPage2, Math,]# NextWeekInstruc, QuizPerfW1, Survey1, Results, PageToShowOnlyToParticipantsWhoExitedTheExp]
