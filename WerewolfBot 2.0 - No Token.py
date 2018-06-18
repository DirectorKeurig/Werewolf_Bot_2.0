import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import random
from threading import Timer
from collections import Counter
import playableClasses
Client = discord.Client()
bot = commands.Bot(command_prefix = "w!")

#global variables
gameIsRunning = False
playerObjectList = []
origChannel = None
adminUser = None
canJoin = False
userList = []
MIN_PLAYERS = 7
time = None
werewolfChannel = None
townName = None
isFirstNight = True
haveWerewolvesEaten = False
werewolfVote = []
allWerewolvesVoted = False
nominationsToday = 0
canNominate = False
nominees = []
vote = []
timeToVote = False
nominators = {}
voting = False
votedLive = []
votedDie = []

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message):
    global gameIsRunning
    global playerObjectList
    global origChannel
    global adminUser
    global canJoin
    global userList
    global MIN_PLAYERS
    global time
    global werewolfChannel
    global townName
    global haveWerewolvesEaten
    global nominationsToday
    global canNominate
    global nominees
    global vote
    global isFirstNight
    global timeToVote
    global nominators
    global canNominate
    global voting
    global votedLive
    global votedDie
    contents = message.content.split(" ")

    #w!setup
    if message.content.upper().startswith("W!SETUP") and gameIsRunning == False:
        print("global vars are:")
        print("gameIsRunning=" + str(gameIsRunning))
        print("playerObjectList=" + str(playerObjectList))
        print("origChannel=" + str(origChannel))
        print("adminUser=" + str(adminUser))
        print("canJoin=" + str(canJoin))
        print("userList=" + str(userList))
        print("MIN_PLAYERS=" + str(MIN_PLAYERS))
        print("time=" + str(time))
        print("werewolfChannel=" + str(werewolfChannel))
        print("townName=" + str(townName))
        print("haveWerewolvesEaten=" + str(haveWerewolvesEaten))
        print("nominationsToday=" + str(nominationsToday))
        print("canNominate=" + str(canNominate))
        print("nominees=" + str(nominees))
        print("vote=" + str(vote))
        print("isFirstNight=" + str(isFirstNight))
        print("timeToVote=" + str(timeToVote))
        print("nominators=" + str(nominators))
        print("canNominate=" + str(canNominate))
        print("voting=" + str(voting))
        print("votedLive=" + str(votedLive))
        print("votedDie=" + str(votedDie))
        await setUp(message)
        await bot.send_message(origChannel, "@everyone, please read the rules before joining the game.")
        await displayRules(origChannel)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!SETUP") and gameIsRunning == True:
        print("global vars are:")
        print("gameIsRunning=" + str(gameIsRunning))
        print("playerObjectList=" + str(playerObjectList))
        print("origChannel=" + str(origChannel))
        print("adminUser=" + str(adminUser))
        print("canJoin=" + str(canJoin))
        print("userList=" + str(userList))
        print("MIN_PLAYERS=" + str(MIN_PLAYERS))
        print("time=" + str(time))
        print("werewolfChannel=" + str(werewolfChannel))
        print("townName=" + str(townName))
        print("haveWerewolvesEaten=" + str(haveWerewolvesEaten))
        print("nominationsToday=" + str(nominationsToday))
        print("canNominate=" + str(canNominate))
        print("nominees=" + str(nominees))
        print("vote=" + str(vote))
        print("isFirstNight=" + str(isFirstNight))
        print("timeToVote=" + str(timeToVote))
        print("nominators=" + str(nominators))
        print("canNominate=" + str(canNominate))
        print("voting=" + str(voting))
        print("votedLive=" + str(votedLive))
        print("votedDie=" + str(votedDie))
        await bot.send_message(message.author, "A game of Werewolf is already running.")
        await deleteMessage(message)

    #w!join
    if message.content.upper().startswith("W!JOIN") and canJoin == True and message.author != adminUser and message.author not in userList:
        await joinGame(message.author, message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!JOIN") and canJoin == False:
        await bot.send_message(message.author, "You cannot join a game at this time.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!JOIN") and canJoin == True and message.author == adminUser:
        await bot.send_message(message.author, "You automatically join your own game of Werewolf.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!JOIN") and canJoin == True and message.author != adminUser and message.author in userList:
        await bot.send_message(message.author, "You can't join a game twice!")
        await deleteMessage(message)

    #w!start
    if message.content.upper().startswith("W!START") and message.author == adminUser and canJoin == True and len(userList) >= MIN_PLAYERS:
        await startGame(message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!START") and message.author == adminUser and canJoin == True and len(userList) < MIN_PLAYERS:
        await bot.send_message(message.author, "There aren't enough players to start the game.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!START") and message.author == adminUser and canJoin == False:
        await bot.send_message(message.author, "You can't start a game right now.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!START") and message.author != adminUser:
        await bot.send_message(message.author, "Only the original user can start the game.")
        await deleteMessage(message)

    #w!stop
    if message.content.upper().startswith("W!STOP") and message.author == adminUser:
        await bot.send_message(origChannel, "@everyone, " + adminUser.mention + " has stopped the game.")
        await stopGame()
        await deleteMessage(message)
    elif message.content.upper().startswith("W!STOP"):
        await deleteMessage(message)

    #w!players
    if message.content.upper().startswith("W!PLAYERS") and gameIsRunning:
        await sendPlayers(message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!PLAYERS"):
        await bot.send_message(message.author, "There is no game running right now.")
        await deleteMessage(message)

    #w!settownname
    if message.content.upper().startswith("W!SETTOWNNAME") and message.author == adminUser and canJoin == True and message.channel == origChannel:
        args = message.content.split(" ")
        if len(args)>1:
            townName = str(" ".join(args[1:]))
        await deleteMessage(message)
    elif message.content.upper().startswith("W!SETTOWNNAME"):
        await deleteMessage(message)

    #w!ability
    if message.content.upper().startswith("W!ABILITY") and getPlayerObject(message.author) != None and getPlayerObject(message.author).hasNonWerewolfAbility == True and time == "night" and message.channel != (origChannel or werewolfChannel):
        await useAbility(message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!ABILITY"):
        await deleteMessage(message)

    #w!eat
    if message.content.upper().startswith("W!EAT") and getPlayerObject(message.author).role == "werewolf" and time == "night" and haveWerewolvesEaten == False and isFirstNight == False and message.channel == werewolfChannel:
        print("\nEat method called.\n")
        await eat(message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!EAT"):
        print("\nEat command bounced.\n")
        print("Message author role = " + str(getPlayerObject(message.author).role))
        print("time = " + time)
        print("haveWerewolvesEaten = " + str(haveWerewolvesEaten))
        print("isFirstNight = " + str(isFirstNight))
        print("message.channel = " + str(message.channel))
        await deleteMessage(message)

    #w!nominate
    if message.content.upper().startswith("W!NOMINATE") and getPlayerObject(message.author) != None and canNominate == True and nominationsToday < 2:
        await nominate(message)
        await deleteMessage(message)
        
    elif message.content.upper().startswith("W!NOMINATE"):
        print("Message author = " + str(getPlayerObject(message.author)))
        print("canNominate = " + str(canNominate))
        print("Nominations today = " + str(nominationsToday))
        print("Nominate command deleted")
        await deleteMessage(message)

    #w!second
    if message.content.upper().startswith("W!SECOND") and getPlayerObject(message.author) != None and canNominate == True and nominationsToday < 2:
        await second(message)
        await deleteMessage(message)
    elif message.content.upper().startswith("W!SECOND"):
        await deleteMessage(message)

    #w!live
    if message.content.upper().startswith("W!LIVE") and getPlayerObject(message.author) != None and timeToVote == True and not getPlayerObject(message.author).hasVoted:
        vote.append("live")
        votedLive.append(getPlayerObject(message.author))
        getPlayerObject(message.author).hasVoted = True
        await bot.send_message(message.author, "You have voted live. ")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!LIVE") and getPlayerObject(message.author).hasVoted:
        await bot.send_message(message.author, "You have already voted. You can't vote twice.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!LIVE"):
        await deleteMessage(message)

    #w!die
    if message.content.upper().startswith("W!DIE") and getPlayerObject(message.author) != None and timeToVote == True and not getPlayerObject(message.author).hasVoted:
        vote.append("die")
        votedDie.append(getPlayerObject(message.author))
        getPlayerObject(message.author).hasVoted = True
        await bot.send_message(message.author, "You have voted die. ")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!DIE") and getPlayerObject(message.author).hasVoted:
        await bot.send_message(message.author, "You have already voted. You can't vote twice.")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!DIE"):
        await deleteMessage(message)

    #w!reveal
    if message.content.upper().startswith("W!REVEAL") and getPlayerObject(message.author) != None and getPlayerObject(message.author).role == "lalma" and message.channel != (origChannel or werewolfChannel) and getPlayerObject(message.author).usedAbility == False:
        args = message.content.split(" ")
        target = None
        attemptedTarget = None
        if len(args) > 1:
            attemptedTarget = str(" ".join(args[1:]))
            target = await targetPlayer(attemptedTarget, message)
            if target == None:
                await bot.send_message(message.author, "No match was found for the player name you entered. Make sure it was spelled correctly, and then try again.")
            else:
                await bot.send_message(origChannel, "@everyone, the all-knowing Lalma has spoken: " + target.player.mention + " is a " + target.role + ". " )
                getPlayerObject(message.author).usedAbility = True
        else:
            await bot.send_message(message.author, "You must include a player's name with the \"w!reveal\" command. Use the format \"w!reveal [player name here]\"")
        await deleteMessage(message)
    elif message.content.upper().startswith("W!REVEAL"):
        await deleteMessage(message)

    #w!help
    if message.content.upper().startswith("W!HELP"):
        await bot.send_message(message.author,
                """
                                                ----Werewolf commands----
                                                
    w!setup - Lets players join your new game of werewolf with an "add players" phase.
    w!stop - Stops your game of werewolf
    w!start - Starts the game once enough players have joined
    w!join - Adds you to a game of werewolf during the "add players" phase.
    w!help - Displays a list of possible commands.
    w!settownname [town name here] - Lets the admin user set the town name during the "add players" phase
    w!players - Displays a list of all living and dead players
    w!rules - Displays the rules of the game
    w!addlog [diary entry here] - Adds a new entry to your diary, which will be read upon your death.
    w!readlog - Displays all of your current diary entries.
    w!deletelog [entry # here] - Deletes a diary entry
                """)
        await deleteMessage(message)

    #w!rules
    if message.content.upper().startswith("W!RULES"):
        await displayRules(message.author)

    #w!addlog
    if message.content.upper().startswith("W!ADDLOG") and gameIsRunning and getPlayerObject(message.author) != None:
        args = message.content.split(" ")
        if len(args) > 1:
            del args[0]
            msg = ' '.join(args)
            print("message = " + str(msg))
            getPlayerObject(message.author).diary.append(msg)
            await bot.send_message(message.author, "Your message has been added to your diary.")
            await deleteMessage(message)
        else:
            await bot.send_message(message.author, "You must include a message to add to your log. Use the format \"w!addlog [message here]\"")
            await deleteMessage(message)

    #w!readlog
    if message.content.upper().startswith("W!READLOG") and gameIsRunning and getPlayerObject(message.author) != None:
        x = 1
        for i in getPlayerObject(message.author).diary:
            await bot.send_message(message.author, str(x) + ". " + str(i))
            x += 1
        await deleteMessage(message)
    elif message.content.upper().startswith("W!READLOG"):
        await deleteMessage(message)

    #w!insertlog
    if message.content.upper().startswith("W!INSERTLOG") and gameIsRunning and getPlayerObject(message.author) != None:
        args = message.content.split(" ")
        if len(args) > 2:
            del args[0]
            num = int(args[0])
            del args[0]
            print("num = " + str(num))
            msg = " ".join(args)
            getPlayerObject(message.author).diary.insert(num - 1, msg)
            await bot.send_message(message.author, "Your message has been inserted before diary entry " + str(num))
        else:
            await bot.send_message(message.author, "You must include the position you want to add an entry at and the entry itself. Use the format \"w!insertlog [number] [message]\"")
            await deleteMessage(message)

    #w!deletelog
    if message.content.upper().startswith("W!DELETELOG") and gameIsRunning and getPlayerObject(message.author) != None and getPlayerObject(message.author).diary != []:
        args = message.content.split(" ")
        if len(args) == 2:
            num = int(" ".join(args[1:])) - 1
            del getPlayerObject(message.author).diary[num]
            await bot.send_message(message.author, "Entry #" + str(num + 1) + " was deleted.")
            await deleteMessage(message)
        else:
            await bot.send_message(message.author, "Use the format \"w!deletelog [number here]\" to delete an entry of your choice.")
            await deleteMessage(message)
            
        

async def sendPlayers(message):
    global playerObjectList
    global userList
    global origChannel
    await bot.send_message(message.author, "----Live Players----")
    for i in playerObjectList:
        await bot.send_message(message.author, i.player.display_name)
    await bot.send_message(message.author, "----Dead Players----")
    for x in userList:
        if getPlayerObject(x) == None:
            await bot.send_message(message.author, x.player.display_name)

async def displayRules(destination):
    await bot.send_message(destination, """
    The rules are as follows:
    - Only send commands in the text channel(s) you are instructed to. Even though most commands will work in any text channel, it can break the game. Seriously, just follow the instructions.
    - You may DM other players IF YOU ARE STILL ALIVE, however, be aware that lying is perfectly acceptable and should be expected.
    - If you are killed, DO NOT DM other players or pass on information in any way.
    - Wait at least 2 minutes after a game ends/stopping a game to restart. I'm working on a fix for this, but right now if you start a game back to back it will cause issues.

    The following rules only apply to server admins.

    - You will be able to look in the private werewolf channel and see who the werewolves are regardless of if you are a werewolf. Don't do it. (Obviously if you're a werewolf go ahead)
    - You will be able to talk at times when you shouldn't (like at night or during someone's defense). Don't do it.
    - Don't mess with permissions during the game. They will be changing a lot, so wait until after the game to make changes.
    - Don't try to break the game by deleting channels the bot is running the game on or kicking players who are in the game. If the game crashes you might need to unmute people manually.
                                        """)
    
async def stopGame():
    global werewolfChannel
    global userList
    global gameIsRunning
    if gameIsRunning:
        gameIsRunning = False
        if werewolfChannel != None:
            await bot.delete_channel(werewolfChannel)
        unmuted = discord.PermissionOverwrite(send_messages = True)
        for person in userList:
            try:
                await bot.edit_channel_permissions(origChannel, person, unmuted)
            except discord.errors.InvalidArgument:
                nothing = None
        await setDefaultVars()

async def second(message):
    global playerObjectList
    global nominees
    global canNominate
    global nominationsToday
    global nominators
    global gameIsRunning
    if gameIsRunning:
        second = None
        args = message.content.split(" ")
        if len(args) > 1:
            secondName = str(" ".join(args[1:]))
            secondedPerson = await targetPlayer(secondName, message)
            if secondedPerson in nominees and nominators[secondedPerson] != getPlayerObject(message.author):
                await bot.send_message(origChannel, secondedPerson.player.mention + " has been seconded by " + message.author.mention + "!")
                canNominate = False
                nominationsToday += 1
                nominators = {}
                await startVote(secondedPerson)
            elif secondedPerson not in nominees:
                await bot.send_message(message.author, secondedPerson.player.mention + " has not been nominated, so you can't second them.")
            elif nominators[secondedPerson] == getPlayerObject(message.author):
                await bot.send_message(message.author, "You can't second the same person you nominated. You need a SECOND person, hence the name seconding.")

async def startVote(person):
    global vote
    global playerObjectList
    global origChannel
    global townName
    global werewolfChannel
    global timeToVote
    global nominationsToday
    global townName
    global voting
    global gameIsRunning
    if gameIsRunning:
        voting = True
        await castVote(person)

async def castVote(person):
    global vote
    global playerObjectList
    global origChannel
    global townName
    global werewolfChannel
    global timeToVote
    global nominationsToday
    global townName
    global voting
    global votedLive
    global votedDie
    global canNominate
    global nominees
    global nominators
    global gameIsRunning
    if gameIsRunning:
        await bot.send_message(origChannel, person.player.mention + " has been nominated and seconded. ")
        await bot.send_message(origChannel, person.player.mention + ", you have 20 seconds to state your defense.")
        unmuted = discord.PermissionOverwrite(send_messages=True)
        muted = discord.PermissionOverwrite(send_messages=False)
        for i in playerObjectList:
            if i != person:
                await bot.edit_channel_permissions(origChannel, i.player, muted)
        await asyncio.sleep(20)
        await bot.send_message(origChannel, "The time has come to vote! Use the \"w!live\" command or the \"w!die\" command IN THE PRIVATE WEREWOLF DM to vote for " + person.player.mention + ". You have 20 seconds to cast your vote, or you can abstain from voting.")
        timeToVote = True
        for i in playerObjectList:
            await bot.edit_channel_permissions(origChannel, i.player, unmuted)
        await asyncio.sleep(20)
        result = await tallyVote(vote)
        if result == "live":
            for i in votedLive:
                await bot.send_message(origChannel, i.player.mention + " voted live.")
            for i in votedDie:
                await bot.send_message(origChannel, i.player.mention + " voted  die.")
            for i in playerObjectList:
                if not i.hasVoted:
                    await bot.send_message(origChannel, i.player.mention + " abstained from voting.")
            await asyncio.sleep(1)
            await bot.send_message(origChannel, "The people have spoken, " + person.player.mention + " must live.")

            vote = []
            voting = False
            canNominate = True
            timeToVote = False
            votedLive = []
            votedDie = []
            nominees = []
            nominators = {}
            for i in playerObjectList:
                i.hasVoted = False
            if nominationsToday == 1:
                await bot.send_message(origChannel, "You may nominate one more person today. The night will start automatically if no one is nominated and seconded within the next 30 seconds.")
                print("Nominations today = " + str(nominationsToday))
                await delayStartNight(30)
            else:
                await bot.send_message(origChannel, "Having nominated two people, the town of " + townName + " goes to bed. The night will start in 30 seconds.")
                await night(30)
        elif result == "die":
            for i in votedLive:
                await bot.send_message(origChannel, i.player.mention + " voted live.")
            for i in votedDie:
                await bot.send_message(origChannel, i.player.mention + " voted  die.")
            for i in playerObjectList:
                if not i.hasVoted:
                    await bot.send_message(origChannel, i.player.mention + " abstained from voting.")
            await asyncio.sleep(1)
            await bot.send_message(origChannel, "The people have spoken, " + person.player.mention + " must be executed for their crimes.")
            await displayLog(person)
            await displayTeam(person)
            await bot.send_message(person.player, "You have been executed.")
            await bot.edit_channel_permissions(origChannel, person.player, muted)
            if person.role == "werewolf":
                await bot.edit_channel_permissions(werewolfChannel, person.player, muted)
            print("\n\nChecking win for vote\n\n")
            playerObjectList.remove(person)
            test = await checkWin()
            if test == None:
                vote = []
                voting = False
                canNominate = False
                timeToVote = False
                votedLive = []
                votedDie = []
                nominees = []
                nominators = {}
                for i in playerObjectList:
                    i.hasVoted = False
                await bot.send_message(origChannel, "Having satisfied it's lust for blood, the town of " + townName + " goes to bed. The night will start in 30 seconds.")
                await night(30)
        elif result == None:
            for i in playerObjectList:
                await bot.send_message(origChannel, i.player.mention + " abstained from voting.")
            await bot.send_message(origChannel, "Since apparently everyone (INCLUDING the people who nominated and seconded) chickened out of voting, " + person.player.mention + " gets to live I guess.")
            vote = []
            voting = False
            canNominate = True
            timeToVote = False
            votedLive = []
            votedDie = []
            nominees = []
            nominators = {}
            for i in playerObjectList:
                i.hasVoted = False
            if nominationsToday == 1:
                await bot.send_message(origChannel, "You may nominate one more person today. The night will start automatically if no one is nominated and seconded within the next 30 seconds.")
                await delayStartNight(30)
            else:
                await bot.send_message(origChannel, "Having nominated two people, the town of " + townName + " goes to bed. The night will start in 30 seconds.")
                await night(30)
        else:
            print(result)
            await stopGame()

            
async def delayStartNight(time):
    global voting
    global gameIsRunning
    if gameIsRunning:
        await asyncio.sleep(time)
        if not voting:
            await bot.send_message(origChannel, "Since no one else was nominated, the night will start momentarily.")
            await night(1)

async def displayLog(person):
    global playerObjectList
    global origChannel
    if gameIsRunning:
        if person.diary != []:
            num = 1
            await bot.send_message(origChannel, person.player.mention + "'s diary reads:")
            for i in person.diary:
                await bot.send_message(origChannel, str(num) + ". " + str(i))
                num += 1
        else:
            await bot.send_message(origChannel, person.player.mention + "'s diary is blank.")
    

        
async def displayTeam(person):
    global origChannel
    global gameIsRunning
    if gameIsRunning:
        if person.team == "villager":
            await bot.send_message(origChannel, person.player.mention + " was on the villager team.")
        elif person.team == "werewolf":
            await bot.send_message(origChannel, person.player.mention + " was on the werewolf team.")
        else:
            await bot.send_message(origChannel, person.player.mention + " was on neither the villager or werewolf team.")

        
async def nominate(message):
    global playerObjectList
    global nominees
    global nominators
    global gameIsRunning
    if gameIsRunning:
        nominee = None
        args = message.content.split(" ")
        if len(args) > 1:
            nomineeName = str(" ".join(args[1:]))
            print("nominate command when through")
            nominee = await targetPlayer(nomineeName, message)
            if nominee not in nominees:
                print("nominate - through the nominee not in nominees if statement")
                nominators[nominee] = getPlayerObject(message.author)
                nominees.append(nominee)
                await bot.send_message(origChannel, message.author.mention + " has nominated " + nominee.player.mention + "!")
            else:
                await bot.send_message(message.author, nominee.player.display_name + " has already been nominated.")

async def eat(message):
    global playerObjectList
    global werewolfVote
    global werewolfChannel
    global userList
    global allWerewolvesVoted
    global gameIsRunning
    if gameIsRunning:
        attemptedTarget = None
        target = None
        author = None
        args = message.content.split(" ")
        author = getPlayerObject(message.author)
        if author.usedAbility == True:
            await bot.send_message(author.player, "You've already voted tonight!")
        elif len(args) > 1:
            attemptedTarget = str(" ".join(args[1:]))
        for x in playerObjectList:
            if x.playerName.upper() == attemptedTarget.upper() or x.player.display_name.upper() == attemptedTarget.upper():
                target = x
        if target == None:
            await bot.send_message(message.author, "No match was found for the player name you entered. Make sure it was spelled correctly, and then try again.")
        else:
            vote = target
            werewolfVote.append(target)
            await bot.send_message(werewolfChannel, str(author.player.display_name) + " has voted for " + str(target.player.display_name))
            author.usedAbility = True
            allWerewolvesVoted = True
            for person in playerObjectList:
                if person.role == "werewolf":
                    if person.usedAbility == False:
                        allWerewolvesVoted = False
            if allWerewolvesVoted == True:
                victim = await tallyVote(werewolfVote)
                haveWerewolvesEaten = True
                victim.wasAttacked = True
                victim.causeOfDeath = " made a fine dinner for the werewolves last night."
                await bot.send_message(werewolfChannel, "You have chosen to attack " + victim.player.display_name)
                werewolfVote = []
    
async def setDefaultVars():
    global gameIsRunning
    global playerObjectList
    global origChannel
    global adminUser
    global canJoin
    global userList
    global MIN_PLAYERS
    global time
    global werewolfChannel
    global townName
    global haveWerewolvesEaten
    global nominationsToday
    global canNominate
    global nominees
    global vote
    global isFirstNight
    global timeToVote
    global nominators
    global canNominate
    global voting
    global votedLive
    global votedDie

    gameIsRunning = False
    playerObjectList = []
    origChannel = None
    adminUser = None
    canJoin = False
    userList = []
    MIN_PLAYERS = 7
    time = None
    werewolfChannel = None
    townName = None
    isFirstNight = True
    haveWerewolvesEaten = False
    werewolfVote = []
    allWerewolvesVoted = False
    nominationsToday = 0
    canNominate = False
    nominees = []
    vote = []
    timeToVote = False
    nominators = {}
    voting = False
    votedLive = []
    votedDie = []

    

async def targetPlayer(name, message):
    global gameIsRunning
    global playerObjectList
    if gameIsRunning:
        target = None
        for x in playerObjectList:
            if x.playerName.upper() == name.upper() or x.player.display_name.upper() == name.upper():
                target = x
                return target
        if target == None:
            await bot.send_message(message.author, "No match was found for the player name you entered. Make sure it was spelled correctly, and then try again.")
            return None

async def tallyVote(vote, message=None):
    global gameIsRunning
    target = None
    if gameIsRunning:
        biggestValue = 0
        tempVote = []
        for i in vote:
            tempVote.append(i)
        unluckyPerson = None
        live = 0
        die = 0
        tally = Counter(tempVote)
        for person in vote:
            if "live" or "die" not in vote and vote != []:
                if tally[person] > biggestValue:
                    tally[person] = biggestValue
                    unluckyPerson = person
        for entry in vote:
            if entry == "live":
                live += 1
            elif entry == "die":
                die += 1
        print("live = " + str(live))
        print("die = " + str(die))
        print("Tally vote - vote = " + str(vote))
        if "live" not in vote and "die" not in vote and vote != []:
            print("Returned option #1")
            target = unluckyPerson
            return target
        elif vote == []:
            print("Returned option #2")
            return unluckyPerson
        elif "live" in vote or "die" in vote:
            if live >= die:
                print("result = live")
                return "live"
            else:
                print("result = die")
                return "die"

async def setUp(message):
    global gameIsRunning
    global origChannel
    global adminUser
    global canJoin
    global userList
    print(message.author)
    origChannel = message.channel
    adminUser = message.author
    gameIsRunning = True
    await bot.send_message(origChannel, "@everyone, " + adminUser.mention + " has started a game of Werewolf! Use the \"w!join\" command to join their game!")
    canJoin = True
    userList.append(adminUser)


async def deleteMessage(message):
        try:
            await bot.delete_message(message)
        except discord.errors.Forbidden:
            return


async def joinGame(user, message):
    global userList
    global adminUser
    global gameIsRunning
    if gameIsRunning:
        if user not in userList:
            userList.append(user)
            await bot.send_message(user, "You have joined " + adminUser.display_name + "'s game!")
            await bot.send_message(adminUser, user.display_name + " has joined your game.")

async def startGame(message):
    global userList
    global adminUser
    global origChannel
    global playerObjectList
    global townName
    global gameIsRunning
    if gameIsRunning:
        if townName == None:
            townName = random.choice(["Villaville", "Radiator Springs", "Springfield", "Nowhere", "Bedrock", "Smallville"])
        numPlayers = len(userList)
        print("numPlayers = " + str(numPlayers))
        await classListGenerator(numPlayers)
        print("\nstartGame - playerObjectList:\n")
        for i in playerObjectList:
            print(i.playerName + ": " + i.role)
        await bot.send_message(origChannel, "@everyone, the game is afoot! Check your direct messages from Werewolf Bot to see your role.")
        await bot.send_message(origChannel, "You have 30 seconds to look at your role and talk with one another before the first night starts.")
        for person in playerObjectList:
            await bot.send_message(person.player, person.description)
        await firstNight(30, message)

async def classListGenerator(numPlayers):
    global canJoin
    global MIN_PLAYERS
    global playerObjectList
    global gameIsRunning
    if gameIsRunning:
        canJoin = False
        total = 0
        defaultClasses = [playableClasses.werewolf, playableClasses.villager, playableClasses.villager, playableClasses.villager, playableClasses.seer, playableClasses.bodyguard, playableClasses.werewolf]
        selections = []
        negativeClasses = [playableClasses.werewolf, playableClasses.sorceress, playableClasses.vampire]

        positiveClasses = [playableClasses.lalma, playableClasses.bodyguard, playableClasses.villager, playableClasses.seer, playableClasses.spellcaster]

        allClasses = [playableClasses.werewolf, playableClasses.villager, playableClasses.seer, playableClasses.bodyguard, playableClasses.sorceress, playableClasses.spellcaster, playableClasses.lalma, playableClasses.vampire]


        if numPlayers >= (MIN_PLAYERS + 2):
            while True:
                total = 0
                selections = []
                for num in range(numPlayers - MIN_PLAYERS):
                    if total == 0:
                        x = random.choice(allClasses)
                        selections.append(x)
                        total += x.score
                    elif total > 0:
                        y = random.choice(negativeClasses)
                        selections.append(y)
                        total += y.score
                    elif total < 0:
                        z = random.choice(positiveClasses)
                        selections.append(z)
                        total += z.score
                    print(total)
                if total == 0:
                    break
                else:
                    print("Bad final total: " + str(total))
        elif numPlayers == (MIN_PLAYERS + 1):
            selections.append(positiveClasses[0])
            total += 1
        
        
        print("Final total is: " + str(total))
        if selections != []:
            for x in selections:
                defaultClasses.append(x)
        for i in range(numPlayers):
            randClass = random.choice(defaultClasses)
            playerObject = randClass()
            playerObject.playerName = userList[i].name
            playerObject.displayName = userList[i].display_name      
            playerObject.player = userList[i]
            playerObjectList.append(playerObject)
            defaultClasses.remove(randClass)
            print("i = " + str(i) + ", " + str(playerObjectList[i].player.name) + ": " + str(playerObjectList[i].role))

def getPlayerObject(user):
    global gameIsRunning
    if gameIsRunning:
        temp = None
        for person in playerObjectList:
            if person.player == user:
                temp = person
                return temp
        if temp == None:
            return None

async def useAbility(message):
    global gameIsRunning
    if gameIsRunning:
        args = message.content.split(" ")
        attemptedTarget = None
        target = None
        if getPlayerObject(message.author).usedAbility == False and getPlayerObject(message.author).role != "lalma" and len(args) > 1:
            attemptedTarget = str(" ".join(args[1:]))
            print(attemptedTarget)
            target = await targetPlayer(attemptedTarget, message)
            if target != None:
                feedback = getPlayerObject(message.author).ability(target)
                await bot.send_message(message.author, feedback)
                getPlayerObject(message.author).usedAbility = True

async def checkWin():
    global playerObjectList
    global origChannel
    global gameIsRunning
    if gameIsRunning:
        whoWon = None
        werewolvesWon = True
        villagersWon = False
        vampireWon = False
        print("Checking win")
        #check if werewolves won
        print("checking if werewolves won")
        for person in playerObjectList:
            if person.team != "werewolf":
                werewolvesWon = False
                print(person.player.display_name + " is not a werewolf")
        if werewolvesWon:
            print("werewolves won")
            await bot.send_message(origChannel, "The werewolves have overtaken the town and won the game!")
            await stopGame()
            whoWon = "werewolves"
            return whoWon
        print("checking if villagers won")
        #check if villagers won
        villagersWon = True
        for person in playerObjectList:
            if person.role == "werewolf" or person.role == "vampire":
                villagersWon = False
                print(person.player.display_name + " is either a werewolf or vampire")
        if villagersWon:
            print("villagers won")
            await bot.send_message(origChannel, "The villagers have won the game!")
            await stopGame()
            whoWon = "villagers"
            return whoWon
        print("checking if vampire won")
        #check if vampire won
        vampireWon = True
        for person in playerObjectList:
            if person.role != "vampire":
                vampireWon = False
                print(person.player.display_name + " is not a vampire")
        if vampireWon:
            print("vampire(s) won")
            await bot.send_message(origChannel, "The vampire won the game!")
            await stopGame()
            whoWon = "vampire"
            return whoWon
        if whoWon == None:
            return None

async def firstNight(delay, message):
    global playerObjectList
    global origChannel
    global time
    global werewolfChannel
    global townName
    global isFirstNight
    global gameIsRunning
    global userList
    if gameIsRunning:
        await asyncio.sleep(delay)
        if gameIsRunning:
            muted = discord.PermissionOverwrite(send_messages = False)
            print("\nfirstNight - playerObjectList.player:")
            for i in playerObjectList:
                print(i.player)
            for person in playerObjectList:
                print(str(person.player))
                await bot.edit_channel_permissions(origChannel, person.player, muted)
                print("Success! " + person.player.display_name + " is muted for the first night.")
            time = "night"
            await bot.send_message(origChannel, "The first night has begun. Tired after a long day, the people of " + townName + " go to bed.")
            await bot.send_message(origChannel, "Players with abilities will have 2 minutes to use them.")
            #create a private channel for the werewolves and set permissions
            werewolfChannel = await bot.create_channel(message.server, "Wolf Den")
            werewolfPerms = discord.PermissionOverwrite(read_messages = True, send_messages=True, read_message_history=True)
            muteAndDeaf = discord.PermissionOverwrite(read_messages = False, send_messages=False, read_message_history = False)
            mute = discord.PermissionOverwrite(read_messages = True, send_message=False, read_message_history = True)
            for x in message.server.members:
                await bot.edit_channel_permissions(werewolfChannel, x, muteAndDeaf)
            for i in playerObjectList:
                if i.role == "werewolf":
                    await bot.edit_channel_permissions(werewolfChannel, i.player, werewolfPerms)
                else:
                    await bot.edit_channel_permissions(werewolfChannel, i.player, muteAndDeaf)

            await bot.send_message(werewolfChannel, "You cannot attack anyone on the first night. Use the time to get to know your fellow werewolves.")
            
            await day(60)

async def night(delay):
    global gameIsRunning
    global playerObjectList
    global origChannel
    global adminUser
    global canJoin
    global userList
    global MIN_PLAYERS
    global time
    global werewolfChannel
    global townName
    global haveWerewolvesEaten
    global nominationsToday
    global canNominate
    global nominees
    global vote
    global timeToVote
    if gameIsRunning:
        vote = []
        timeToVote = False
        time = "night"
        haveWerewolvesEaten = False
        for person in playerObjectList:
            person.invulnerable = False
            person.hasVoted = False
            person.silenced = False
            person.wasAttacked = False
            if person.role != "lalma":
                person.usedAbility = False
        await asyncio.sleep(delay)
        muted = discord.PermissionOverwrite(send_messages = False)
        unmuted = discord.PermissionOverwrite(send_messages = True)
        for person in playerObjectList:
            await bot.edit_channel_permissions(origChannel, person.player, muted)
        await bot.send_message(origChannel, "@everyone, it is now night. Players with abilities will have 2 minutes to use them.")
        await day(120)


async def day(delay):
    global playerObjectList
    global origChannel
    global time
    global townName
    global isFirstNight
    global werewolfVote
    global nominationsToday
    global canNominate
    global allWerewolvesVoted
    global haveWerewolvesEaten
    global nominationsToday
    global gameIsRunning
    await asyncio.sleep(delay)
    if gameIsRunning:
        muted = discord.PermissionOverwrite(send_messages = False)
        unmuted = discord.PermissionOverwrite(send_messages = True)
        time = "day"
        allWerewolvesVoted = False
        nominationsToday = 0
        isFirstNight = False
        if werewolfVote != []:
            victim = await tallyVote(werewolfVote)
            victim.wasAttacked = True
            haveWerewolvesEaten = True
            werewolfVote = []
            victim.causeOfDeath = " was torn to shreds by werewolves last night."
        await bot.send_message(origChannel, "@everyone, the sun rises on the town of " + townName + ".")
        for person in playerObjectList:
            if person.role != "lalma":
                person.usedAbility = False
            if person.wasAttacked == True and person.invulnerable == False:
                await bot.send_message(origChannel, person.player.mention + person.causeOfDeath)
                await displayLog(person)
                await displayTeam(person)
                if person.role == "werewolf":
                    await bot.edit_channel_permissions(werewolfChannel, person.player, muted)
                await bot.edit_channel_permissions(origChannel, person.player, muted)
                playerObjectList.remove(person)
            elif person.wasAttacked == True and person.invulnerable == True:
                await bot.send_message(origChannel, person.player.mention + " was attacked last night, but miraculously survived.")
                person.wasAttacked = False
                person.invulnerable = False
                person.causeOfDeath = None
        
        print("\n\nChecking win for overnight kills\n\n")
        whoWon = await checkWin()

        if whoWon == None:
            for person in playerObjectList:
                if person.silenced == False:
                    await bot.edit_channel_permissions(origChannel, person.player, unmuted)
                else:
                    person.silenced = False
                    await bot.send_message(person.player, "You have been silenced. You cannot talk for today.")
            await bot.send_message(origChannel, "You have 60 seconds to talk amongst yourselves before nominations can begin.")
            await asyncio.sleep(60)
            await bot.send_message(origChannel, "You may now start nominating people! Use the \"w!nominate [player name here]\" command to nominate someone, and use the \"w!second [player name here]\" command to second someone. You have 30 seconds to nominate someone before the next night will begin automatically.")
            canNominate = True
            for person in playerObjectList:
                if person.markedByVampire == True:
                    await bot.send_message(origChannel, person.player.mention + " feels a sharp pain in their chest and falls to the ground.")
                    await displayLog(person)
                    await displayTeam(person)
                    await bot.send_message(person.player, "You had a heart attack and died.")
                    if person.role == "werewolf":
                        await bot.edit_channel_permissions(werewolfChannel, person.player, muted)
                    await bot.edit_channel_permissions(origChannel, person.player, muted)
                    playerObjectList.remove(person)
            print("\n\nChecking win for vampire kills\n\n")
            test = await checkWin()
            if test == None:
                await asyncio.sleep(30)
                if nominationsToday == 0:
                    canNominate = False
                    await bot.send_message(origChannel, "No one was nominated and seconded today. The night will start in 30 seconds.")
                    await night(30)

bot.run("Token goes here")
