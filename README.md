# reCAPTCHA Telegram Bot

Telegram bot that sends reCAPTCHA styled image when someone enters a chat.

## Usage

At first you need to install dependencies:

**Ubuntu:**

```bash
cd ./recaptcha-tg-bot
python3 -m venv env
source ./env/bin/activate
pip install -r requirements
```

**Windows:**

```powershell
cd .\recaptcha-tg-bot
python -m venv env
.\env\Scripts\activate
pip install -r .\requirements.txt
```

Then you can run the bot:

```bash
python -m captcha_bot
```

But at the first launch it will raise an error, that says you need to fill values in just created `settings.json` file. More on this below in [Settings File](#settings-file) section. 

Next step you need to create `images` directory. In it create other directories with images on some theme. The name of each directory will be used as captcha image caption.

After all you will be able to run it.

In Telegram add the bot to your chat (also make sure that `chats_id` array in settings file has its ID or that it's empty) and make it admin.

If you want to get some captcha images, you can direct message the bot. It will send you all its commands on the `/start` command.

## Settings File

All bot settings stored in `settings.json` file. After the first launch there will be placeholders and some of them you will need to replace.

- `token` - your bot token from [BotFather](https://botfather.t.me/)
- `owner_id` - your Telegram ID
- `chats_id` - chats where bot will work, leave the array empty to make the bot work in any chat
- `include_directories` - directory names in `images` directory that will be used in the captcha, leave the array empty to use all directories 
- `exclude_directories` - directory names in `images` directory that won't be used in the captcha, leave the array empty to use all directories
- `no_caption_directories` - directory names in `images` directory that will be used in the captcha, but won't be used as caption of it, leave the array empty to use all directories
- `kick_delay` - the number of minutes that must pass before the bot kicks the user, if it's `0`, bot will never kick the user
- `messages_text`
  - `joined` - text used as caption of the captcha image (allowed keys: `username`, `first_name`, `full_name`, `answers`)
  - `answer` - text used when user tried to solve the captcha (allowed keys: `username`, `first_name`, `full_name`, `correct`, `incorrect`, `congrats`)
  - `no_nums` - congrats when there is no numbers in the user answer
  - `no_text` - congrats when there is no text in the user answer
  - `<n>_correct` - congrats when there is `<n>` correct answers
  - `incorrect` - congrats when there is 4 correct and more than 2 incorrect answers

### Allowed Keys

Some of message texts can be formatted with some keys. 

- `username` - '\@' symbol with user's  username
- `first_name` - user's first name
- `full_name` - user's first and last name 
- `answers` - list of correct captcha answers
- `correct` - number of user correct answers
- `incorrect` - number of user incorrect answers
- `congrats` - text based on number of correct and incorrect answers

For example this text:

`some text... {username} | {first_name} | {full_name} | {answers} | {correct} | {incorrect} | {congrats}`

will be formatted as: 

`some text... @dofoerix | @Dofoerix | Dofoerix Second Name | 1, 4, 5, 9 | 3 | 1 | Not bad!`

## Licenses

This bot use Roboto font by Christian Robertson. It's licensed under the Apache License, Version 2.0.

Bot itself licensed under the MIT license.