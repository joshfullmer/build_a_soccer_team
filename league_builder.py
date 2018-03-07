import csv
import os


LETTER_TEXT = """Dear {},

Thanks for enrolling your child, {}, in our soccer league!

Your child will be playing for the {}.
Their first team practice will be on March 7, 2018 at 10:30am.

Thanks, and we'll seeya there!
"""


def create_teams(team_names, players):
    """
    Takes a list of team names and a list of player dictionaries and returns
    a dictionary where the keys are the team names and the values are a list of
    dictionaries representing the players.

    Evenly distributes the players by experience and ensures equal team size.
    """
    teams = {}

    # Create empty lists to house players, one for each team.
    for team in team_names:
        teams[team] = []

    team_num = 0
    team_max_index = len(team_names) - 1

    # Only add players with experience to ensure equal distribution of
    # experience
    for player in players:
        if player['Soccer Experience'] == 'YES':

            # Uses the list of provided team names with the index to add
            # to the correct key's list of the teams dictionary
            teams[team_names[team_num]].append(player)
            if team_num == team_max_index:
                team_num = 0
            else:
                team_num += 1

    # Uses the same index to start from, so it picks up where the last loop
    # left off. This would handle any configuration of teams and players.
    for player in players:
        if player['Soccer Experience'] == 'NO':
            teams[team_names[team_num]].append(player)
            if team_num == team_max_index:
                team_num = 0
            else:
                team_num += 1

    return teams


def write_roster(teams, filename):
    """
    Iterates through the list of teams generated and writes the team rosters
    to file in the filename provided
    """
    with open(filename, 'w') as file:
        for team_name, players in teams.items():

            # Add team name with fancy header
            file.write(team_name+"\n")
            file.write("="*len(team_name)+"\n\n")

            for player in players:
                file.write("{}, {}, {}\n".format(
                    player['Name'],
                    player['Soccer Experience'],
                    player['Guardian Name(s)'],
                ))
            file.write("\n")


def write_letters(teams, directory=''):
    """
    Iterates through the list of teams generated and composes a letter to the
    parent/guardian welcoming them to the league.
    """
    # Create directory with provided name, if it is provided
    if directory:
        os.makedirs(directory, exist_ok=True)

    for team_name, players in teams.items():
        for player in players:

            # Generate lower case full name, replacing spaces with underscores
            filename = player['Name'].lower().replace(' ', '_') + '.txt'

            # Modify filename to include directory, if provided
            if directory:
                filename = "/".join([directory, filename])
            with open(filename, 'w') as file:
                file.write(LETTER_TEXT.format(
                    player['Guardian Name(s)'],
                    player['Name'],
                    team_name,
                ))


if __name__ == '__main__':
    with open('soccer_players.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        players = list(reader)

    team_names = ['Sharks', 'Dragons', 'Raptors']
    teams = create_teams(team_names, players)

    write_roster(teams, 'teams.txt')

    write_letters(teams, 'more_letters')
