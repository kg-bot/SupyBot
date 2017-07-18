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
import string
import random
import json
import supybot.schedule as schedule
import time
import supybot.ircmsgs as ircmsgs

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Kviz')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x
allowed_channels = []

class Kviz(callbacks.Plugin):
    """Add the help for "@plugin help Kviz" here
    This should describe *how* to use this plugin."""
    threaded = True

    def doPrivmsg(self, irc, msg):
        check_kviz = self.check_online(msg)
        channel = msg.args[0]
        user_answer = msg.args[1].lower()
        nick = msg.nick
        if channel in allowed_channels:
            if check_kviz == 1:
                valid_answer = 'Kviz/%s/Valid_answers.json' % channel
                with open(valid_answer, 'r') as validating:
                    correct_answer = json.loads(validating.read())
                    answer = correct_answer['valid']
                    if user_answer == answer.lower():
                        try:
                            schedule.removeEvent('%s-clue' % channel)
                            questions = 'Kviz/%s/Questions.json' % channel
                            irc.reply("Congrats \x02%s\x02, you got the correct answer on this questions and you got 2 points to your score on this channel." % nick)
                            self.write_score(irc, msg, nick, channel, questions, valid_answer)
                            irc.reply("Next question in 10 seconds.")
                        except:
                            schedule.removeEvent('%s-next-question' % channel)
                            questions = 'Kviz/%s/Questions.json' % channel
                            irc.reply("Congrats \x02%s\x02, you got the correct answer on this questions and you got 2 points to your score on this channel." % nick)
                            self.write_score(irc, msg, nick, channel, questions, valid_answer)
                            irc.reply("Next question in 10 seconds.")

    def write_score(self, irc, msg, name, channel, questions, valid):
        scores = 'Kviz/%s/Scores.json' % channel
        with open(scores, 'r') as read_scores:
            scores_file = json.loads(read_scores.read())
            old_score = scores_file[name]
            new_score = old_score + 5
            scores_file[name] = new_score
            with open(scores, 'w') as write_score:
                write_score.write(json.dumps(scores_file))
                schedule.addEvent(self._ask, time.time() + 10, args=(irc, msg, questions, channel, valid))

    def _ask(self, irc, msg, questions, channel, valid):
        with open(questions, 'r') as read_questions:
            questions_dict = json.loads(read_questions.read())
            questions_keys = questions_dict.keys()
            place = random.choice(questions_keys)
            extract_question = questions_dict[place]['question']
            extract_clue = questions_dict[place]['clue']
            correct_answer = questions_dict[place]['correct']
            valid_answer = {}
            valid_answer['valid'] = correct_answer
            with open(valid, 'w') as writing_valid_answer:
                writing_valid_answer.write(json.dumps(valid_answer))
            irc.reply('\x02%s\x02' % extract_question)
            schedule.addEvent(self.give_clue, time.time() + 5, '%s-clue' % channel, args=(irc, msg, channel, questions, extract_clue))

    def check_online(self, msg):
        channel = msg.args[0]
        filename = 'Kviz/%s/Kviz_Status.json' % channel
        if channel in allowed_channels:
            with open(filename, 'r') as kviz_status:
                running = json.loads(kviz_status.read())
                online = running['Online']
                return online

    def give_clue(self, irc, msg, channel, questions, clue):
        valid_answer = 'Kviz/%s/Valid_answers.json' % channel
        irc.queueMsg(ircmsgs.privmsg(channel, clue))
        schedule.addEvent(self._ask, time.time() + 10, '%s-next-question' % channel, args=(irc, msg, questions, channel, valid_answer))
            

    def start(self, irc, msg, args):
        """Takes no arguments

        Starts new round of quiz."""
        check_kviz = self.check_online(msg)
        channel = msg.args[0]
        questions = 'Kviz/%s/Questions.json' % channel
        valid_answer = 'Kviz/%s/Valid_answers.json' % channel
        nick = msg.nick
        users = irc.state.channels[channel].users
        if nick == "DonVitoCorleone":
            if check_kviz == 1:
                irc.reply("Quiz is already running on this channel, you can't start a new instance of it until this one is stopped.")
            else:
                irc.reply(', '.join(users))
                irc.reply("Starting a new instance of Quiz, get ready!!!")
                self._ask(irc, msg, questions, channel, valid_answer)
                filename = 'Kviz/%s/Kviz_Status.json' % channel
                stop_kviz = {}
                stop_kviz['Online'] = 1
                with open(filename, 'w') as kviz_status:
                    kviz_status.write(json.dumps(stop_kviz))
        else:
            irc.reply("You can't start Quiz because you're not in my admins list.")
    start = wrap(start)

    def stop(self, irc, msg, args):
        """Takes no arguments

        Stops quiz."""
        channel = msg.args[0]
        try:
            event = '%s-clue' % channel
            schedule.removeEvent(event)
            filename = 'Kviz/%s/Kviz_Status.json' % channel
            stop_kviz = {}
            stop_kviz['Online'] = 0
            with open(filename, 'w') as kviz_status:
                kviz_status.write(json.dumps(stop_kviz))
                irc.reply("Quiz has just been stopped, to start it again type +kviz Start.")
        except:
            event = '%s-next-question' % channel
            schedule.removeEvent(event)
            filename = 'Kviz/%s/Kviz_Status.json' % channel
            stop_kviz = {}
            stop_kviz['Online'] = 0
            with open(filename, 'w') as kviz_status:
                kviz_status.write(json.dumps(stop_kviz))
                irc.reply("Quiz has just been stopped, to start it again type +kviz start.")
    stop = wrap(stop)

    def addq(self, irc, msg, args, channel, question, clue, answer):
        """<channel> <question> <clue> <answer>

        Adds question entry for the given channel"""
        msg_place = msg.args[0]
        my_nick = irc.nick
        nick = msg.nick
        questions = 'Kviz/%s/Questions.json' % channel
        if msg_place == my_nick:
            if channel.startswith('#'):
                try:
                    with open(questions, 'r') as read_questions:
                        loaded_questions = json.loads(read_questions.read())
                        questions_length = len(loaded_questions.keys())
                        question_number = questions_length + 1
                        new_question_dict = {}
                        new_question_dict['question'] = str(question)
                        new_question_dict['clue'] = str(clue)
                        new_question_dict['correct'] = str(answer)
                        loaded_questions[question_number] = new_question_dict
                        with open(questions, 'w') as write_questions:
                            write_questions.write(json.dumps(loaded_questions))
                            irc.reply("Question number \x02%s\x02 successfully added." % question_number)
                except:
                    irc.reply("There is no database for this channel yet, if you would love to add it please ask my owner to do that.")
            else:
                irc.reply("You can't add questions on my PM, only on the channel for which you want to add questions.")
        else:
            irc.reply("You can't do this command anywhere else except on PVT with me.")
    addq = wrap(addq, ['something', 'something', 'something', 'something'])

    def viewq(self, irc, msg, args, channel, number):
        """<channel> [<question number>]

        If [<question number>] is specified it will try to return info about that question, else it will return info about every question in channel database."""
        msg_place = msg.args[0]
        my_nick = irc.nick
        if msg_place == my_nick:
            if channel.startswith('#'):
                try:
                    ops = irc.state.channels[channel].ops
                    nick = msg.nick
                    if nick in ops:
                        try:
                            questions = 'Kviz/%s/Questions.json' % channel
                            with open(questions, 'r') as read_questions:
                                loaded_questions = json.loads(read_questions.read())
                                if number is None:
                                    irc.reply("There are \x02%s\x02 questions for this channel, I'm going to return all of them now." % len(loaded_questions.keys()))
                                    for Question in loaded_questions:
                                        question = loaded_questions[Question]['question']
                                        clue = loaded_questions[Question]['clue']
                                        answer = loaded_questions[Question]['correct']
                                        irc.reply('\x02%s.)\x02 Question: \x02%s\x02, Clue: \x02%s\x02, Answer: \x02%s\x02.' % (Question, question, clue, answer))
                                else:
                                    try:
                                        formated_question = str(number)
                                        question = loaded_questions[formated_question]['question']
                                        clue = loaded_questions[formated_question]['clue']
                                        answer = loaded_questions[formated_question]['correct']
                                        irc.reply("Question: \x02%s\x02, Clue: \x02%s\x02, Answer: \x02%s\x02." % (question, clue, answer))
                                    except:
                                        irc.reply("There is no question number \x02%s\x02 in channel database." % number)
                        except:
                            irc.reply("There is no database for this channel, if this is your channel and you want to add questions please contact my owner.")
                except:
                    irc.reply("I'm not on that channel, it means that Quiz is not even available on that channel.")
            else:
                irc.reply("Channel name that you gave me isn't valid channel name.")
        else:
            irc.reply("You can't do this command anywhere else except on PVT with me.")
    viewq = wrap(viewq, ['something', optional('int')])

    def fixq(self, irc, msg, args, channel, number, part, new):
        """<channel> <question number> <part for fixing> <new part>

        Changes part of the question that you want for the given channel."""
        msg_place = msg.args[0]
        my_nick = irc.nick
        if msg_place == my_nick:
            if channel.startswith('#'):
                try:
                    ops = irc.state.channels[channel].ops
                    nick = msg.nick
                    if nick in ops:
                        try:
                            questions = 'Kviz/%s/Questions.json' % channel
                            with open(questions, 'r') as read_questions:
                                loaded_questions = json.loads(read_questions.read())
                                formated_question = str(number)
                                if part == "question":
                                    if formated_question not in loaded_questions:
                                        irc.reply("There is no question number \x02%s\x02 in this channel database, there are \x02%s\x02 questions in database." % (number, len(loaded_questions.keys())))
                                    else:
                                        loaded_questions[formated_question]['question'] = ' '.join(new)
                                        with open(questions, 'w') as write_questions:
                                            write_questions.write(json.dumps(loaded_questions))
                                            irc.reply("Successfully changed \x02question\x02 part of question number \x02%s\x02." % number)
                                elif part == "clue":
                                    if formated_question not in loaded_questions:
                                        irc.reply("There is no question number \x02%s\x02 in this channel database, there are \x02%s\x02 questions in database." % (number, len(loaded_questions.keys())))
                                    else:
                                        loaded_questions[formated_question]['clue'] = ' '.join(new)
                                        with open(questions, 'w') as write_questions:
                                            write_questions.write(json.dumps(loaded_questions))
                                            irc.reply("Successfully changed \x02clue\x02 part of question number \x02%s\x02." % number)
                                elif part == "correct":
                                    if formated_question not in loaded_questions:
                                        irc.reply("There is no question number \x02%s\x02 in this channel database, there are \x02%s\x02 questions in database." % (number, len(loaded_questions.keys())))
                                    else:
                                        loaded_questions[formated_question]['correct'] = ' '.join(new)
                                        with open(questions, 'w') as write_questions:
                                            write_questions.write(json.dumps(loaded_questions))
                                            irc.reply("Successfully changed \x02correct\x02 part of question number \x02%s\x02." % number)
                                else:
                                    irc.reply("There is no such part in question as \x02%s\x02, possible parts are: \x02question, clue or correct\x02." % part)
                        except:
                            irc.reply("There is no database for this channel, if this is your channel and you want to add questions please contact my owner.")
                except:
                    irc.reply("I'm not on that channel, it means that Quiz is not even available on that channel.")
            else:
                irc.reply("Channel name that you gave me isn't valid channel name.")
        else:
            irc.reply("You can't do this command anywhere else except on PVT with me.")
    fixq = wrap(fixq, ['something', 'int', 'something', many('something')])

    def removeq(self, irc, msg, args, channel, number):
        """<channel> <question number>

        Removes question from channel database"""
        msg_place = msg.args[0]
        my_nick = irc.nick
        if msg_place == my_nick:
            if channel.startswith('#'):
                try:
                    ops = irc.state.channels[channel].ops
                    nick = msg.nick
                    if nick in ops:
                        try:
                            questions = 'Kviz/%s/Questions.json' % channel
                            with open(questions, 'r') as read_questions:
                                loaded_questions = json.loads(read_questions.read())
                                formated_question = str(number)
                                if formated_question in loaded_questions:
                                    del loaded_questions[formated_question]
                                    with open(questions, 'w') as write_questions:
                                        write_questions.write(json.dumps(loaded_questions))
                                        irc.reply("Question number \x02%s\x02 removed from channel database." % number)
                                else:
                                    irc.reply("Question number \x02%s\x02 not in channel database, I can't remove it." % number)
                        except:
                            irc.reply("There is no database for this channel, if this is your channel and you want to add questions please contact my owner.")
                except:
                    irc.reply("I'm not on that channel, it means that Quiz is not even available on that channel.")
            else:
                irc.reply("Channel name that you gave me isn't valid channel name.")
        else:
            irc.reply("You can't do this command anywhere else except on PVT with me.")
    removeq = wrap(removeq, ['something', 'int'])

    def score(self, irc, msg, args, name):
        """[<name>]

        Checks name score for current channel."""
        channel = msg.args[0]
        scores = 'Kviz/%s/Scores.json' % channel
        try:
            with open(scores, 'r') as read_scores:
                scores_file = json.loads(read_scores.read())
                scores_list = []
                if name is None:
                    if scores_file.keys():
                        for player, score in scores_file.items():
                            ready_score = '%s - [%s]' % (player, score)
                            scores_list.append(ready_score)
                        irc.reply("\x02%s\x02 scores are: \x02%s\x02." % (channel, ', '.join(scores_list)))
                    else:
                        irc.reply("Score database for \x02%s\x02 is empty." % channel)
                else:
                    try:
                        player_score = scores_file[name]
                        irc.reply("\x02%s\x02's score for \x02%s\x02 is: \x02%s\x02." % (name, channel, player_score))
                    except:
                        irc.reply("This player never played Quiz on this channel.")
        except:
            irc.reply("There is no scores database for this channel.")
    score = wrap(score, [optional('something')])
            

Class = Kviz


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
