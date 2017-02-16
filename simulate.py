from random import choice, triangular, randint
from batterData import *

STRIKES = 0
BALLS = 0

class season:
    """
    """
    def __init__(self, teams=[]):
        self.teams = teams
        self.gamesPlayed = []
        self.seasonLength = 162

    def simulateSeason(self):
        totalGames = self.seasonLength / 2 * len(self.teams)
        while len(self.gamesPlayed) < totalGames:
            currentMatchup = self.getTeams()
            currentGame = game(currentMatchup[0], currentMatchup[1])
            currentGame.simulateGame()
            self.gamesPlayed.append(currentGame)

    def getTeams(self):
        homeTeam = choice(self.teams)
        awayTeam = choice(self.teams)
        while homeTeam.name == awayTeam.name:
            homeTeam = choice(self.teams)
            awayTeam = choice(self.teams)
        teams = [awayTeam, homeTeam]
        return teams

    def __str__(self):
        mvpOPS = 0
        mvp = ''
        for team in self.teams:
            print "\n%s's Record: %s-%s %s" % (team.name,team.wins, team.losses, team.wins * 100 / (team.wins+team.losses))
            for i in team.batters:
                firstName = i.firstName
                lastName = i.lastName
                avg = '%s' % (i.hits / 1.0 / (i.plateAppearances - i.walks))
                obp = '%s' % ((i.hits + i.walks) / 1.0 / i.plateAppearances)
                slg = '%s' % ((i.hits + i.doublesHit + (i.triplesHit *2) + (i.homerunsHit * 3) + i.walks) / 1.0 / i.plateAppearances)
                pas = i.plateAppearances
                hrs = i.homerunsHit
                walkPer = i.walks * 100 / i.plateAppearances
                kPer = i.strikeouts * 100 / i.plateAppearances
                if float(obp)+float(slg) > mvpOPS:
                    mvpOPS = float(obp)+float(slg)
                    mvp = 'MVP is %s %s' % (i.firstName, i.lastName)
                print '%s %s %s/%s/%s PA:%s; HRs:%s; FBs:%s; W:%s%%, K:%s%%' % (firstName, lastName, avg[2:5],obp[2:5],slg[2:5], pas, hrs, i.totalFlyBalls, walkPer, kPer)

        return mvp

class batter:
    """
    """
    def __init__(self, data=[]):
        self.firstName = ''
        self.lastName = ''
        self.foulballChance = triangular(100,300)
        self.babip = 0
        self.oSwing = 0
        self.zSwing = 0
        self.swing = 0
        self.oContact = 0
        self.zContact = 0
        self.contact = 0
        self.zone = 0
        self.fStrike = 0
        self.swingingStrike = 0
        self.doubles = 0
        self.triples = 0
        self.homeruns = 0
        self.hits = 0
        self.walks = 0
        self.doublesHit = 0
        self.triplesHit = 0
        self.homerunsHit = 0
        self.strikeouts = 0
        self.plateAppearances = 0
        self.flyballPercentage = 0
        self.homerunPerFlyball = 0

        if len(data) > 0:
            self.loadBatter(data)

    def loadBatter(self, nthBatter):
        if len(nthBatter) > 0:
            self.firstName = nthBatter[0]
            self.lastName = nthBatter[1]
            self.babip = nthBatter[2]
            self.oSwing = nthBatter[3]
            self.zSwing = nthBatter[4]
            self.swing = nthBatter[5]
            self.oContact = nthBatter[6]
            self.zContact = nthBatter[7]
            self.contact = nthBatter[8]
            self.zone = nthBatter[9]
            self.fstrike = nthBatter[10]
            self.swingingStrike = nthBatter[11]
            self.doubles = nthBatter[12] * 100 / 185
            self.triples = nthBatter[13] * 100 / 185
            self.homeruns = nthBatter[14] * 100 / 185
            self.flyballPercentage = nthBatter[15]
            self.homerunPerFlyball = nthBatter[16]
            self.totalFlyBalls = 0
        else:
            print 'Failed to load batter data.'

    def checkHit(self, pitchObject):
        global BALLS, STRIKES
        #Strike
        if not pitchObject.isBall:
            STRIKES += 1
            swingChance = randint(0,1000)
            if swingChance < self.zSwing:
                #Batter swings at a strike
                if randint(0,1000) < self.foulballChance:
                    return 'foul'
                else:
                    hitChance = randint(0,1000)
                    if hitChance < self.zContact:
                        #Batter makes contact with ball
                        chanceOfFlyball = randint(0,1000)
                        if chanceOfFlyball < self.flyballPercentage:
                            #Flyball
                            self.totalFlyBalls += 1
                            chanceOfHomerun = randint(0,1000)
                            if chanceOfHomerun < self.homerunPerFlyball:
                                #Homerun!
                                return 'homerun'
                            if chanceOfHomerun < self.babip:
                                if chanceOfHomerun < (self.homeruns + self.triples):
                                    return 'triple'
                                if chanceOfHomerun < (self.homeruns + self.triples + self.doubles):
                                    return 'double'
                                else:
                                    return 'single'
                            else:
                                return 'out'
                        chanceOfSingle = randint(0,1000)
                        if chanceOfSingle < self.babip:
                            if chanceOfSingle < (self.homeruns + self.triples):
                                return 'triple'
                            if chanceOfSingle < (self.homeruns + self.triples + self.doubles):
                                return 'double'
                            else:
                                return 'single'
                        else:
                            return 'out'
                    else:
                        #Batter swings and misses
                        return 'swinging strike'
            else:
                #Batter does not swing at strike
                return 'called strike'
        else:
            #Ball
            BALLS += 1
            swingChance = randint(0,1000)
            if swingChance < self.oSwing:
                #Batter swings at a ball
                if randint(0,1000) < self.foulballChance:
                    return 'foul'
                else:
                    #TODO: Make it less likely to hit a ball
                    hitChance = randint(150,1000)
                    if hitChance < self.oContact:
                        chanceOfFlyball = randint(0,1000)
                        if chanceOfFlyball < self.flyballPercentage:
                            #Flyball
                            self.totalFlyBalls += 1
                            chanceOfHomerun = randint(200,1000)
                            if chanceOfHomerun < self.homerunPerFlyball:
                                #Homerun!
                                return 'homerun'
                            if chanceOfHomerun < self.babip:
                                if chanceOfHomerun < (self.homeruns + self.triples):
                                    return 'triple'
                                if chanceOfHomerun < (self.homeruns < self.triples + self.doubles):
                                    return 'double'
                                else:
                                    return 'single'
                            else:
                                return 'out'
                        chanceOfSingle = randint(0,1000)
                        if chanceOfSingle < self.babip:
                            if chanceOfSingle < (self.homeruns + self.triples):
                                return 'triple'
                            if chanceOfSingle < (self.homeruns + self.triples + self.doubles):
                                return 'double'
                            else:
                                return 'single'
                        else:
                            return 'out'
                    else:
                        #Batter swings and misses
                        return 'swinging strike'
            else:
                #Batter does not swing at ball
                return 'ball'



