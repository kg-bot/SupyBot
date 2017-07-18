###
# Uno/plugin.py
# by SpiderDave
###


# -- ToDo --------------------------------
# * Add option for colors, bold
# * Configurable maximum tables and
#   tables per channel.
# ----------------------------------------

import re
import random

import supybot.utils as utils
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import time
import os
import pickle

# This will be used to change the name of the class to the folder name
PluginName=os.path.dirname( __file__ ).split(os.sep)[-1]
class _Plugin(callbacks.Plugin):
    """
    Uno!
    """
    threaded = True
    pluginpath=os.path.dirname( __file__ ) + os.sep
    
    game=[{},{},{},{},{}]

    channeloptions = {}
    channeloptions['allow_game']=False
    channeloptions['debug']=False
    channeloptions['use_queue']=True
    channeloptions['nplayers']=10
    channeloptions['maxbots']=9
    lastgame=time.time()

    def start(self, irc, msg, args, text):
        """takes no arguments
        
        Pokrece novu Uno igru.  Za pravila igre koristite komandu +rules .
        """
        try:
            self._read_options(irc)
        except:
            pass
        if self.channeloptions['allow_game']==False:
            irc.reply('Error: allow_game=False')
            return

        # may want to add a game variant later
        if text:
            gametype=text.lower().strip()
            if gametype.replace(' ', '')=='globalthermalnuclearwar':
                irc.reply('Curious game.  The only winning move is not to play.')
                return
            if gametype not in ['uno']:
                irc.reply('Error: Invald game type %s.' % gametype)
                return
        else:
            gametype='uno'
        nick=msg.nick
        table=self._gettablefromnick(nick)
        if table != None:
            gametype=self.game[table].get('type').capitalize()
            irc.reply('Error: You are already in a game of %s.' % gametype)
            return
        
        table=self._getopentable()
        if table==None:
            irc.reply('Sorry, all the game tables are in use at the moment.')
            return

        self._cleanup(table)
        self.game[table]['channel']=msg.args[0]
        self.game[table]['type']=gametype
        
        
        if gametype=='uno':
            self.game[table]['players'][nick]={}
            #self.game[table]['nplayers']=int(self.channeloptions[gametype+'_nplayers'])
            self.game[table]['nplayers']=int(self.channeloptions['nplayers'])
            irc.reply('%s je pokrenuo novu %s igru za stolom %s.  Da vidite pravila igre, kucajte "+rules" bez navodnika.  Da se ukljucite u igru koristite komandu, "+uno join" bez navodnika.  Da bi ste dodali bot igraca, kucajte "+uno join cpu" bez navodnika.' % (nick, gametype.capitalize(), table+1), prefixNick=False)
        self.game[table]['phase']='join'
        
    start = wrap(start, ['public', optional('something')])

    def begin(self, irc, msg, args):
        """
        begin uno game
        """
        self._uno_begin(irc,msg.nick)
    begin = wrap(begin)

    def _uno_begin(self, irc, nick):
        """
        test
        """
        table=self._gettablefromnick(nick)
        if table==None:
            irc.reply('Error: Ne igrate ni za jednim stolom.')
            return
        if self.game[table]['type']!='uno':
            irc.reply('Error: Nije Uno igra.')
            return
        if self.game[table]['phase']!='join':
            irc.reply("Error: Ne mozete koristiti ovu komandu sada.")
            return
        nplayers=self.game[table]['players'].keys()
        if nplayers<2:
            irc.reply('Error: Minimalan broj igraca za Uno je 2.')
            return
        # start things for real
        for n in self.game[table]['players'].keys():
            self.game[table]['players'][n]['hand']=[]
            # each player draws 7 initial cards
            for i in range(0,7):
                card=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
                self.game[table]['players'][n]['hand'].append(card)
        self.game[table]['phase']='running'
        irc.reply('Igra je pocela!  Pratite vas PM i sledite instrukcije koje vam bot daje.', prefixNick=False, to=self.game[table]['channel'])
        for n in self.game[table]['players'].keys():
            self._uno_tell_status(irc, n)
        self._uno_do_cpu(irc, table)

    def _uno_do_cpu(self, irc, table):
        while(1):
            if self.game[table].get('phase')!='running':
                return
            if self.game[table].get('type')!='uno':
                return
            turnplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
            if self.game[table]['players'][turnplayer].get('cpu'):
                self._uno_cpu_play(irc, table)
            else:
                return
    
    
    def _uno_tell_status(self, irc, nick):
        """
        test
        """
        table=self._gettablefromnick(nick)
        if table==None:
            irc.reply('Error: Ne igrate ni za jednim stolom.')
            return
        channel=self.game[table]['channel']
        opponents=[p for p in self.game[table]['players'].keys() if p!=nick]
        opponent=opponents[0]
        opponent_cards=['%s has %s cards' % (n,len(self.game[table]['players'][n]['hand'])) for n in self.game[table]['players'].keys() if n!=nick]
        opponent_cards=', '.join(opponent_cards)
        topcard=self.game[table]['discard'][-1]
        if 'Wild' in topcard:
            topcard='%s (%s)' % (topcard, self.game[table].get('wildcolor'))
        
        yourhand=utils.str.commaAndify(self.game[table]['players'][nick]['hand'])
        ncards=len(self.game[table]['players'][nick]['hand'])
        opponent_ncards=len(self.game[table]['players'][opponent]['hand'])
        turnplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
        if turnplayer==nick:
            if self.game[table]['players'][turnplayer].get('cpu'):
                # We'll skip notice in the channel since the cpu player will
                # take their turn quickly, and no need to announce it.
                pass
            else:
                txt="%s je na redu.  Trenutna karta na stolu je %s." % (nick, topcard)
                txt=txt.replace("s's","s'")
                irc.reply(txt, to=channel)
                turnplayer='your'
                txt='Ti si na redu.  Trenutna karta na stolu je %s.  Ti imas %s karata (%s). %s.  Da bi odigrao kartu, koristi komandu "+uno play Zeljena-Karta" .' % (topcard, ncards, yourhand, opponent_cards)
                self.reply(irc, txt, to=nick, private=True)
        else:
            pass

    def _uno_is_valid_play(self, table, card, discard):
        if card=='Wild':
            # Wild draw 4 is always a valid play for now
            return True
        if card=='Wild Draw 4':
            turnplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
            if 'Wild Draw 4' in self.game[table]['players'][turnplayer]['hand']:
                if 'Wild' in discard:
                    # can't play it, because wild draw 4 is black and color of last card
                    # played is black (going by the letter of the rules).
                    return False
                else:
                    discardcolor=discard.split(' ',1)[0]
                    for c in self.game[table]['players'][turnplayer]['hand']:
                        if discardcolor in c:
                            return False
            return True
            
        unocolors=['Blue','Green','Red','Yellow']
        for color in unocolors:
            if color in card:
                if 'Wild' in discard:
                    # Wild or Wild Draw 4
                    if color==self.game[table].get('wildcolor'):
                        return True
                    else:
                        return False
                if color in discard:
                    # Color matches
                    return True
                if card.split(' ', 1)[1]==discard.split(' ', 1)[1]:
                    # Number or word matches
                    return True
        return False

    def _uno_draw_card(self, table, player):
        card=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
        self.game[table]['players'][player]['hand'].append(card)
        if len(self.game[table]['deck'])==0:
            self.game[table]['deck']=self.game[table]['discard']
            self.game[table]['discard']=[]
            random.shuffle(self.game[table]['deck'])
            topcard=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
            self.game[table]['discard'].append(topcard)
        return card

    def tellstatus(self, irc, msg, args):
        """?"""
        self._uno_tell_status(irc, msg.nick)
    tellstatus=wrap(tellstatus)

    def rules(self, irc, msg, args, text):
        """takes no arguments
        
        Prikazuje pravila igre.  Pokreni Uno sa komandom "+uno start" .
        """
        if text:
            gametype=text.lower().strip()
        else:
            gametype='uno'
        if gametype=='uno':
            irc.reply('Pravila igre Uno: http://www.pjesmicezadjecu.com/drustvene-igre-pravila-igre/uno.html')
        else:
            irc.reply('Unknown game type.')
    rules=wrap(rules, [additional('text')])
    
    def join(self, irc, msg, args, table, fakenick):
        """[<sto>]
        
        Ubacuje te u igru za nekim od stolova . 
        Koristi <sto> ukoliko se na kanalu igra za vise od jednog stola.
        """
        try:
            self._read_options(irc)
        except:
            pass
        if self.channeloptions['allow_game']==False:
            irc.reply('Error: allow_game=False')
            return

        nick=msg.nick
        if table !=None: table-=1 # make tables zero based
        tables=self._getcurrenttables()
        if not tables:
            # no games running
            irc.reply('Error: Nema stola gde mozete da se pridruzite.')
            return
        if table !=None and table not in tables:
            # given table doesn't have a game going
            if table not in range(len(self.game)):
                irc.reply("Error: Zeljeni sto ne postoji")
                return
            irc.reply("Error: Za tim stolom se ne igra Uno")
            return
        tables=[t for t in tables if self.game[t]['channel']==msg.args[0]]
        if table !=None:
            if table not in tables:
                irc.reply('Error: Taj sto se ne nalazi na ovom kanalu.')
                return
            tables=[table] # success!
        if len(tables)==0:
            irc.reply('Error: Na kanalu trenutno nema igara kojima mozete da se pridruzite.')
            return
        elif len(tables)==1:
            table=tables[0]
        else:
            messagetxt="Preciziraj za kojim stolom zelis da igras sa komandom '+uno join <table>'.  Trenutni stolovi su: "
            for t in tables:
                messagetxt+='Table %s (%s), ' % (t+1, ' '.join(self.game[t]['players'].keys()))
            messagetxt=messagetxt.rsplit(', ',1)[0]+'.'
            irc.reply(messagetxt)
            return
        isfake=False
        iscpu=False
        if ((self.channeloptions['debug']) and fakenick) or (fakenick and fakenick.lower()=='cpu'):
            nick=fakenick
            isfake=True
            if fakenick.lower()=='cpu': iscpu=True
        if self.game[table]['phase']=='join':
            if nick in self.game[table]['players'].keys():
                irc.reply('Error: Vec si seo za taj sto.')
                return
            if self.game[table]['type']=='uno':
                self._init_uno(table)
                if iscpu==True:
                    nick=self._uno_make_cpu(table)
                else:
                    self.game[table]['players'][nick]={}
                if isfake==True:
                    self.game[table]['players'][nick]['fake']=True
                
                if len(self.game[table]['players'].keys()) < self.game[table]['nplayers']:
                    irc.reply('%s se pridruzio igri %s za stolom %s.  Koristi komandu +uno begin da pokrenes igru.' % (nick,self.game[table]['type'],table+1), prefixNick=False, to=self.game[table]['channel'])
                    return
                
                for n in self.game[table]['players'].keys():
                    self.game[table]['players'][n]['hand']=[]
                    # each player draws 7 initial cards
                    for i in range(0,7):
                        card=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
                        self.game[table]['players'][n]['hand'].append(card)
                irc.reply('Igra je pocela!  Pratite vas PM i sledite instrukcije koje vam bot daje.', prefixNick=False, to=self.game[table]['channel'])
                for n in self.game[table]['players'].keys():
                    self._uno_tell_status(irc, n)
            self.game[table]['phase']='running'
        else:
            if self.game[table]['phase']=='running':
                irc.reply('Error: Igra je vec pokrenuta.')
                return
            elif self.game[table]['phase']=='':
                irc.reply('Error: Treba prvo da otvorite igru sa komandom "+uno start" .')
                return
            else:
                # don't know when this would happen, but whatever
                irc.reply('Error: not join phase.')
                return
    join = wrap(join, ['public', optional('int'), optional('something')])

    def leave(self, irc, msg, args, fakenick):
        """takes no arguments
        
        Leave a game of Uno.
        """
        try:
            self._read_options(irc)
        except:
            pass
        if self.channeloptions['allow_game']==False:
            irc.reply('Error: allow_game=False')
            return

        nick=msg.nick
        if self.channeloptions['debug'] and fakenick:
            nick=fakenick
        table=self._gettablefromnick(nick)
        if table==None:
            irc.reply('Error: Ne igrate ni za jednim stolom.')
            return
            
        if self.game[table].get('type')=='uno':
            self._leavegame(irc, msg, nick)
            self._uno_do_cpu(irc, table) # only works if game type is uno
            return
    leave = wrap(leave, ['public', optional('something')])

    def _leavegame(self, irc, msg, nick):
        """takes no arguments
        
        Leave a game of Uno.
        """
        try:
            self._read_options(irc)
        except:
            pass
        if self.channeloptions['allow_game']==False:
            irc.reply('Error: allow_game=False')
            return

        table=self._gettablefromnick(nick)
        if table==None:
            return
        
        # ---- replace with cpu ----
        oldnick=nick
        nick=self._uno_make_cpu(table)
        del self.game[table]['players'][nick] # remove new cpu player (we just want the nick)

        self.game[table]['players'][nick]=self.game[table]['players'][oldnick]
        del self.game[table]['players'][oldnick]
        self.game[table]['players'][nick]['fake']=True
        self.game[table]['players'][nick]['cpu']=True

        irc.reply('%s has been replaced by %s.' % (oldnick, nick), prefixNick=False, to=self.game[table]['channel'])
        return

    def _init_uno(self, table):
        self.game[table]['deck']=[]
        self.game[table]['discard']=[]
        self.game[table]['wildcolor']='red'
        self.game[table]['turn']=0
        self.game[table]['direction']=1
        unocolors=['Blue','Green','Red','Yellow']
        for unocolor in unocolors:
            for i in range(10):
                self.game[table]['deck'].append('%s %s' % (unocolor,i))
            for i in range(1,10):
                self.game[table]['deck'].append('%s %s' % (unocolor,i))
            for i in range(0,2):
                self.game[table]['deck'].append('%s Draw Two' % unocolor)
                self.game[table]['deck'].append('%s Reverse' % unocolor)
                self.game[table]['deck'].append('%s Skip' % unocolor)
        for i in range(0,4):
            self.game[table]['deck'].append('Wild')
            self.game[table]['deck'].append('Wild Draw 4')
        self.unodeck=[card for card in self.game[table]['deck']]
        random.shuffle(self.game[table]['deck'])
        card=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
        self.game[table]['discard'].append(card)

    def _uno_make_cpu(self, table):
        nicklist=[ 'Snarl', 'Slag', 'Sludge', 'Swoop', 'Grimlock',
                   'Data', 'Lore', 'B-4',
                   'Marvin','Deep Thought',
                   'Gort',
                   'C-3PO', 'R2-D2',
                   'Daryl',
                   'Bishop',
                   'Johnny 5',
                   'Bender', 'Flexo',
                   'Dorothy',
                   'Robot B-9',
                   'K-9',
                   'Vicki',
                   'Buffybot',
                   'Lyla',
                   'Robo',
                   'Cyrax','Sektor'
                   ]
        nicklist=[n for n in nicklist if n not in self.game[table]['players'].keys()]
        nick=random.choice(nicklist)
        #assumes nick isn't taken atm
        self.game[table]['players'][nick]={}
        self.game[table]['players'][nick]['fake']=True
        self.game[table]['players'][nick]['cpu']=True
        return nick

    def _uno_cpu_play(self, irc, table):
        channel=self.game[table]['channel']
        nick=self.game[table]['players'].keys()[self.game[table]['turn']]
        discard=self.game[table]['discard'][-1]
        novalid=True
        for c in self.game[table]['players'][nick]['hand']:
            if self._uno_is_valid_play(table, c, discard)==True:
                novalid=False
        if novalid==True:
            # draw a card
            card=self._uno_draw_card(table, nick)
            self.game[table]['players'][nick]['hasdrawn']=True
            
            if self._uno_is_valid_play(table, card, discard)==True:
                # always play the card if possible
                ncards=len(self.game[table]['players'][nick]['hand'])
                irc.reply("%s povlaci kartu i igra; Odigrao je %s (%s karata je ostalo u ruci)." % (nick, card, ncards), to=channel)
            else:
                # Can't play a card, end turn
                ncards=len(self.game[table]['players'][nick]['hand'])
                irc.reply('%s povlaci kartu (%s karti u rukama).' % (nick, ncards), to=self.game[table]['channel'])
                card=''
        else:
            # pick a random card
            playablecards=[c for c in self.game[table]['players'][nick]['hand'] if self._uno_is_valid_play(table, c, discard)==True or 'Wild' in c]
            card=random.choice(playablecards)
            if card=='Wild' or card=='Wild Draw 4':
                # Just do dumb blind color choice
                unocolors=['Blue','Green','Red','Yellow']
                self.game[table]['wildcolor']=random.choice(unocolors)
            self.game[table]['players'][nick]['hand'].remove(card)
            self.game[table]['discard'].append(card)
            ncards=len(self.game[table]['players'][nick]['hand'])
            irc.reply('%s je odigrao %s (%s karata je ostalo u ruci).' % (nick, card, ncards), to=channel)

        ncards = len(self.game[table]['players'][nick]['hand'])
        if ncards==0:
            irc.reply('The game is over.  '+ircutils.bold('%s wins!' % nick), to=channel)
            self.game[table]['phase']='gameover'
            self._cleanup(table)
            return

        if 'Reverse' in card:
            self.game[table]['direction']*=-1

        nplayers=len(self.game[table]['players'].keys())
        turn=self.game[table]['turn']+1*self.game[table]['direction']
        if turn>nplayers-1:turn=0
        if turn<0:turn=nplayers-1
        self.game[table]['turn']=turn

        if 'Draw Two' in card or 'Draw 4' in card:
            ndrawcards=2
            if 'Draw 4' in card: ndrawcards=4
            drawplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
            for n in range(ndrawcards):
                c=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
                self.game[table]['players'][drawplayer]['hand'].append(c)
            ncards=len(self.game[table]['players'][drawplayer]['hand'])
            irc.reply('%s povlaci %s karata (%s karata u ruci).' % (drawplayer, ndrawcards, ncards), to=channel)

        # Skip turn
        if 'Skip' in card or 'Draw Two' in card or 'Draw 4' in card or ('Reverse' in card and nplayers==2):
            turn=self.game[table]['turn']+1*self.game[table]['direction']
            if turn>nplayers-1:turn=0
            if turn<0:turn=nplayers-1
            self.game[table]['turn']=turn

        for n in self.game[table]['players'].keys():
            self._uno_tell_status(irc, n)
        return

    def play(self, irc, msg, args, text):
        """<kartu>
        
        Odigraj <kartu>. Primeri: "+uno play red 0", "+uno play wild blue", "+uno play draw", "+uno play done", ukoliko nemate odgovarajucu kartu onda povlacite iz spila sa komandom "+uno play draw"
        """

        nick=msg.nick
        
        table=self._gettablefromnick(nick)
        if table==None:
            irc.reply('Error: Ne igrate Uno ni za jednim stolom.')
            return
        channel=self.game[table]['channel']
        if self.channeloptions['debug'] and text.rsplit(' ',1)[-1] in self.game[table]['players']:
            fakenick=[p for p in self.game[table]['players'] if p.lower()==text.rsplit(' ',1)[-1].lower()]
            if len(fakenick)==0:
                fakenick=None
            else:
                fakenick=fakenick[0]
                nick=fakenick
                text=text.rsplit(' ',1)[:-1][0]
        
        if self.game[table]['phase']=='running':
            nplayers=len(self.game[table]['players'].keys())
            if nick not in self.game[table]['players']:
                irc.reply("Error: Ne igrate ovu igru.")
                return
            opponent=[p for p in self.game[table]['players'] if p !=nick][0]
            
            turnplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
            if nick!=turnplayer:
                # Note: it will prefix nick in private -- need to fix that
                irc.reply("%s: %s je na redu." % (nick, turnplayer), prefixNick=False)
                return
            
            text=text.strip()
            
            discard=self.game[table]['discard'][-1]
            novalid=True
            
            for c in self.game[table]['players'][nick]['hand']:
                if self._uno_is_valid_play(table, c, discard)==True:
                    novalid=False
            
            if text.lower()=='draw':
                if self.game[table]['players'][nick].get('hasdrawn')==True:
                    irc.reply('Vec si povukao kartu.')
                    return
                if novalid==False:
                    irc.reply("Ne mozes da povuces jer u ruci imas kartu koju mozes da odigras")
                    return
                else:
                    # Draw a card
                    c=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
                    self.game[table]['players'][nick]['hand'].append(c)
                    if self._uno_is_valid_play(table, c, discard)==True:
                        self.reply(irc, 'Povlacis %s sa spila.  Mozes da preskocis ovaj krug sa komandom "+uno play done"' % c, to=nick, private=True)
                        self.game[table]['players'][nick]['hasdrawn']=True
                        return
                        # card=c
                    else:
                        # Can't play a card, end turn
                        ncards=len(self.game[table]['players'][nick]['hand'])
                        self.reply(irc, 'Povlacis %s sa spila.  Nemas karata koje bi mogao da odigras, i tvoj krug je zavrsen.' % c, to=nick, private=True)
                        irc.reply('%s povlaci kartu (%s karti u rukama).' % (nick, ncards), to=self.game[table]['channel'])

                        turn=self.game[table]['turn']+1*self.game[table]['direction']
                        if turn>nplayers-1:turn=0
                        if turn<0:turn=nplayers-1
                        self.game[table]['turn']=turn

                        for n in self.game[table]['players'].keys():
                            self._uno_tell_status(irc, n)
                        self._uno_do_cpu(irc, table)
                        return

            if text.lower()=='done':
                if self.game[table]['players'][nick].get('hasdrawn')!=True:
                    self.reply(irc, "Ne mozes da zavrsis krug bez da odigras kartu ili povuces sa spila.", to=nick, private=True)
                    return
                ncards=len(self.game[table]['players'][nick]['hand'])
                irc.reply('%s povlaci kartu (%s karti u rukama).' % (nick, ncards), to=self.game[table]['channel'])

                turn=self.game[table]['turn']+1*self.game[table]['direction']
                if turn>nplayers-1:turn=0
                if turn<0:turn=nplayers-1
                self.game[table]['turn']=turn

                for nn in self.game[table]['players'].keys():
                    self._uno_tell_status(irc, nn)
                self._uno_do_cpu(irc, table)
                return
            
            card=text
            
            card=[card for card in self.unodeck if card.lower()==text.lower()]
            validwild=['Wild Blue','Wild Green', 'Wild Red', 'Wild Yellow',
                       'Wild Draw 4 Blue','Wild Draw 4 Green', 'Wild Draw 4 Red', 'Wild Draw 4 Yellow']
            if len(card)==0:
                card=[c for c in validwild if c.lower()==text.lower()]
                if len(card)!=0:
                    card=card[0].rsplit(' ',1)
                    self.game[table]['wildcolor']=card[1]
                    card=[card[0]]
            else:
                if card[0]=='Wild' or card[0]=='Wild Draw 4':
                    irc.reply('Moras da preciziras boju kada igras Wild kartu.')
                    return

            if len(card)==0:
                irc.reply('To nije ispravna karta.')
                return
            else:
                card=card[0]

            hand=self.game[table]['players'][nick]['hand']
            if card not in hand:
                irc.reply('Nemas tu kartu u ruci.')
                return
            
            # check for illegal move
            if self._uno_is_valid_play(table, card, discard)==False:
                irc.reply("Ne mozes da odigras tu kartu.")
                return
            
            # play the card
            self.game[table]['players'][nick]['hand'].remove(card)
            self.game[table]['discard'].append(card)
            ncards=len(self.game[table]['players'][nick]['hand'])
            
            if 'Wild' in card:
                card='%s(%s)' % (card, self.game[table]['wildcolor'])
            if self.game[table]['players'][nick].get('hasdrawn')==True:
                irc.reply("%s povlaci kartu, i igra je; To je %s (%s karata ostalo u ruci)." % (nick, card, ncards), to=channel)
                self.game[table]['players'][nick]['hasdrawn']=False
            else:
                irc.reply('%s je odigrao %s (%s karata ostalo u ruci).' % (nick, card, ncards), to=channel)
            
            ncards = len(self.game[table]['players'][nick]['hand'])
            if ncards==0:
                irc.reply('The game is over.  '+ircutils.bold('%s wins!' % nick), to=channel)
                self.game[table]['phase']='gameover'
                self._cleanup(table)
                return

            if 'Reverse' in card:
                self.game[table]['direction']*=-1
            
            turn=self.game[table]['turn']+1*self.game[table]['direction']
            if turn>nplayers-1:turn=0
            if turn<0:turn=nplayers-1
            self.game[table]['turn']=turn

            if 'Draw Two' in card or 'Draw 4' in card:
                ndrawcards=2
                if 'Draw 4' in card: ndrawcards=4
                drawplayer=self.game[table]['players'].keys()[self.game[table]['turn']]
                for n in range(ndrawcards):
                    c=self.game[table]['deck'].pop(random.randint(0,len(self.game[table]['deck'])-1))
                    self.game[table]['players'][drawplayer]['hand'].append(c)
                ncards=len(self.game[table]['players'][drawplayer]['hand'])
                irc.reply('%s povlaci %s karata (%s karata u ruci).' % (drawplayer, ndrawcards, ncards), to=channel)

            # Skip turn
            if 'Skip' in card or 'Draw Two' in card or 'Draw 4' in card or ('Reverse' in card and nplayers==2):
                turn=self.game[table]['turn']+1*self.game[table]['direction']
                if turn>nplayers-1:turn=0
                if turn<0:turn=nplayers-1
                self.game[table]['turn']=turn

            for n in self.game[table]['players'].keys():
                self._uno_tell_status(irc, n)
            self._uno_do_cpu(irc, table)
        else:
            irc.reply('Error: game not running')
    play = wrap(play, ['text'])

    def setoption(self, irc, msg, args, channel, text, value):
        """<option> <value>
        
        Changes an option for Uno game.  You can view the 
        options for the current channel with the "+uno showoptions" command."""
        try:
            self._read_options(irc)
        except:
            pass
        if value.lower()=='true':
            value=True
        elif value.lower()=='false':
            value=False
        elif value.lower()=='unset':
            if text in self.channeloptions:
                irc.reply('Set %s %s-->(unset)' % (text, self.channeloptions[text]))
                del self.channeloptions[text]
                try:
                    self._write_options(irc)
                except:
                    irc.reply('Failed to write options to file. :(')
            else:
                irc.reply('%s was already unset.' % text)
            return
        if text in self.channeloptions:
            irc.reply('Set %s %s-->%s' % (text, self.channeloptions[text], value))
            self.channeloptions[text]=value
        else:
            irc.reply('Set %s (unset)-->%s' % (text, value))
            self.channeloptions[text]=value
        try:
            self._write_options(irc)
        except:
            irc.reply('Failed to write options to file. :(')
    setoption = wrap(setoption, [('checkChannelCapability', 'op'), 'something', 'something'])

    def showoptions(self, irc, msg, args):
        """(takes no arguments)
        
        Prikazuje trenutne opcije sto se Uno tice za ovaj kanal."""
        try:
            self._read_options(irc)
        except:
            pass
        txt=', '.join(['='.join([str(i) for i in item]) for item in self.channeloptions.items()])
        irc.reply(txt)
    showoptions = wrap(showoptions)

    def _cleanup(self, table):
        self.game[table]={}
        self.game[table]['players']={}
        self.game[table]['phase']=''

    def _getopentable(self):
        openslot=[i for i in range(len(self.game)) if not self.game[i].get('phase')]
        if len(openslot)==0:
            return None
        else:
            return openslot[0]

    def _getcurrenttables(self):
        slot=[i for i in range(len(self.game)) if self.game[i].get('phase')]
        return slot

    def _gettablefromnick(self, n):
        tables=self._getcurrenttables()
        if not tables: return None
        for table in tables:
            if n.lower() in map(lambda x:x.lower(), self.game[table]['players'].keys()):
                return table
        return None

    def _read_options(self, irc):
        network=irc.network.replace(' ','_')
        channel=irc.msg.args[0]
        #irc.reply('test: %s.%s.options' % (irc.network, irc.msg.args[0] ))
        f="%s%s.%s.options" % (self.pluginpath, network, channel)
        if os.path.isfile(f):
            inputfile = open(f, "rb")
            self.channeloptions = pickle.load(inputfile)
            inputfile.close()
        else:
            # Use defaults
            channeloptions = {}
            channeloptions['allow_game']=False
            channeloptions['debug']=False
            channeloptions['use_queue']=True
            channeloptions['nplayers']=10
            channeloptions['maxbots']=9
        return

    def _write_options(self, irc):
        network=irc.network.replace(' ','_')
        channel=irc.msg.args[0]
        outputfile = open("%s%s.%s.options" % (self.pluginpath, network, channel), "wb")
        pickle.dump(self.channeloptions, outputfile)
        outputfile.close()

    def doNick(self, irc, msg):
        oldNick = msg.nick
        newNick = msg.args[0]
        table=self._gettablefromnick(oldNick)
        if table == None:
            return
        self.game[table]['players'][newNick]=self.game[table]['players'][oldNick]
        del self.game[table]['players'][oldNick]

    def doQuit(self, irc, msg):
        nick=msg.nick
        table=self._gettablefromnick(nick)
        if table == None:
            return
        self._leavegame(irc, msg, nick)
        self._uno_do_cpu(irc, table) # only works if game type is uno

    def doPart(self, irc, msg):
        #self.log.info('doPart debug: msg.args[0]=%s, msg.args[1]=%s, msg.command=%s, msg.nick=%s' % (msg.args[0], msg.args[1], msg.command, msg.nick))
        nick=msg.nick
        table=self._gettablefromnick(nick)
        if table == None:
            return
        if msg.args[0] == self.game[table]['channel']:
            self._leavegame(irc, msg, nick)
            self._uno_do_cpu(irc, table) # only works if game type is uno
        
    def doKick(self, irc, msg):
        (channel, nicks) = msg.args[:2]
        nicks=nicks.split(',')
        for nick in nicks:
            table=self._gettablefromnick(nick)
            if table!=None:
                self._leavegame(irc, msg, nick)
                self._uno_do_cpu(irc, table) # only works if game type is uno

    def _sendMsg(self, irc, msg):
        if self.channeloptions['use_queue']:
            irc.queueMsg(msg)
        else:
            irc.sendMsg(msg)
        irc.noReply()

    def reply(self, irc, text, action=False, private=False, prefixNick=False, to='', fast=False):
        table=self._gettablefromnick(to)
        if table == None:
            # hopefully it's a valid channel
            pass
        else:
            if self.game[table]['players'][to].get('fake'):
                if self.channeloptions['debug']:
                    text='(to %s): %s' % (to, text)
                    text=ircutils.mircColor(text, fg=14)
                    to=self.game[table]['channel']
                else:
                    # No need to show cpu actions anywhere if debug is false.
                    return

        if action==True or fast==False:
            irc.reply(text, action=action, private=private, prefixNick=prefixNick, to=to)
        else:
            if (prefixNick) and ('#' not in to):
                text='%s: %s' % (to, text)
            m=ircmsgs.privmsg(to, text)
            self._sendMsg(irc, m)


_Plugin.__name__=PluginName
Class = _Plugin

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
