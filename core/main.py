import sys
import quest


def failed():
    print('Usage:\npython3.6 core/main.py [telegram] [settings file]')
    exit(1)

tostart = ""
manager = None

if len(sys.argv) == 1:
    tostart = 'telegram'

elif len(sys.argv) == 2:
    if sys.argv[1] not in ('telegram', ):
        failed()

    tostart = sys.argv[1]

elif len(sys.argv) == 3:
    if sys.argv[1] not in ('telegram', ):
        failed()

    tostart = sys.argv[1]
    manager = quest.create_manager(sys.argv[2])

else:
    failed()

if tostart == 'telegram':
    import telegram
    telegram.start_telegram(manager if manager else quest.create_manager("settings/settings.json"))
