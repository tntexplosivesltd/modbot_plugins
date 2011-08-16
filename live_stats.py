from ftplib import FTP_TLS
from string import *
from constants import *

class Module():
  depends = ['logger']
  hooks = {'topicupdated': 'get_topic',
           'irc_rpl_endofwho':'print_topic'}
  commands = {'update':'print_topic'}

  def write_file(self):
    output = open('chan_output.htm', 'w')
    for channel in self.main.channels:
      self.logger.log(LOG_DEBUG, "Writing output for %s, topic %s" % (channel, self.topics[channel]))
      output.write("Channel: %s\n<br />Topic: %s<br />\n<ul>\n" % (channel, self.topics[channel]))
      for user in self.main.channels[channel]['users']:
        output.write("  <li>%s</li>\n" %(user))
      output.write("</ul>\n\n")
    output.close
    
    output = open('chan_output.htm', 'r')
    self.update_all = 0
    ftp_server = 'whub25.webhostinghub.com'
    ftp_user = 'entropybot@entropy.net.nz'
    self.logger.log(LOG_INFO, "Connecting to FTP server %s, username %s" % (ftp_server, ftp_user))
    ftp = FTP_TLS(ftp_server, ftp_user, 'lol400babies')
    ftp.prot_p()
    self.logger.log(LOG_INFO, "Successfully logged in, storing file")
    ftp.storlines('STOR chan_output.htm', output)
    ftp.close()
    output.close()
    self.logger.log(LOG_INFO, "Done")


  def loaded(self):
    self.topics = {}
    self.repliesleft = 0
    self.update_all = 0
    for my_channel in self.main.channels:
      self.logger.log(LOG_DEBUG, "Getting topic from %s" % (my_channel))
      self.main.topic(my_channel)

  def print_topic(self, user, channel, args):
    if user in self.main.channels[channel]['admins']:
      self.update_all = 1
      self.repliesleft = len(self.main.channels)
      for my_channel in self.main.channels:
        self.logger.log(LOG_DEBUG, "Getting topic from %s" % (my_channel))
        self.main.topic(my_channel)

  def get_topic(self, user, channel, topic):
    topic = topic.rstrip('\n')
    if not topic:
      topic = '(none)'
    self.topics[channel]=topic
    if self.update_all:
      self.repliesleft -= 1
    else:
      self.replieslift = 0
    self.logger.log(LOG_INFO, "%s: %s. Replies left: %s" % (channel, self.topics[channel], self.repliesleft))
    if not self.repliesleft:
      self.write_file()