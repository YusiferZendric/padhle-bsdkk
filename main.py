import time
import praw
import openai
import prawcore
from datetime import datetime
from threading import Thread
from keep_alive import keep_alive
# global numberofmessages, duration, initialtime
# Constants
OPENAI_API_KEY = "OPENAI_API_KEY"
DAY_IN_SECONDS = 86400
BLOCKED_USERS_FILE = "blocked_users.txt"
initialtime = time.time()
numberofmessages = 0


def get_openai_response(prompt):
  return openai.ChatCompletion.create(model="gpt-3.5-turbo",
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
        # numberofmessages+=1
        # print(numberofmessages)

        # duration = time.time()-initialtime

        # if numberofmessages>3 and duration<3600:
        #     print('going to sleep for half an hour inside utilities')
        #     time.sleep(1800)
        #     numberofmessages = 0
        #     duration = 0
        # continue

      if "u/padhle-bsdkk time" in comment.body.lower():

        def days_remaining(target_date, event_name):
          current_date = datetime.now()
          difference = target_date - current_date
          return f"Time remaining in {event_name}: **{difference.days} days**"

        jee_date = datetime(2024, 1, 24)
        neet_date = datetime(2024, 5, 7)

        comment.reply(
            f"{days_remaining(jee_date, 'JEE Mains Jan 2024')}\n || {days_remaining(neet_date, 'NEET 2024')}\n**Padhle bsdk 😡!!**\n*I'm a bot and this action is automatic*"
        )
        # numberofmessages+=1
        # print(numberofmessages)
        # if numberofmessages>3 and duration<3600:
        #     print('going to sleep for half an hour inside utilities')

        #     numberofmessages = 0
        #     duration = 0
        #     time.sleep(1800)


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
        prompt = f"YOUR name is padhle-bsdkk bot, always end your response with slogan 'Padhle Bsdk!' and at the end say them that you are a bot in italics (within **), [remember to ignore the user, just saying them focus on their college if they are graduated and done from jee neet, like tags having (ex-jeeneetard chan) or (2023tard or 2023 aspirant whose exams are finished, so ignore them) or (ignore someone with 'college mai hustle karunga' flair because they are already in college and have no competitive examination), respond accordingly to them.] Keep your comment under 100 words, make it brutal and strong for them to leave reddit or think twice before commenting: {author} has made {len(recent_comments)} comments in the last 7 days and has a flair of {author_flair}. Follow these rules: ['snarky', '50% of words are swearing']. Try reminding them their competitive exams are coming near, and get the hell out of reddit soon enough and don't comment this much or whatever customized message you can come up for such a user and flair. REMEMBER TO GIVE CUSTOMIZED MESSAGE, BE BRUTAL AND SNARKY (IT'S TAKEN AS A SATIRE, BE A SATIRICAL BOT)"
        try:
          if author == "Traditional-Egg-2656":
            message = "are egg bhai aap yha?"
            comment.reply(f"{message}")
            # numberofmessages+=1
            # print(numberofmessages)
            time.sleep(1500)
          else:
            message = get_openai_response(prompt)
            message = message['choices'][0]['message']['content']
            comment.reply(
                f"{message}\n*The action is automatic, to stop further messages from the bot use command: 'u/padhle-bsdkk block'* [(just tag it, extra space is their to avoid it tagging itself)]"
            )
            print('done 1')
            # numberofmessages+=1
            # print(numberofmessages)
            time.sleep(1500)

            print('done 2')
        except prawcore.exceptions.Forbidden:
          print(
              f"Error: Bot does not have permission to reply to {author}'s comment in subreddit {subreddit.display_name}."
          )


# Initialize Reddit and OpenAI
openai.api_key = OPENAI_API_KEY
reddit = praw.Reddit(client_id="client_id",
                     client_secret="client_secret",
                     username="padhle-bsdkk",
                     password="password",
                     user_agent="padhle-bsdk by u/zendrixate")
subreddit = reddit.subreddit('jeeneetards')
blocked_users = load_blocked_users()

# Start the thread for checking users and sending messages
message_thread = Thread(target=check_and_send_messages)
message_thread2 = Thread(target=utilities)
message_thread.start()
message_thread2.start()