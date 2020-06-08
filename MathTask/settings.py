from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

'''
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.50, doc="",
    mturk_hit_settings=dict(
        keywords='bonus, study, research, fun, riddle, cooperative, quiz, trivia, team',
        title='Research Study Involving Team Work on Riddles. BONUS UP TO $19.50; Average Time 35min Across Two '
              'Sessions',
        description='In this study, you will answer some survey questions and try to solve a fun riddle with other MTurkers -- Total Bonus payment is UP TO $19.50, Average Bonus $11.50; Average Time 35min. One session now and one session in three days.',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=75,
        expiration_hours=6,
        qualification_requirements=[{
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
            {
                'QualificationTypeId': "00000000000000000040",  ### number of HITs
                'Comparator': "GreaterThan",
                'IntegerValues': [1000]
            },
            {
                'QualificationTypeId': "000000000000000000L0",  ### percentage accept of HITs
                'Comparator': "GreaterThan",
                'IntegerValues': [97]
            },
            {
                'QualificationTypeId': "3Z2GNG0CT8ISBEMCTX0VD5RZWR1XWL",  ### prevent retakers
                'Comparator': "DoesNotExist"
            }
        ],
        grant_qualification_id='3Z2GNG0CT8ISBEMCTX0VD5RZWR1XWL',  # to prevent retakes
    )
)


'''

# For week 2
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=3.00, doc="",
    mturk_hit_settings=dict(
        keywords='bonus, study, research, fun, cooperative, quiz, trivia, team',
        title='Second Session of Research study on team work on problem solving. Average time 10 minutes.',
        description='This is the follow up for the session which was completed three days ago. Average time 10 minutes. Earn additional bonuses.',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=26,
        qualification_requirements=[{
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
            {
                'QualificationTypeId': "00000000000000000040",  ### number of HITs
                'Comparator': "GreaterThan",
                'IntegerValues': [1000]
            },
            {
                "QualificationTypeId": "3N6NATQOCRH8FDZD0PUXB036YEP8EA", ##Participated in first part
                "Comparator": "Exists"
            },
            {
                'QualificationTypeId': "3SEZZHS5L895351BPCYPFD8QX589A4",  ### prevent retakers
                'Comparator': "DoesNotExist"
            }
        ],
        grant_qualification_id='3SEZZHS5L895351BPCYPFD8QX589A4',  # to prevent retakes
    )
)


SESSION_CONFIGS = [
    # dict(
    #     name='WeekOne',
    #     display_name="Week One",
    #     app_sequence=['Captcha', 'startsurvey', 'quizz_two', 'stumpers'],
    #     #q=3,
    #     quiztime=15,
    #     num_demo_participants=3,
    # ),
    dict(
        name='math',
        display_name="math",
        app_sequence=['maths'],
        num_demo_participants=3,
        #q=3,
    ),
    # dict(
    #     name='everything',
    #     display_name="Everything",
    #     app_sequence=['Captcha','startsurvey', 'quizz_two', 'stumpers','weektwo'],
    #     num_demo_participants=3,
    #     quiztime=15,
    #     #q=3,
    # ),
    # dict(
    #     name="week2",
    #     display_name="OnlyWeek2",
    #     num_demo_participants=1,
    #     app_sequence=['weektwo'],
    # ),
    # dict(
    #     name="session2",
    #     display_name="Session Two",
    #     num_demo_participants=1,
    #     app_sequence=['Captcha', 'week1begin', 'week2rating', 'selfw2', 'otherw2', 'finishw2'],
    # ),
]




RECAPTCHA_PUBLIC_KEY = '6LcDleYUAAAAABOjmn93fgLcoC55Iu92_5-RbZL1'
RECAPTCHA_PRIVATE_KEY = '6LcDleYUAAAAAIVNjf_rEBtZK8zevhVpJ2yfsjWW'

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = []

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'marissaOTree'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '8(op17+kt0005q(re^!kpgd6m&mjamhit34@1kszx9685(ju&h'

# setting for integration with AWS Mturk

#AWS_ACCESS_KEY_ID = environ.get('AWSAccessKeyId')
#AWS_SECRET_ACCESS_KEY = environ.get('AWSSecretKey')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
EXTENSION_APPS = ['Captcha', 'leavable_wait_page']
