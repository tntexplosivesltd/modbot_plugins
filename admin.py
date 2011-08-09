from constants import *

class Module():
  commands = {'nick': 'change_nick',
              'become': 'change_nick',
              'reg': 'identify',
              'identify': 'identify',
              'join': 'join_chan',
              'part': 'part_chan',
              'leave': 'part_chan',
              'me': 'me',
              'say': 'say'}
  depends = ['logger']

  def change_nick(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      if args:
        new_nick = args[0]
        self.logger.log(LOG_WARNING, "%s is changing my nick to %s" % (user, new_nick))
        self.main.setNick(new_nick)
      else:
        self.logger.log(LOG_WARNING, "%s requested my nick" % (user))
        self.main.msg(channel, self.main.nick)

  def identify(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      if args:
        msg = "identify " + args[0]
        if len(args) > 1:
          nick_serv = args[1]
        else:
          nick_serv = "NickServ"
        self.logger.log(LOG_WARNING, "%s is registering me with %s" % (user, nick_serv))
        self.main.msg(nick_serv, msg, MSG_MAX)
        msg = ''

  def join_chan(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      if args:
        new_chan = args[0]
        self.logger.log(LOG_WARNING, "%s is making me join %s" % (user, new_chan))
        self.main.join(new_chan)

  def part_chan(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      if args:
        chan_to_leave = args[0]
      else:
        chan_to_leave = channel
      self.logger.log(LOG_WARNING, "%s is making me leave %s" % (user, chan_to_leave))
      self.main.leave(chan_to_leave)

  def me(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      if args:
        if args[0] in self.main.channels:
          my_channel = args[0]
          action = ' '.join(args[1:])
          self.logger.log(LOG_WARNING, "%s is making me %s" % (user, action))
          self.main.me(my_channel, action)

  def say(self, user, channel, args):
    if (user in self.main.channels[channel]['admins']):
      if (args):
        if args[0] in self.main.channels:
          my_channel = args[0]
          msg = ' '.join(args[1:])
          self.logger.log(LOG_WARNING, "%s is making my say %s" % (user, msg))
          self.main.msg(my_channel, msg)
