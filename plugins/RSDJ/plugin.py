###
# Copyright (c) 2013, KG-Bot
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import json
import string
import supybot.conf as conf
import locale
import supybot.ircmsgs as ircmsgs
import datetime
import os

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('RSDJ')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

allowed_channels = ['#BorgiaFamily', '#Gromovnici']

class RSDJ(callbacks.Plugin):
    """Add the help for "@plugin help RSDJ" here
    This should describe *how* to use this plugin."""
    threaded = True

    def read_vojnici_database(self, msg):
        channel = msg.args[0]
        try:
            with open('RSDJ/%s/Vojnici.json' % channel, 'r') as vojnici:
                soldiers = json.loads(vojnici.read())
                return soldiers
        except:
            return 0

    def write_vojnici_database(self, channel, database):
        try:
            with open('RSDJ/%s/Vojnici.json' % channel, 'w') as vojnici:
                vojnici.write(json.dumps(database))
                return "Done"
        except:
            return 0

    def read_gazde_database(self, msg):
        channel = msg.args[0]
        try:
            with open('RSDJ/%s/Gazde.json' % channel, 'r') as gazde:
                admins = json.loads(gazde.read())
                return admins
        except:
            return 0

    def read_udar_tok_database(self, msg):
        channel = msg.args[0]
        try:
            with open('RSDJ/%s/Udar_tok.json' % channel, 'r') as tok_udara:
                tok = json.loads(tok_udara.read())
                return tok
        except:
            return 0

    def write_udar_tok_database(self, channel, database):
        try:
            with open('RSDJ/%s/Udar_tok.json' % channel, 'w') as tok_udara:
                tok_udara.write(json.dumps(database))
                return "Done"
        except:
            return 0

    def read_udar_vojnici_database(self, msg):
        channel = msg.args[0]
        try:
            with open('RSDJ/%s/Udar_vojnici.json' % channel, 'r') as vojnici_udar:
                vojnici = json.loads(vojnici_udar.read())
                return vojnici
        except:
            return 0

    def write_udar_vojnici_database(self, channel, database):
        try:
            with open('RSDJ/%s/Udar_vojnici.json' % channel, 'w') as tok_udara:
                tok_udara.write(json.dumps(database))
                return "Done"
        except:
            return 0

    def read_arhiva_database(self, channel, fajl):
        try:
            with open('RSDJ/Arhiva/%s/%s.json' % (channel, fajl), 'r') as arhiva_udar:
                arhiva = json.loads(arhiva_udar.read())
                return arhiva
        except:
            return 0

    def write_arhiva_database(self, channel, today, database):
        try:
            with open('RSDJ/Arhiva/%s/%s.json' % (channel, today), 'w') as arhiviranje:
                arhiviranje.write(json.dumps(database))
                return "Done"
        except:
            return 0
                

    def upisi(self, irc, msg, args, vojn, id):
        """<vojnik> <id vojnika>

        Upisuje vojnika u bazu."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                vojnik = string.lower(vojn)
                nick_za_upis = {}
                nick_za_upis['id'] = id
                nick_za_upis['nick'] = string.lower(vojnik)
                vojnici = self.read_vojnici_database(msg)
                if vojnik in vojnici.keys():
                    irc.reply("Vojnik \x02%s\x02 se vec nalazi u bazi." % vojnik)
                else:
                    vojnici[vojnik] = nick_za_upis
                    upis = self.write_vojnici_database(channel, vojnici)
                    if upis == "Done":
                        irc.reply('Vojnik \x02%s\x02 je upisan u bazu, u bazi se trenutno nalazi \x02%s\x02 vojnika.' % (vojnik, len(vojnici.items())))
                    else:
                        irc.reply("Nesto je poslo po zlu, baza je ostala ista. Sintaksa komande je \x02+upisi NICK-VOJNIKA ID-VOJNIKA\x02.")
    upisi = wrap(upisi, ['something', 'int'])

    def obrisi(self, irc, msg, args, vojn):
        """<vojnik>
        
        Brise vojnika iz baze."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                vojnik = string.lower(vojn)
                vojnici = self.read_vojnici_database(msg)
                if vojnik in vojnici.keys():
                    del vojnici[vojnik]
                    upis = self.write_vojnici_database(channel, vojnici)
                    if upis == "Done":
                        irc.reply("Vojnik \x02%s\x02 je obrisan iz baze, u bazi se trenutno nalazi \x02%s\x02 vojnika." % (vojnik, len(vojnici)))
                    else:
                        irc.reply("Nesto je poslo po zlu, baza je ostala ista. Sintaksa komande je \x02+obrisi NICK-VOJNIKA\x02.")
                else:
                    irc.reply("Vojnik \x02%s\x02 se ne nalazi u bazi, sto znaci da ne moze biti ni obrisan." % vojnik)
    obrisi = wrap(obrisi, ['something'])

    def vojnici(self, irc, msg, args, vojn):
        """[<vojnik>]
    
        Pregled baze vojnika, ako se u komandi nalazi i [<vojnik>] radi se pregled baze samo za tog vojnika, inace se radi pregled citave baze."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                if vojn is None:
                    vojnici = self.read_vojnici_database(msg)
                    #with open('RSDJ/Vojnici.json', 'r') as vojnici:
                       # b = json.loads(vojnici.read())
                    if len(vojnici.keys()) != 0:
                        join_vojnici = ', '.join(vojnici.keys())
                        irc.reply("U bazi se nalazi \x02%s\x02 vojnika, i oni su: \x02%s\x02." % (len(vojnici.keys()), join_vojnici))
                    else:
                        irc.reply("U bazi nema vojnika.")
                else:
                    vojnik = string.lower(vojn)
                    #with open('RSDJ/Vojnici.json', 'r') as vojnici:
                        #b = json.loads(vojnici.read())
                    vojnici = self.read_vojnici_database(msg)
                    if vojnik in vojnici.keys():
                        vojnik_id = vojnici[vojnik]['id']
                        irc.reply("Vojnik \x02%s\x02 se nalazi u bazi, njegov ID je: \x02%s\x02, ukupno vojnika u bazi: \x02%s\x02." % (vojnik, vojnik_id, len(vojnici.keys())))
                    else:
                        irc.reply("Vojnik \x02%s\x02 se ne nalazi u bazi, ukupno vojnika u bazi: \x02%s\x02." % (vojnik, len(vojnici.keys())))
            #else:
                #irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost pregleda baze." % nick)
    vojnici = wrap(vojnici, [optional('something')])

    def pokreni(self, irc, msg, args):
        """Takes no arguments

        Pokrece udar."""
        nick = msg.nick
        chan = msg.args[0]
        if chan not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
        #with open('RSDJ/Gazde.json', 'r') as gazde:
            #admins = json.loads(gazde.read())
            #if nick in admins:
                sati = datetime.datetime.now().hour
                minuta = datetime.datetime.now().minute
                sekundi = datetime.datetime.now().second
                mikros = datetime.datetime.now().microsecond
                pocetak = '%s:%s:%s:%s' % (sati, minuta, sekundi, mikros)
                udar = {}
                udar['Udar'] = 1
                udar['Vodja'] = nick
                udar['Pocetak'] = pocetak
                pokreni_udar = self.write_udar_tok_database(chan, udar)
                #with open('RSDJ/Udar_tok.json', 'w') as tok_udara:
                    #tok_udara.write(json.dumps(udar))
                if pokreni_udar == "Done":
                    nicks = ', '.join(irc.state.channels[chan].users)
                    irc.reply(nicks)
                    irc.reply("\x02Upravo je poceo udar, svi koji ucestvuju molimo da promenite vas nick i da se upisete na bota pomocu komande \x0310+dodaj Broj-vaseg-wella\x03\x02.")
                else:
                    irc.reply("Nesto je poslo po zlu, baza je ostala ista. Sintaksa komande je \x02+pokreni\x02.")
            #else:
                #irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost pokretanja udara." % nick)
    pokreni = wrap(pokreni)

    def dodaj(self, irc, msg, args, well):
        """Takes no arguments

        Upisuje vas nick u bazu vojnika za trenutni udar."""
        nick = string.lower(msg.nick)
        url = conf.supybot.plugins.ERep.url()
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
        #with open('RSDJ/Udar_tok.json', 'r') as tok_udara:
            #b = json.loads(tok_udara.read())
            tok_udara = self.read_udar_tok_database(msg)
            udar_traje = tok_udara['Udar']
            vodja_udara = tok_udara['Vodja']
            if udar_traje == 1:
            #with open('RSDJ/Vojnici.json', 'r') as vojnici:
                #b = json.loads(vojnici.read())
                vojnici = self.read_vojnici_database(msg)
                if nick in vojnici.keys():
                    id = vojnici[nick]['id']
                    data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                    rank_points = data['military']['rank']['points']
                    base = data['military']['base_hit']
                    true_patriot_damage = data['true_patriot']['damage'] if data['true_patriot'] else 0
                    q1 = base * 1.2000373204
                    q2 = q1 * 1.1666925828
                    q3 = q2 * 1.14287618286
                    q4 = q3 * 1.12501457726
                    q5 = q4 * 1.1111226288
                    q6 = q5 * 1.10000932923
                    q7 = q6 * 1.36358239335
                    nick_za_upis = {}
                    nick_za_upis['rpts'] = rank_points
                    nick_za_upis['q7'] = q7
                    nick_za_upis['id'] = id
                    nick_za_upis['tp'] = true_patriot_damage
                    #with open('RSDJ/Udar_vojnici.json', 'r') as vojnici_udar:
                        #b = json.loads(vojnici_udar.read())
                    udar_vojnici = self.read_udar_vojnici_database(msg)
                    if nick in udar_vojnici.keys():
                        irc.reply("Vec se nalazite u bazi za ovaj udar, nije moguce duplo upisivanje.")
                    else:
                        udar_vojnici[nick] = nick_za_upis
                            #with open('RSDJ/Udar_vojnici.json', 'w') as vojnici_udar_upis:
                                #vojnici_udar_upis.write(json.dumps(b))
                        udar_vojnici_upis = self.write_udar_vojnici_database(channel, udar_vojnici)
                        if udar_vojnici_upis == "Done":
                            irc.reply("Uspesno ste se upisali u bazu vojnika za ovaj udar.")
                            irc.queueMsg(ircmsgs.privmsg(vodja_udara, "\x02%s\x02 se prijavio za podelu, on ima \x02%s\x02 well -a, i njegov donate link je: \x02http://www.erepublik.com/en/economy/donate-items/%s\x02" % (nick, well, id)))
                            irc.queueMsg(ircmsgs.privmsg('#grom_komanda', "\x02%s\x02 se prijavio za podelu, on ima \x02%s\x02 well -a, i njegov donate link je: \x02http://www.erepublik.com/en/economy/donate-items/%s\x02" % (nick, well, id)))
                        else:
                            irc.reply("Nesto je poslo po zlu, baza je ostala ista. Sintaksa komande je \x02+dodaj BROJ-WELLa\x02.")
                else:
                    irc.reply("Vi niste jedan od vojnika RSDj -a, ili mozda jeste ali se ne nalazite u bazi vojnika. Ako mislite da je u pitanju greska javite nekome iz komande.")
            else:
                irc.reply("Udar nije u toku, ne mozete da se upisete sada.")
    dodaj = wrap(dodaj, ['int'])

    def proveri(self, irc, msg, args, vojn):
        """[<vojni>]

        Provera vojnika u toku udara. Ako ne upisete ime vojnika radi proveru za sve vojnike prijavljene za udar."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                url = conf.supybot.plugins.ERep.url()
        #with open('RSDJ/Gazde.json', 'r') as gazde:
            #admins = json.loads(gazde.read())
            #if nick in admins:
                tok_udara = self.read_udar_tok_database(msg)
                udar_traje = tok_udara['Udar']
                vodja_udara = tok_udara['Vodja']
                if udar_traje == 1:
               #with open('RSDJ/Udar_tok.json', 'r') as tok_udara:
                    #b = json.loads(tok_udara.read())
                    #udar_traje = b['Udar']
                #if udar_traje == 1:
                    udar_vojnici = self.read_udar_vojnici_database(msg)
                    #with open('RSDJ/Udar_vojnici.json', 'r') as vojnici_udar:
                        #b = json.loads(vojnici_udar.read())
                    if vojn is not None:
                        vojnik = string.lower(vojn)
                        if vojnik in udar_vojnici.keys():
                            stari_rpts = udar_vojnici[vojnik]['rpts']
                            stari_q7 = udar_vojnici[vojnik]['q7']
                            stari_tp = udar_vojnici[vojnik]['tp']
                            id = udar_vojnici[vojnik]['id']
                            data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                            rank_points = data['military']['rank']['points']
                            base = data['military']['base_hit']
                            true_patriot_damage = data['true_patriot']['damage'] if data['true_patriot'] else 0
                            q1 = base * 1.2000373204
                            q2 = q1 * 1.1666925828
                            q3 = q2 * 1.14287618286
                            q4 = q3 * 1.12501457726
                            q5 = q4 * 1.1111226288
                            q6 = q5 * 1.10000932923
                            q7 = q6 * 1.36358239335
                            strength = data['military']['strength']
                            razlika_rpts = rank_points - stari_rpts
                            razlika_q7 = q7 - stari_q7
                            razlika_tp = true_patriot_damage - stari_tp
                            broj_tenkova = razlika_rpts / q7
                            broj_tenkova_format = '%.2f' % broj_tenkova
                            utrosen_dmg = razlika_rpts * 10
                            irc.reply("Vojnik \x02%s\x02 (\x02%s\x02) je ispucao \x02%s\x02 tenkova i napravio \x02%s\x02 (patriot \x02%s\x02) stete." % (vojnik, locale.format('%d', int(strength), True), broj_tenkova_format, locale.format('%d', int(utrosen_dmg), True), locale.format('%d', int(razlika_tp), True)))
                        else:
                            irc.reply("\x02%s\x02 nije jedan od vojnika ove Vojne Jedinice." % vojnik)
                    else:
                        zbirna_snaga = []
                        zbir_tenkova = []
                        zbir_stete = []
                        zbir_tp_stete = []
                        for ratnik in udar_vojnici:
                            stari_rpts = udar_vojnici[ratnik]['rpts']
                            stari_q7 = udar_vojnici[ratnik]['q7']
                            stari_tp = udar_vojnici[ratnik]['tp']
                            id = udar_vojnici[ratnik]['id']
                            data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                            rank_points = data['military']['rank']['points']
                            base = data['military']['base_hit']
                            true_patriot_damage = data['true_patriot']['damage'] if data['true_patriot'] else 0
                            q1 = base * 1.2000373204
                            q2 = q1 * 1.1666925828
                            q3 = q2 * 1.14287618286
                            q4 = q3 * 1.12501457726
                            q5 = q4 * 1.1111226288
                            q6 = q5 * 1.10000932923
                            q7 = q6 * 1.36358239335
                            strength = data['military']['strength']
                            razlika_rpts = rank_points - stari_rpts
                            razlika_q7 = q7 - stari_q7
                            razlika_tp = true_patriot_damage - stari_tp
                            broj_tenkova = razlika_rpts / q7
                            broj_tenkova_format = '%.2f' % broj_tenkova
                            utrosen_dmg = razlika_rpts * 10
                            zbirna_snaga.append(strength)
                            zbir_tenkova.append(broj_tenkova)
                            zbir_stete.append(utrosen_dmg)
                            zbir_tp_stete.append(razlika_tp)
                            irc.reply("Vojnik \x02%s\x02 (\x02%s\x02) je ispucao \x02%s\x02 tenkova i napravio \x02%s\x02 (patriot \x02%s\x02) stete." % (ratnik, locale.format('%d', int(strength), True), broj_tenkova_format, locale.format('%d', int(utrosen_dmg), True), locale.format('%d', int(razlika_tp), True)))
                        broj_vojnika = len(udar_vojnici.keys())
                        suma_snage = sum(zbirna_snaga) / broj_vojnika
                        duzina_tenkova = sum(zbir_tenkova)
                        duzina_tenkova_format = '%.2f' % duzina_tenkova
                        suma_stete = sum(zbir_stete)
                        tp_suma = sum(zbir_tp_stete)
                        irc.reply("Na udaru prisutno \x02%s\x02 vojnika, prosecna snaga \x02%s\x02, utroseno tenkova \x02%s\x02, ukupna steta \x02%s\x02 (patriot \x02%s\x02)." % (broj_vojnika, locale.format('%d', int(suma_snage), True), duzina_tenkova_format, locale.format('%d', int(suma_stete), True), locale.format('%d', int(tp_suma), True)))
                else:
                    irc.reply("Udar nije u toku i provera vojnika nije moguca.")
            #else:
                #irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost provere toka udara." % nick)
    proveri = wrap(proveri, [optional('something')])

    def zavrsi(self, irc, msg, args):
        """Takes no arguments

        Zavrsava udar, cisti baze, sacuvava statistike udara u arhivu."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                url = conf.supybot.plugins.ERep.url()
                udar_tok_0 = {}
                udar_tok_0['Udar'] = 0
        #with open('RSDJ/Gazde.json', 'r') as gazde:
            #admins = json.loads(gazde.read())
            #if nick in admins:
                #with open('RSDJ/Udar_tok.json', 'r') as udar_tok:
                    #udar_citanje = json.loads(udar_tok.read())
                tok_udara = self.read_udar_tok_database(msg)
                if 'Vodja' not in tok_udara.keys():
                    irc.reply("Udar nije u toku, prema tome zavrsavanje istoga nije moguce.")
                else:
                    #udar_traje = tok_udara['Udar']
                    vodja_udara = tok_udara['Vodja']
                    #vodja_udara = udar_citanje['Vodja']
                    pocetak_udara = tok_udara['Pocetak']
                #with open('RSDJ/Udar_tok.json', 'w') as tok_udara:
                    #tok_udara.write(json.dumps(udar_tok_0))
                    zavrsi_udar = self.write_udar_tok_database(channel, udar_tok_0)
                    udar_vojnici = self.read_udar_vojnici_database(msg)
                    #with open('RSDJ/Udar_vojnici.json', 'r') as vojnici_udar:
                        #b = json.loads(vojnici_udar.read())
                    zbirna_snaga = []
                    zbir_tenkova = []
                    zbir_stete = []
                    zbir_tp_stete = []
                    for ratnik in udar_vojnici.keys():
                        stari_rpts = udar_vojnici[ratnik]['rpts']
                        stari_q7 = udar_vojnici[ratnik]['q7']
                        stari_tp = udar_vojnici[ratnik]['tp']
                        id = udar_vojnici[ratnik]['id']
                        data = json.load(utils.web.getUrlFd('%scitizen/profile/%s.json' % (url, id)))
                        rank_points = data['military']['rank']['points']
                        base = data['military']['base_hit']
                        true_patriot_damage = data['true_patriot']['damage'] if data['true_patriot'] else 0
                        q1 = base * 1.2000373204
                        q2 = q1 * 1.1666925828
                        q3 = q2 * 1.14287618286
                        q4 = q3 * 1.12501457726
                        q5 = q4 * 1.1111226288
                        q6 = q5 * 1.10000932923
                        q7 = q6 * 1.36358239335
                        strength = data['military']['strength']
                        razlika_rpts = rank_points - stari_rpts
                        razlika_q7 = q7 - stari_q7
                        razlika_tp = true_patriot_damage - stari_tp
                        broj_tenkova = razlika_rpts / q7
                        broj_tenkova_format = '%.2f' % broj_tenkova
                        utrosen_dmg = razlika_rpts * 10
                        zbirna_snaga.append(strength)
                        zbir_tenkova.append(broj_tenkova)
                        zbir_stete.append(utrosen_dmg)
                        zbir_tp_stete.append(razlika_tp)
                    broj_vojnika = len(udar_vojnici.keys())
                    suma_snage = sum(zbirna_snaga) / broj_vojnika
                    duzina_tenkova = sum(zbir_tenkova)
                    duzina_tenkova_format = '%.2f' % duzina_tenkova
                    suma_stete = sum(zbir_stete)
                    tp_suma = sum(zbir_tp_stete)
                    kraj_sati = datetime.datetime.now().hour
                    kraj_minuta = datetime.datetime.now().minute
                    kraj_sekundi = datetime.datetime.now().second
                    kraj_mikros = datetime.datetime.now().microsecond
                    kraj_udara = '%s:%s:%s:%s' % (kraj_sati, kraj_minuta, kraj_sekundi, kraj_mikros)
                    today_date = datetime.date.today().strftime('%d_%m_%Y') # datetime.date.today().strftime('%d')
                    today_hour = datetime.datetime.now().hour
                    today = '%s_%s' % (today_date, today_hour)
                    statistika = {}
                    statistika['Broj Vojnika'] = broj_vojnika
                    statistika['Suma snage'] = suma_snage
                    statistika['Broj tenkova'] = duzina_tenkova_format
                    statistika['Suma stete'] = suma_stete
                    statistika['TP suma'] = tp_suma
                    statistika['Pocetak udara'] = pocetak_udara
                    statistika['Vodja udara'] = vodja_udara
                    statistika['Kraj udara'] = kraj_udara
                    statistika['Vojnici'] = udar_vojnici
                    write_arhiva = self.write_arhiva_database(channel, today, statistika)
                    #with open('RSDJ/Arhiva/%s.json' % today, 'w') as arhiviranje:
                        #arhiviranje.write(json.dumps(statistika))
                    chan = msg.args[0]
                    nicks = ', '.join(irc.state.channels[chan].users)
                    irc.reply(nicks)
                    irc.reply("Udar zavrsen, Vojna Jedinica napravila stete \x02%s\x02 i potrosila \x02%s\x02 tenkova." % (locale.format('%d', int(suma_stete), True), duzina_tenkova_format))
                    empty_dict = {}
                    self.write_udar_vojnici_database(channel, empty_dict)
                    #with open('RSDJ/Udar_vojnici.json', 'w') as vojnici:
                        #vojnici.write('{}')
            #else:
               # irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost provere toka udara." % nick)
    zavrsi = wrap(zavrsi)

    def arhiva(self, irc, msg, args, dan, mesec, godina, sat):
        """<dan> <mesec> <godina> <sat>

        Prikazuje statistiku sa udara za odabrani datum."""
        nick = msg.nick
        channel = msg.args[0]
        if channel not in allowed_channels:
            irc.reply("Ova komanda nije moguca na ovom kanalu, molimo pokusajte da je kucate na kanalu vase Vojne Jedinice.")
        else:
            admins = self.read_gazde_database(msg)
            if nick not in admins:
                irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost upisivanja vojnika u bazu." % nick)
            else:
                fajl = '%s_%s_%s_%s' % (dan, mesec, godina, sat)
        #with open('RSDJ/Gazde.json', 'r') as gazde:
            #admins = json.loads(gazde.read())
            #if nick in admins:
                try:
                    #with open('RSDJ/Arhiva/%s.json' % fajl, 'r') as arhiva_udar:
                        #stari_udar = json.loads(arhiva_udar.read())
                    stari_udar = self.read_arhiva_database(channel, fajl)
                    vodja_udara = stari_udar['Vodja udara']
                    pocetak_udara = stari_udar['Pocetak udara']
                    kraj_udara = stari_udar['Kraj udara']
                    broj_vojnika = stari_udar['Broj Vojnika']
                    suma_snage = stari_udar['Suma snage']
                    broj_tenkova = stari_udar['Broj tenkova']
                    tp_suma = stari_udar['TP suma']
                    suma_stete = stari_udar['Suma stete']
                    vojnici = ', '.join(stari_udar['Vojnici'].keys())
                    irc.reply("Udar poceo u \x02%s\x02, udar je vodio \x02%s\x02, prisustvovalo \x02%s\x02 vojnika koji su potrosili \x02%s\x02 tenkova i napravili \x02%s\x02 (patriot \x02%s\x02) stete. Prosecna snaga na udaru je bila \x02%s\x02, udar zavrsio u \x02%s\x02." % (pocetak_udara, vodja_udara, broj_vojnika, broj_tenkova, locale.format('%d', int(suma_stete), True), locale.format('%d', int(tp_suma), True), locale.format('%d', int(suma_snage), True), kraj_udara))
                    irc.reply("Vojnici koji su prisustvovali udaru su: \x02%s\x02." % vojnici)
                except:
                    udari = []
                    lista_udara = os.listdir('RSDJ/Arhiva/%s/' % channel)
                    for udar in lista_udara:
                        prvi_split = str.split(udar, '.')
                        udari.append(prvi_split[0])
                    irc.reply("U arhivi ne postoji statistika za ovaj udar. Trenutno se u arhivi nalaze sledeci udari: \x02%s\x02." % ', '.join(udari))
            #else:
                #irc.reply("\x02%s\x02 se ne nalazi u bazi administratora i nema mogucnost provere toka udara." % nick)
    arhiva = wrap(arhiva, ['something', 'something', 'something', 'something'])
                
Class = RSDJ


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
