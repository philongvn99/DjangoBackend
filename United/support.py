# PLAYER
# Table-name LIST
playerPosition = ["goalkeeper", "defender", "midfielder", "forward"]

# Player-information FIELDS
#   entire fields
playerFields = [
    'player_id', 
    'player_name', 
    'player_full_name', 
    'player_avatar_link', 
    'player_nationality', 
    'player_birthday', 
    'player_right_foot', 
    'player_kit_number', 
    'player_height', 
    'player_role',
    'player_salary', 
    'player_status'
]

#  LEAGUE
#  League-table FIELDS
leagueTableField = [
    'team__team_name',
    'team__team_acronym_name',
    'team__team_logo_link',
    'team_played_game',
    'team_won_game',
    'team_drawn_game',
    'team_lost_game',
    'team_goal_for',
    'team_goal_against',
    'team_goal_difference',
    'team_points'
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

