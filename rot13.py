from constants import *
from string import maketrans
class Module():
  depends = ['logger']
  commands = {'rot13': 'myrot13'}

  def loaded(self):
    self.rot13_trans = maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')

  def myrot13(self, user, channel, args):
    if args:
      if args[0] in self.main.channels:
        my_channel = args[0]
        start = 1
      else:
        my_channel = channel
        start = 0

      out_str = ' '.join(args[start:])
      out_str = out_str.translate(self.rot13_trans)
      self.logger.log(LOG_DEBUG, "Saying %s in %s" % (out_str, my_channel))
      self.main.msg(my_channel, out_str, MSG_MAX)
      out_str=''
