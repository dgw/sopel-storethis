import os

import requests

from sopel import plugin


def _storage_filename(bot):
    return os.path.join(bot.config.core.homedir, 'stored_messages.txt')


@plugin.command('storethis')
@plugin.example('.storethis Some text that will be stored in the file')
@plugin.require_privmsg("This only works in PM.")
def store_message(bot, trigger):
    """Stores the passed text to a file that the bot owner can read later."""
    if not trigger.group(2):
        bot.reply("I need a message to store.")
        return plugin.NOLIMIT

    with open(_storage_filename(bot), 'a') as f:
        f.write('<{}> {}'.format(trigger.nick, trigger.group(2)) + '\n')

    bot.say("OK, saved that.")


@plugin.command('getthat')
@plugin.require_owner("Only the bot owner can retrieve the stored messages.")
def get_messages(bot, trigger):
    with open(_storage_filename(bot), 'r') as f:
        data = f.read()

    r = requests.post('http://sprunge.us/', data={'sprunge': data})
    try:
        r.raise_for_status()
    except Exception:
        bot.reply("Something went terribly wrong. :(")

    bot.reply("Messages: {}".format(r.text))
