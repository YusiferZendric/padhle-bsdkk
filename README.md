# Padhle-Bsdkk Bot

## Overview
This is a Reddit bot made specifically for the `r/jeeneetards` subreddit. It uses PRAW (Python Reddit API Wrapper) and the GPT-3.5-turbo model from OpenAI to interact with the community. It performs multiple functions like tracking time remaining for JEE and NEET exams, providing motivational quotes, and encouraging users to study. It also allows users to block or unblock the bot.

## Features
- **Block/Unblock Users**: Users can block or unblock the bot by mentioning it with the commands `u/padhle-bsdkk block` or `u/padhle-bsdkk unblock`.
- **Time Remaining**: Users can get the time remaining for JEE and NEET exams by mentioning `u/padhle-bsdkk time`. An image with a countdown and a motivational quote is generated.
- **Send Messages**: The bot will reply to comments by users not on the blocked list. Replies are generated using OpenAI's GPT-3.5-turbo model.

## Dependencies
- PRAW
- OpenAI
- Python Image Library (PIL)
- Pandas
- ImgurPython
- DateTime
- threading
- textwrap

## Configuration
- **Imgur**: Requires client_id and client_secret for uploading images.
- **OpenAI**: An API key is needed for using the GPT-3.5-turbo model.
- **Reddit**: `client_id`, `client_secret`, `username`, `password`, and `user_agent` are required for Reddit API access.

## Setup
1. Install all the dependencies.
2. Fill in the configuration details for Imgur, OpenAI, and Reddit.
3. Run the script to start the bot.

## Usage
To interact with the bot, users can use the following commands within the comments section of the `r/jeeneetards` subreddit:
- `u/padhle-bsdkk block`: To block the bot.
- `u/padhle-bsdkk unblock`: To unblock the bot.
- `u/padhle-bsdkk time`: To get an image with time remaining for exams and a motivational quote.

**Note**: This is a fictional bot, and its purpose is satirical. Use at your own risk.
