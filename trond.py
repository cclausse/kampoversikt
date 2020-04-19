import urllib.request, json, csv, time, trondconfig
import smtplib, ssl
#from trondconfig import TROND_CID
# https://www.youtube.com/watch?v=9N6a-VLBa2I&t=735s


def getMatchdata():
    print('Starter getMatchdata!')
    # url7 = "http://api.fotballdata.no/v1/stadiums/17723/clubs/1138/matches?cid=2" + KEY + "&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json"
    url7 = "http://api.fotballdata.no/v1/stadiums/17723/clubs/1138/matches?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json"
    url9 = "http://api.fotballdata.no/v1/stadiums/6410/clubs/1138/matches?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json"
    url11 = "http://api.fotballdata.no/v1/stadiums/6406/clubs/1138/matches?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json"
    numGoalsHome=0
    numGoalsAway=0
    totalNumGoalsHome = 0
    totalNumGoalsAway = 0 
    total_baneNumGoalsHome = 0
    total_baneNumGoalsAway = 0
    numkamper=0
    tot_numkamper=0
    url_list = (url7, url9, url11)

    i=0
    while i < len(url_list):
        # print(url_list[i])
        numGoalsHome = 0
        maxGoalsHome = 0
        maxGoalsAway = 0
        numGoalsAway = 0 
        total_bane_NumGoalsHome = 0
        total_bane_NumGoalsAway = 0
        with urllib.request.urlopen(url_list[i]) as url:
            numkamper = 0
            bane_data = json.loads(url.read().decode())
            banenavn = bane_data['StadiumName']
            # print('Logger data for: ' + banenavn)
            for match in bane_data['Matches']:
                print(match)
                print(match['TournamentName'] + " - "+ match['HomeTeamName'])
                # matchId = match['MatchId']
                # numGoalsHome = match['HomeTeamGoals']
                # numGoalsAway = match['AwayTeamGoals']
                matchdate = int(match['MatchStartDate'][6:16])
                matchdate_str = time.strftime("%Y %m %d - %H:%M", time.localtime(matchdate))
                print(matchdate_str)
                # Største seier
                if numGoalsHome >= maxGoalsHome and match['HomeTeamName'][0:5] =='Trond':
                    maxGoalsHome=numGoalsHome
                    maxGoalsHomeTeam = match['HomeTeamName']
                    if 'AwayTeamGoals' in match.keys(): 
                        maxseier_bortemal = match['AwayTeamGoals']
                        maxseier_bortelag = match['AwayTeamName']
                        # print("Present, ", end =" ")              Hva betyr dette?
                        # print("value =", dict['AwayTeamGoals'])   Hva betyr dette?
                        # Største tap
                        if (numGoalsAway >= maxGoalsAway and match['AwayTeamName'][0:5] !='Trond'):
                            maxGoalsAway=numGoalsAway
                            maxGoalsAwayTeam = match['AwayTeamName']
                            # print('Støreste tap: ' + str(match['MatchId']) + ': maxGoalsHomeTeam:\t ' + str(numGoalsHome)+ ' - '+ str(numGoalsAway) )

                            total_bane_NumGoalsHome += numGoalsHome
                            total_bane_NumGoalsAway += numGoalsAway

                            totalNumGoalsHome += numGoalsHome
                            totalNumGoalsAway += numGoalsAway
                    else: 
                        print("Match not played or no result found!") 
                numkamper +=1
                tot_numkamper +=1
            i += 1
        print('{}: \tAntall hjemmemål: \t{} Antall bortemål: \t{}'.format(banenavn, str(total_bane_NumGoalsHome), str(total_bane_NumGoalsAway)))
        print('Støreste seier\t: ' + str(match['MatchId']) + maxGoalsHomeTeam + '-' + maxseier_bortelag +' : ' + str(maxGoalsHome)+ ' - '+ str(maxseier_bortemal) )
        print('Støreste tap\t: ' + str(match['MatchId']) + ': maxGoalsAwayTeam:\t ' + str(numGoalsHome)+ ' - '+ str(numGoalsAway) )
        print('\n')

    print('Antall hjemmemål totalt: \t{} Antall bortemål totalt: \t{}'.format( str(totalNumGoalsHome), str(totalNumGoalsAway)))
    print('\nAntall kamper totalt: \t{}'.format( str(tot_numkamper)))
    print('\nAvslutter')

def getAllMatchesByTeamId(teamId):
    # print('\t\tHenter kamper for TeamId: {}'.format(teamId))
    url_teamId = 'http://api.fotballdata.no/v1/teams/' + str(teamId) + '/matches?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json'
    matchHomeCount=0
    HomeTeamId=''
    with urllib.request.urlopen('http://api.fotballdata.no/v1/teams/23928/matches?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json') as url:
        team_data = json.loads(url.read().decode())
        for match in team_data['Matches']:
            matchId = match['MatchId']
            HomeTeamId = match['HomeTeamClubId']

            if HomeTeamId == 1138:
                HomeTeamName = match['HomeTeamName']
                AwayTeamName = match['AwayTeamName']
                TournamentName = match['TournamentName']
                
                print('\t{} - {}\t{}'.format(HomeTeamName, AwayTeamName, TournamentName)) 
                matchHomeCount+=1

        # print('\tLag: {}\t TeamId: {} '.format(team['TeamName'], teamId))
        print('\tAntall hjemmekamper: {}'.format(matchHomeCount)) 
        return matchHomeCount
        # matchTotalCount +=matchCount
        # print('\t\tAntall matcher totalt: {}'.format(matchTotalCount)) 

def getAllTeams():
    print('Henter alle lag...')
    url_teams = "http://api.fotballdata.no/v1/clubs/1138/teams?cid=356&cwd=0E977397-2AF0-479A-8A47-C6A7B090B47B&format=json"
    matchTotalCount = 0
    with urllib.request.urlopen(url_teams) as url:
        teams_data = json.loads(url.read().decode())

        output_file = open('TeamsJson.csv', 'w', encoding='utf-8', newline='')
        # print(teams_data)
        # print(len(teams_data['Teams']))
        # print(json.dumps(teams_data, indent=2))
        # print(len(teams_data['Teams']))
        output_writer = csv.writer(output_file)
        print('\tFølgende lag deltar på vegne av {}'.format(teams_data['ClubName']))
        for team in teams_data['Teams']:
            teamId=team['TeamId']
            print('\tLag: {}\t TeamId: {} '.format(team['TeamName'], teamId))
            numMatches = getAllMatchesByTeamId(teamId)
            matchTotalCount +=numMatches
            row_array = []
            row_array.append(team['TeamName'])
            for attribute in team:
                # print(team['TeamName'])
                # print(attribute)
                row_array.append(team['TeamName'])
                output_writer.writerow(row_array)

        print('Antall matcher totalt: {}'.format(matchTotalCount))

def main():
    
    '''
        Get Current working Directory
    '''
    currentDirectory = os.getcwd()
    
    print(currentDirectory)
    
    '''
        Change the Current working Directory
    '''
    os.chdir('/home/varun')
    
    '''
        Get Current working Directory
    '''
    currentDirectory = os.getcwd()
    
    print(currentDirectory)
    getAllTeams()
	getMatchdata()
    
if __name__ == '__main__':
    main()