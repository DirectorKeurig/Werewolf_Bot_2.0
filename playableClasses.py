import asyncio

class villager(object):
    role = "villager"
    team = "villager"
    score = 1
    playerName = None
    player = None
    alive = True
    description = "You are a Villager. Find the werewolves and lynch them before they eat you. You win when all the werewolves are dead."
    hasNonWerewolfAbility = False
    invulnerable = False
    usedAbility = False
    hasAbility = False
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def setDefaults():
        role = "villager"
        team = "villager"
        score = 1
        playerName = None
        player = None
        alive = True
        description = "You are a Villager. Find the werewolves and lynch them before they eat you. You win when all the werewolves are dead."
        hasNonWerewolfAbility = False
        invulnerable = False
        usedAbility = False
        hasAbility = False
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None
    
    
class werewolf(object):
    role = "werewolf"
    team = "werewolf"
    score = -6
    playerName = None
    player = None
    alive = True
    description = "You are a Werewolf. Wake up each night to choose a player to eat, and don't get lynched during the day. Use the command \"w!eat [player name]\" IN THE WOLF-DEN CHANNEL to vote to eat someone. You win when all the players on the villager team are dead."
    hasNonWerewolfAbility = False
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def setDefaults():
        role = "werewolf"
        team = "werewolf"
        score = -6
        playerName = None
        player = None
        alive = True
        description = "You are a Werewolf. Wake up each night to choose a player to eat, and don't get lynched during the day. Use the command \"w!eat [player name]\" IN THE WOLF-DEN CHANNEL to vote to eat someone. You win when all the players on the villager team are dead."
        hasNonWerewolfAbility = False
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None
    
class seer(object):
    role = "seer"
    team = "villager"
    score = 7
    playerName = None
    player = None
    alive = True
    description = "You are the seer. Wake up each night to find out whether or not a player is a werewolf. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to check if someone is a werewolf. You win when all the werewolves are dead."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def ability(player):
        if player == werewolf:
            return str(player.playerName) + " is a werewolf."
        else:
            return str(player.playerName) + " is not a werewolf."

    def setDefaults():
        role = "seer"
        team = "villager"
        score = 7
        playerName = None
        player = None
        alive = True
        description = "You are the seer. Wake up each night to find out whether or not a player is a werewolf. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to check if someone is a werewolf. You win when all the werewolves are dead."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None


class bodyguard(object):
    role = "bodyguard"
    team = "villager"
    score = 3
    playerName = None
    player = None
    alive = True
    description = "You are the bodyguard. Wake up each night to choose someone to protect. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to protect someone for the night. You win when all the werewolves are dead."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def ability(player):
        player.invulnerable =  True
        return str(player.playerName + " is under your protection for the night.")

    def setDefaults():
        role = "bodyguard"
        team = "villager"
        score = 3
        playerName = None
        player = None
        alive = True
        description = "You are the bodyguard. Wake up each night to choose someone to protect. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to protect someone for the night. You win when all the werewolves are dead."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None

class sorceress(object):
    role = "sorceress"
    team = "werewolf"
    score = -3
    playerName = None
    player = None
    alive = True
    description = "You are the sorceress. Wake up each night to find out if someone is the seer. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to find out if that player is the seer. You win if the werewolves win."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def ability(player):
        if player == seer:
            return player.playerName + " is the seer."
        else:
            return player.playerName + " is not the seer."

    def setDefaults():
        role = "sorceress"
        team = "werewolf"
        score = -3
        playerName = None
        player = None
        alive = True
        description = "You are the sorceress. Wake up each night to find out if someone is the seer. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to find out if that player is the seer. You win if the werewolves win."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None

class spellcaster(object):
    role = "spellcaster"
    team = "villager"
    score = 1
    playerName = None
    player = None
    alive = True
    description = "You are the Spellcaster. Wake up each night to choose a player to silence. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to find out if that player is the seer. You win if the villagers win."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def ability(player):
        player.silenced = True

    def setDefaults():
        role = "spellcaster"
        team = "villager"
        score = 1
        playerName = None
        player = None
        alive = True
        description = "You are the Spellcaster. Wake up each night to choose a player to silence. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to find out if that player is the seer. You win if the villagers win."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None
        
class vampire(object):
    role = "vampire"
    team = "self"
    score = -7
    playerName = None
    player = None
    alive = True
    description = "You are the Vampire. Wake up each night and choose a player to die during tomorrow's nominations. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to mark that player for death tomorrow. You win if you are the last one left alive."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def ability(player):
        player.markedByVampire = True
        return player.playerName + " has been marked for tomorrow's nominations."

    def setDefaults():
        role = "vampire"
        team = "self"
        score = -7
        playerName = None
        player = None
        alive = True
        description = "You are the Vampire. Wake up each night and choose a player to die during tomorrow's nominations. Use the command \"w!ability [player name here]\" IN THIS DM ONLY to mark that player for death tomorrow. You win if you are the last one left alive."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None

class lalma(object):
    role = "lalma"
    team = "villager"
    score = 3
    playerName = None
    player = None
    alive = True
    description = "You are the Lalma. You may choose a player with the command \"w!reveal [player name here]\" DURING THE DAY and IN THIS DM to immediately reveal their role. Using this ability will not reveal your role. You may only use your ability ONCE. You win when the villagers win."
    hasNonWerewolfAbility = True
    invulnerable = False
    usedAbility = False
    hasAbility = True
    hasVoted = False
    markedByVampire = False
    silenced = False
    wasAttacked = False
    causeOfDeath = None

    def setDefaults():
        role = "lalma"
        team = "villager"
        score = 3
        playerName = None
        player = None
        alive = True
        description = "You are the Lalma. You may choose a player with the command \"w!reveal [player name here]\" DURING THE DAY and IN THIS DM to immediately reveal their role. Using this ability will not reveal your role. You may only use your ability ONCE. You win when the villagers win."
        hasNonWerewolfAbility = True
        invulnerable = False
        usedAbility = False
        hasAbility = True
        hasVoted = False
        markedByVampire = False
        silenced = False
        wasAttacked = False
        causeOfDeath = None
