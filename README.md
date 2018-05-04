# FoxQuest
Quest bot for messengers. Works for many users with many quests. Currenlty supports only telegram.

# Usage
```
python3.6 core/main.py [telegram] [settings file]
```

# Installation
1. Install python 3.6+
2. Install `pyTelegramBotAPI` with your python's pip
   ```
   Examples: 
   python3.6 -m pip install -r requirements.txt
   python3.6 -m pip install pyTelegramBotAPI
   ```
3. Run your bot

# Configuration
- [Bot configuration](settings/settings.json) (`token` is your telegram token and `quests` are pathes to your quests)
- [Simple quest](settings/simple.json)  
- [Text based quest](settings/question.json)  

- [List of available steps for quests](step_types.md) 
