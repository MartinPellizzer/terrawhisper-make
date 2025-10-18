import random

from lib import io

from tkinter import *

from oliark_llm import llm_reply

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

def tk_tweet_save():
    ###
    twitter_folderpath = f'social/twitter'
    twitter_posts_filepath = f'{twitter_folderpath}/twitter-posts.json'
    twitter_posts_json = io.json_read(twitter_posts_filepath, create=True)
    if 'posts' not in twitter_posts_json: twitter_posts_json['posts'] = []
    io.json_write(twitter_posts_filepath, twitter_posts_json)
    ###
    tweet_reply = tweet_reply_textarea.get('1.0', END)
    tweet = {
        'posted': 0,
        'content': tweet_reply,
    }
    twitter_posts_json['posts'].append(tweet)
    io.json_write(twitter_posts_filepath, twitter_posts_json)

prompt = f'''
My niche is DIY herbalists and home apothecaries.
Give me a complete numbered list of smart ideas for content generation in headline form.

Smart ideas must not blend with others in my industry, they must be unique, novel, and uncommon.
Smart ideas must spark action, reach a goal, improve a situation, or solve a problem. 
Smart ideas must be tactical and practical.
Smart ideas must give a quick win, be easy to implement, and be transformational.
Smart ideas are like life hacks.

Reply only with the list.
'''.strip()

tweet_prompt = f'''
write a tweet in less than 140 characters about the following headline: [headline]

start with a short puchy one-liner explaining what the tweet is about.
follow with a numebred ordered list of 3-5 actionable steps explaining how to do it practically.
these steps must be less than 7 words.
these steps must be tactical and practical.
these ideas must not blend with others in my industry, they must be unique, novel, and uncommon.
end with a short punchy one-liner explaining why it's important.
don't use emojies.
add a new empty line between the sentences.
'''.strip()

def tk_idea_random_get():
    ideas_reply = ideas_reply_textarea.get('1.0', END)
    ideas = [line.strip() for line in ideas_reply.split('\n') if line.strip() != '']
    idea_i = random.randint(0, len(ideas))
    idea_prompt_textarea.delete(1.0, END)
    idea_prompt_textarea.insert(END, ideas[idea_i])
    del ideas[idea_i]
    ideas = '\n'.join(ideas)
    ideas_reply_textarea.delete(1.0, END)
    ideas_reply_textarea.insert(END, ideas)
    tk_tweet_reply_gen()

def tk_tweet_characters_get():
    tweet_reply = tweet_reply_textarea.get('1.0', END)
    tweet_characters_textarea.delete(1.0, END)
    tweet_characters_textarea.insert(END, str(len(tweet_reply)))

def tk_ideas_reply_gen():
    prompt = ideas_prompt_textarea.get('1.0', END)
    prompt += f'/no_think'
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    reply = reply.replace('**', '')
    reply = reply.replace('"', '')
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        line = line.strip()
        if line == '': continue
        lines.append(line)
    lines_reply = '\n'.join(lines)
    ideas_reply_textarea.delete(1.0, END)
    ideas_reply_textarea.insert(END, lines_reply)

def tk_tweet_reply_gen():
    headline = idea_prompt_textarea.get('1.0', END)
    prompt = tweet_prompt_textarea.get('1.0', END)
    prompt = prompt.replace('[headline]', headline)
    prompt += f'/no_think'
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    reply = reply.replace('**', '')
    tweet_reply_textarea.delete(1.0, END)
    tweet_reply_textarea.insert(END, reply)

root = Tk() 
###
root.geometry('1920x1080')
###
frame_1 = Frame(root)
frame_1.pack(side=LEFT)
ideas_prompt_textarea = Text(frame_1, width=100, padx=10, pady=10)
ideas_prompt_textarea.pack(padx=10, pady=10)
ideas_prompt_textarea.delete(1.0, END)
ideas_prompt_textarea.insert(END, prompt)
ideas_reply_textarea = Text(frame_1, width=100, padx=10, pady=10)
ideas_reply_textarea.pack(padx=10, pady=10)
reply_button = Button(frame_1, text='reply', command=tk_ideas_reply_gen)
reply_button.pack()
###
frame_2 = Frame(root)
frame_2.pack(side=LEFT)
idea_random_button = Button(frame_2, text='idea random', command=tk_idea_random_get)
idea_random_button.pack()
idea_prompt_textarea = Text(frame_2, width=100, height=1, padx=10, pady=10)
idea_prompt_textarea.pack(padx=10, pady=10)
tweet_prompt_textarea = Text(frame_2, width=100, padx=10, pady=10)
tweet_prompt_textarea.pack(padx=10, pady=10)
tweet_prompt_textarea.delete(1.0, END)
tweet_prompt_textarea.insert(END, tweet_prompt)
tweet_reply_textarea = Text(frame_2, width=100, height=10,padx=10, pady=10)
tweet_reply_textarea.pack(padx=10, pady=10)
tweet_characters_button = Button(frame_2, text='calculate characters', command=tk_tweet_characters_get)
tweet_characters_button.pack()
tweet_characters_textarea = Text(frame_2, width=100, height=1, padx=10, pady=10)
tweet_characters_textarea.pack(padx=10, pady=10)
tweet_reply_button = Button(frame_2, text='tweet reply', command=tk_tweet_reply_gen)
tweet_reply_button.pack()
###
frame_3 = Frame(root)
frame_3.pack(side=LEFT)
tweet_save_button = Button(frame_3, text='tweet save', command=tk_tweet_save)
tweet_save_button.pack()
###
root.mainloop()