class team:
    """
    """
    def __init__(self, name='', first=batter(), second=batter(),
                    third=batter(), fourth=batter(), fifth=batter(),
                    sixth=batter(), seventh=batter(), eighth=batter(),
                    ninth=batter()):

        self.name = name
        self.batters = (first, second, third, fourth, fifth, sixth,
                        seventh, eighth, ninth)
        self.wins = 0
        self.losses = 0

    def getNextBatter(self, position=0):
        return self.batters[position]

class game:
    """
    """
    def __init__(self, homeTeam, awayTeam):
        self.gameOver = False
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.inning = 0
        self.currentHalfInning = 'top'
        self.outs = 0
        self.balls = 0
        self.strikes = 0
        self.pitches = 0
        self.totalStrikes = 0
        self.totalBalls = 0
        self.awayScore = []
        self.homeScore = []
        self.awayHits = []
        self.homeHits = []
        self.atFirstBase = False
        self.atSecondBase = False
        self.atThirdBase = False
        self.plateAppearances = 0
        self.hits = 0
        self.walks = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homeruns = 0
        self.newHalfInning()
        self.homeTeam = homeTeam
        self.awayTeam
        self.homeAtBats = 0
        self.awayAtBats = 0
        self.currentBatter = self.awayTeam.getNextBatter(self.awayAtBats % 9)

    def simulateGame(self):
        while self.gameOver == False:
            currentPitch = pitch(self.currentBatter.zone)
            self.pitch(currentPitch)
        if sum(self.homeScore) > sum(self.awayScore):
            self.homeTeam.wins += 1
            self.awayTeam.losses += 1
        else:
            self.awayTeam.wins += 1
            self.homeTeam.losses += 1

    def pitch(self, objPitch):
        if self.currentHalfInning == 'bottom':
            self.currentBatter = self.homeTeam.getNextBatter(self.homeAtBats % 9)
            self.homeAtBats += 1
        else:
            self.currentBatter = self.awayTeam.getNextBatter(self.awayAtBats % 9)
            self.awayAtBats += 1

        self.pitches += 1
        result = self.currentBatter.checkHit(objPitch)
        if result == 'ball':
            self.recordBall()
        elif result == 'swinging strike':
            self.recordStrike()
        elif result == 'called strike':
            self.recordStrike()
        elif result == 'foul':
            if self.strikes < 2:
                self.strikes += 1
        elif result == 'single':
            self.recordSingle()
        elif result == 'double':
            self.recordDouble()
        elif result == 'triple':
            self.recordTriple()
        elif result == 'homerun':
            self.recordHomerun()
        elif result == 'out':
            self.recordOut()

    def batterOnBase(self):
        if self.atFirstBase == 0:
            self.atFirstBase = 1
        elif self.atSecondBase == 0:
            self.secondBase = 1
        elif self.atThirdBase == 0:
            self.atThirdBase = 1
        else:
            self.recordRun()
        self.newBatter()

    def recordHit(self):
        self.hits += 1
        self.currentBatter.hits += 1
        if self.currentHalfInning == 'top':
            self.awayHits[self.inning - 1] += 1
        else:
            self.homeHits[self.inning - 1] += 1

    def recordRun(self):
        if self.currentHalfInning == 'top':
            self.awayScore[self.inning - 1] += 1
        else:
            self.homeScore[self.inning - 1] += 1

    def recordSingle(self):
        self.recordHit()
        self.singles += 1

        if self.atFirstBase == 0:
            self.atFirstBase = 1
        elif self.atSecondBase == 0:
            self.secondBase = 1
        elif self.atThirdBase == 0:
            self.atThirdBase = 1
        else:
            self.recordRun()
        self.newBatter()

    def recordDouble(self):
        self.recordHit()
        self.currentBatter.doublesHit += 1
        self.doubles += 1

        if self.atThirdBase == 1:
            self.recordRun()
        if self.atSecondBase == 1:
            self.recordRun()
        if self.atFirstBase == 1:
            self.atThirdBase = 1
        self.atSecondBase = 1

        self.newBatter()

    def recordTriple(self):
        self.recordHit()
        self.currentBatter.triplesHit += 1
        self.triples += 1

        if self.atThirdBase == 1:
            self.recordRun()
        if self.atSecondBase == 1:
            self.recordRun()
        if self.atFirstBase == 1:
            self.recordRun()
        self.atThirdBase = 1

        self.newBatter()

    def recordHomerun(self):
        self.recordHit()
        self.currentBatter.homerunsHit += 1
        self.homeruns += 1

        if self.atThirdBase == 1:
            self.recordRun()
        if self.atSecondBase == 1:
            self.recordRun()
        if self.atFirstBase == 1:
            self.recordRun()
        self.recordRun()

        self.newBatter()

    def newBatter(self):
        self.currentBatter.plateAppearances += 1
        self.strikes = 0
        self.balls = 0
        self.plateAppearances += 1

    def recordBall(self):
        self.balls += 1
        self.totalBalls += 1
        if self.balls > 3:
            self.currentBatter.walks += 1
            self.walks += 1
            self.batterOnBase()

    def recordStrike(self):
        self.strikes += 1
        self.totalStrikes += 1
        if self.strikes > 2:
            self.currentBatter.strikeouts += 1
            self.recordOut()

    def recordOut(self):
        self.outs += 1
        if self.outs > 2:
            self.newHalfInning()
        self.newBatter()

    def newHalfInning(self):
        self.outs = 0
        self.atFirstBase = 0
        self.atSecondBase = 0
        self.atThirdBase = 0

        if self.inning >= 9:
            if self.homeScore > self.awayScore:
                self.gameOver = True

        if not self.gameOver:
            if self.currentHalfInning == 'top':
                self.currentHalfInning = 'bottom'
                self.homeScore.append(0)
                self.homeHits.append(0)
            else:
                if self.inning >= 9:
                    self.gameOver = True
                else:
                    self.inning += 1
                    self.currentHalfInning = 'top'
                    self.awayScore.append(0)
                    self.awayHits.append(0)

    def __str__(self):
        awayScoreRecord = ''
        awayTeamRuns = 0
        for score in self.awayScore:
            awayScoreRecord += ' %s ' % score
            awayTeamRuns += score

        homeScoreRecord = ''
        homeTeamRuns = 0
        for score in self.homeScore:
            homeScoreRecord += ' %s ' % score
            homeTeamRuns += score

        output = '\t\t\t 1  2  3  4  5  6  7  8  9\t |\n'
        output += self.awayTeam, ':\t', awayScoreRecord,'\t | ', awayTeamRuns,'\n'
        output += self.homeTeam, ':\t', homeScoreRecord,'\t | ', homeTeamRuns,'\n'
        return output


class pitch:
    """
    """
    def __init__(self, zone):
        self.pitchType = choice(['fastball', 'slider', 'changeup'])
        self.speed = randint(70,90)
        if self.pitchType == 'fastball':
            self.speed += 10
        if self.pitchType == 'slider':
            self.speed += 5
        self.distanceFromCenter = randint(1,1000)
        self.isBall = False
        if self.distanceFromCenter > zone:
            self.isBall = True
        self.pitch_angle = randint(0,360)

NYY = team('New York Yankees', batter(derek_jeter), batter(johnny_damon),
			batter(mark_teixeira), batter(alex_rodriguez),
			batter(jorge_posada), batter(hideki_matsui),
			batter(robinson_cano), batter(nick_swisher),
			batter(melky_cabrera))
STL = team('St Louis Cardinals', batter(jon_jay), batter(david_freese),
			batter(allen_craig), batter(matt_holiday),
			batter(carlos_beltran), batter(yadier_molina),
			batter(matt_carpenter), batter(skip_schumaker),
			batter(pete_kozma))

objSeason = season([NYY,STL])
objSeason.simulateSeason()

print objSeason
