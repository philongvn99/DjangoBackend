# PLAYER
# Table-name LIST
import re


playerPosition = ["goalkeeper", "defender", "midfielder", "forward"]

# Player-information FIELDS
#   entire fields
playerFields = [
    'id', 
    'name', 
    'full_name', 
    'avatar_link', 
    'nationality', 
    'birthday', 
    'right_foot', 
    'kit_number', 
    'height', 
    'role',
    'salary', 
    'status'
]

#  LEAGUE
#  League-table FIELDS
leagueTableField = [
    'name',
    'acronym_name',
    'logo_link',
    'played_game',
    'won_game',
    'drawn_game',
    'lost_game',
    'goal_for',
    'goal_against',
    'goal_difference',
    'points'
]

username = 'dr3g0ng44m'
password = "abc37841"

# Define support function
def displayError(jsError):
    print(jsError)
    for key, values in jsError.items():
        print(key, ':')
        for value in values:
            for field, val in value.items():
                print('  ', field)
                print('     ', val)


char_dict = {   '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, 
                'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15, 'G' : 16, 'H' : 17, 'I' : 18, 
                'J' : 19, 'K' : 20, 'L' : 21, 'M' : 22, 'N' : 23, 'O' : 24, 'P' : 25, 'Q' : 26, 'R' : 27, 
                'S' : 28, 'T' : 29, 'U' : 30, 'V' : 31, 'W' : 32, 'X' : 33, 'Y' : 34, 'Z' : 35, 
                'a' : 36, 'b' : 37, 'c' : 38, 'd' : 39, 'e' : 40, 'f' : 41, 'g' : 42, 'h' : 43, 'i' : 44, 
                'j' : 45, 'k' : 46, 'l' : 47, 'm' : 48, 'n' : 49, 'o' : 50, 'p' : 51, 'q' : 52, 'r' : 53, 
                's' : 54, 't' : 55, 'u' : 56, 'v' : 57, 'w' : 58, 'x' : 59, 'y' : 60, 'z' : 61  }

userField = ('username', 'email', 'phone', 'name', 'license')

regex_bearer = re.compile(r"^[Bb]earer (.*)$")

sample_user_firebase = {
    'name': 'string', 
    'picture': 'url_string', 
    'iss': 'https://securetoken.google.com/plfirebase-cc1f1', 
    'aud': 'plfirebase-cc1f1', 
    'auth_time': 1683811332, 
    'user_id': 'tKh7gGHff9NUglYxe931ge49gAq2', 
    'sub': 'tKh7gGHff9NUglYxe931ge49gAq2', 
    'iat': 1683811332, 
    'exp': 1683814932, 
    'email': 'holtby331@gmail.com', 
    'email_verified': False, 
    'phone_number': '+84327071985', 
    'firebase': {
        'identities': {
            'phone': ['+84327071985'], 
            'email': ['holtby331@gmail.com']},
            'sign_in_provider': 'password'
        }, 
    'uid': 'tKh7gGHff9NUglYxe931ge49gAq2'
}

