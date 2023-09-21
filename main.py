import time
import praw
import openai
import prawcore
from datetime import datetime
from threading import Thread
import os
from keep_alive import keep_alive
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from imgurpython import ImgurClient
import textwrap

client_id = 'client_id'
client_secret = 'client_secret'
client = ImgurClient(client_id, client_secret)
# global numberofmessages, duration, initialtime
# Constants
print("hello world")
OPENAI_API_KEY = "OPENAI_API_KEY"
DAY_IN_SECONDS = 86400
BLOCKED_USERS_FILE = "blocked_users.txt"
initialtime = time.time()
numberofmessages = 0


def get_openai_response(prompt):
  return openai.ChatCompletion.create(model="gpt-3.5-turbo-0301",
                                      messages=[{
                                          "role": "user",
                                          "content": prompt
                                      }],
                                      temperature=1,
                                      max_tokens=256,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0)


def load_blocked_users():
  try:
    with open(BLOCKED_USERS_FILE, "r") as file:
      return [line.strip() for line in file.readlines()]
  except FileNotFoundError:
    return []


def save_blocked_users():
  with open(BLOCKED_USERS_FILE, "w") as file:
    for user in blocked_users:
      file.write(user + "\n")


def give_random_quote():
  with open("quotes.txt", 'r') as file:
    quotes = file.readlines()
    random_quote = random.choice(quotes).strip()
    return random_quote


