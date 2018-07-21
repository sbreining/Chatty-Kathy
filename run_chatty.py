"""
Initiator of the program. Needs command line arguments to get started.
The arguments are needed at the command line because they are the secret
token and client id needed from starting a developer account with Twitch.
"""

import sys
from ch4tty.chatbot import TwitchBot


def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    bot = TwitchBot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    bot.start()


if __name__ == "__main__":
    main()
