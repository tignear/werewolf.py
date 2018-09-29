from enum import Enum,auto
from copy import copy
import asyncio
class GameLogicError(Exception):
    pass
class Role(Enum):
    WOLF=auto()
    VILLAGER=auto()
    FORTUNETELLER=auto()
    MEDIUM=auto()
    HUNTER=auto()
    IMMORALIST=auto()
SET_OF_FORETELLS_RESULT_BLACK=frozenset({
    Role.WOLF
})
SET_OF_WOLF_CAMP=frozenset({
    Role.WOLF,Role.IMMORALIST
})
SET_OF_WOLF_COUNT_IN=SET_OF_FORETELLS_RESULT_BLACK
class Player:
    def __init__(self,role):
        self.__role=role
        self.__live=True
    @property
    def role(self):
        return self.__role
    @property
    def live(self):
        return self.__live
    def foretells(self):
        if not self.__live:
            raise GameLogicError()
        return self.role in SET_OF_FORETELLS_RESULT_BLACK
    def inspiration(self):
        if self.__live:
            raise GameLogicError()
        return self.role in SET_OF_FORETELLS_RESULT_BLACK
    def kill(self):
        self.__live=False
class ActionPlater:
    def __init__(self,player):
        self.__player=player
    @property
    def player(self):
        return self.__player
    def action(self):
            pass
class DayActionPlayer(ActionPlater):
    def __init__(self,player):
        super().__init__(player)
        self.__vote=False
    def voteKill(self):
        self.__vote==True
    def action(self):
            if self.__vote:
                self.player.kill()
class NightActionPlayer(ActionPlater):
    def __init__(self,player):
        super().__init__(player)
        """constructor
        
        Parameters
        ----------
        player : Player
        """
        self.__guarding=False
        self.__attacked=False
    def guard(self):
        self.__guarding=True
    def attack(self):
        self.__attacked=True
    def foretells(self):
        return self.player.foretells()
    def inspiration(self):
        return self.player.inspiration()
    def action(self):
        if self.__attacked and not self.__guarding :
            self.player.kill()

class GameWinner(Enum):
    NONE=auto()
    WOLF=auto()
    VILLAGER=auto()
class Game:
    def __init__(self,players,settings={}):
        """constructor
        
        Parameters
        ----------
        players : {Player}
        settings: {str:any}
        """
        self.__players=copy(players)
        self.__livePlayers=copy(players)
    @property
    def players(self):
        return frozenset(self.__players)
    @property
    def livePlayers(self):
        return frozenset(self.__livePlayers)
    async def day(self,actPlayer):
        """require overriding
        
        Parameters
        ----------
        self : 
            
        
        """
        pass
    async def night(self,actPlayer):
        """actPlayer
        
        Parameters
        ----------
        actPlayer : [type]
            [description]
        
        """
        pass
    def __updateLivePlayer(self):
        newLivePlayer=filter(lambda x:x.live,self.__livePlayers)
        diedPlayer=self.__livePlayers-newLivePlayer
        self.__players=newLivePlayer
        self.playerDied(diedPlayer)
    def __checkComplete(self):
        playerCount=len(self.__livePlayers)
        wolfCampCount=len(set(filter(lambda x:x.player.role in SET_OF_WOLF_COUNT_IN,self.__livePlayers)))
        villagerCount=playerCount-wolfCampCount
        res=None
        if wolfCampCount>=villagerCount:
            res=GameWinner.WOLF
        elif wolfCampCount==0:
            res=GameWinner.VILLAGER
        return res
    def action(self,turnPlayer):
        for e in turnPlayer:
            e.action()
        self.__updateLivePlayer()
        return self.__checkComplete()
    async def playerDied(self,setOfDiedPlayer):
        pass
    async def turn(self):
        dayactP=frozenset(map(lambda x:DayActionPlayer(x),self.__livePlayers))
        await self.day(dayactP)
        winner=self.action(dayactP)
        if winner!=None:
            return winner
        nightactP=frozenset(map(lambda x:NightActionPlayer(x),self.__livePlayers))
        await self.night(nightactP)
        winner=self.action(nightactP)
        if winner!=None:
            return winner
        return
    async def game(self):
        while True:
            winner=self.turn()
            if winner!=None:
                return winner