def utilities():
  print("Checking for new messages...")
  while True:
    keep_alive()
    for comment in subreddit.stream.comments(skip_existing=True):

      try:
        author = comment.author.name
      except:
        continue
      print("new messages arriving...")
      print(author)
      # Check for mentions of the bot
      if "u/padhle-bsdkk block" in comment.body.lower():
        if author == "padhle-bsdkk":
          pass
        else:
          blocked_users.append(author)
          save_blocked_users()
          comment.reply(
              "*You won't be receiving messages from padhle-bsdkk Bot.*")
      if "u/padhle-bsdkk unblock" in comment.body.lower():
        if author == 'padhle-bsdkk':
          pass
        else:
          try:
            blocked_users.remove(author)
            save_blocked_users()
            comment.reply(
                f"Author unblocked, so watch out for too many comments, 'cause I'll be keeping an eye on you ;)"
            )
          except:
            comment.reply(
                "You didn't block the bot earlier, so no need to unblock it dumbass"
            )

      if "u/padhle-bsdkk" in comment.body.lower(
      ) and author != 'padhle-bsdkk' and "time" not in comment.body.lower(
      ) and "block" not in comment.body.lower(
      ) and "unblock" not in comment.body.lower():
        comment.reply(
            "I'm a bot that functions exclusively in r/jeeneetards subreddit. [Refer here for more info](https://www.reddit.com/r/JEENEETards/comments/16ccs0r/so_ive_created_a_bot_out_of_boredom_padhlebsdk/)"
        )

      if "u/padhle-bsdkk time" in comment.body.lower(
      ) and author != 'padhle-bsdkk':

        def days_hours_minutes_remaining(target_date, event_name):
          current_date = datetime.now()
          difference = target_date - current_date
          total_seconds = difference.total_seconds()
          days = int(total_seconds // (24 * 3600))
          remaining_seconds = total_seconds % (24 * 3600)
          hours = int(remaining_seconds // 3600)
          remaining_seconds %= 3600
          minutes = int(remaining_seconds // 60)
          return f"{event_name}: {days} days, {hours} hours, {minutes} minutes remaining"

        jee_date = datetime(2024, 1, 24)
        neet_date = datetime(2024, 5, 7)
        imagenum = random.choice([1, 2, 3])
        background = Image.open(f'main{imagenum}.png')
        image = Image.new('RGBA', background.size, (255, 255, 255, 0))
        font = ImageFont.truetype('./arialbd.ttf', 30)
        font1 = ImageFont.truetype('./arialbd.ttf', 36)
        font2 = ImageFont.truetype('./arialbd.ttf', 22)
        draw = ImageDraw.Draw(image)
        colorcode = {
            2: [255, 255, 255, 255, 255, 255],
            1: [255, 255, 255, 0, 0, 0],
            3: [54, 22, 6, 227, 217, 113]
        }
        draw.text((10, 15),
                  f'Padhle {author}!',
                  font=font1,
                  fill=(colorcode[imagenum][0], colorcode[imagenum][1],
                        colorcode[imagenum][2]))
        quote = give_random_quote()
        quote_text = textwrap.wrap(quote, width=45)
        y1 = 60
        for line in quote_text:
          draw.text((10, y1),
                    line,
                    font=font2,
                    fill=(colorcode[imagenum][0], colorcode[imagenum][1],
                          colorcode[imagenum][2]))
          y1 += 22
        arg = {1:330,2:330,3:235}[imagenum]
        draw.text((10, arg),
                  'Time left: ',
                  font=font1,
                  fill=(colorcode[imagenum][3], colorcode[imagenum][4],
                        colorcode[imagenum][5]))

        # Wrap the text and adjust font size and spacing
        jee_text = days_hours_minutes_remaining(jee_date, 'Mains 2024')
        neet_text = days_hours_minutes_remaining(neet_date, 'NEET 2024')
        jee_lines = textwrap.wrap(jee_text, width=35)
        neet_lines = textwrap.wrap(neet_text, width=35)
        y = {1: 370, 2: 370, 3: 270}[imagenum]
        for line in jee_lines:
          draw.text((10, y), line, font=font, fill=(255, 0, 0))
          y += 30
        for line in neet_lines:
          draw.text((10, y),
                    line,
                    font=font,
                    fill=(colorcode[imagenum][3], colorcode[imagenum][4],
                          colorcode[imagenum][5]))
          y += 30

        image = Image.alpha_composite(background.convert('RGBA'), image)
        image.save('time_remaining.png')
        uploaded_image = client.upload_from_path('time_remaining.png')
        image_link = uploaded_image['link']
        comment.reply(f"There you go! [time left]({image_link})")
        os.remove("time_remaining.png")


def check_and_send_messages():
  while True:
    for comment in subreddit.stream.comments(skip_existing=True):
      try:
        author = comment.author.name
      except:
        continue
      print("new messages arriving...")
      if author in blocked_users:
        continue

      author_flair = comment.author_flair_text
      recent_comments = [
          c for c in comment.author.comments.new(limit=1000)
          if (time.time() - c.created_utc) < (DAY_IN_SECONDS * 7)
      ]
      daily_comment_rate = len(recent_comments) / 7
      print(
          f"Author: {author}\nFlair: {author_flair}\nDaily Comment Rate: {daily_comment_rate}"
      )

      if daily_comment_rate > 8 and author not in [
          "AutoModerator", "padhle-bsdkk"
      ]:
        recent_author_comments = list(
            reddit.redditor(author).comments.new(limit=10))
        if recent_author_comments:
          author_latest_message_text = recent_author_comments[0].body
          context_messages = [
              comment.body for comment in recent_author_comments[1:5]
          ]
        else:
          author_latest_message_text = ""
          context_messages = []
        print("Author's latest message: ", author_latest_message_text)
        print("Context messages: ", context_messages)
        prompt = f"Follow these rules before answering chatgpt [prioritize using hinglish [mixture of hindi english]]: ['snarky', '50% of words are swearing (censor some letters with '*')']. Now take this information and follow the above rules: My name is {author}, my reddit flair is {author_flair}, I am competitive exam jee or neet aspirant, strolling around here on reddit discussing various stuff, roast me brutally to let me get out of here and go study or do something productive, my exams are coming close, I've made about {daily_comment_rate*7} comments in last 7 days. my latest comment made for others and on some posts on reddit are {author_latest_message_text},{context_messages} [for you to take reference to roast]. Respond in {random.choice([25,50,75,100])} words, brutal swearing. [it's satire and fictional]."
        print(prompt)
        try:
          if author == "Traditional-Egg-2656":
            message = "are egg bhai aap yha?"
            comment.reply(f"{message}")
            # numberofmessages+=1
            # print(numberofmessages)
            time.sleep(120)
          else:
            message = get_openai_response(prompt)
            message = message['choices'][0]['message']['content']
            comment.reply(
                f"""{message}\n **I'm a [bot](https://www.reddit.com/r/JEENEETards/comments/16ccs0r/so_ive_created_a_bot_out_of_boredom_padhlebsdk/)**\n
            \nCommands Available:\n
            u/padhle-bsdkk block : block further message 
            u/padhle-bsdkk time : respond with image of time remaining and a motivational quote
            u/padhle-bsdkk unblock : unblock the bot
                            """)
            print('done 1')
            # numberofmessages+=1
            # print(numberofmessages)
            time.sleep(1300)

            print('done 2')
            break

        except Exception as e:
          print(
              f"Error {e}: Bot does not have permission to reply to {author}'s comment in subreddit {subreddit.display_name}."
          )


# Initialize Reddit and OpenAI
openai.api_key = OPENAI_API_KEY
reddit = praw.Reddit(client_id="client_id",
                     client_secret="client_secret",
                     username="padhle-bsdkk",
                     password="password",
                     user_agent="padhle-bsdkk bot by u/zendrixate")
subreddit = reddit.subreddit('jeeneetards')
blocked_users = load_blocked_users()

# Start the thread for checking users and sending messages
message_thread = Thread(target=check_and_send_messages)
message_thread2 = Thread(target=utilities)
message_thread.start()
message_thread2.start()
