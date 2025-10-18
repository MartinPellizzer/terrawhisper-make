import os
import json
import random
from datetime import datetime

from oliark_llm import llm_reply
from oliark import img_resize

from PIL import Image, ImageDraw, ImageFont

import llm
from lib import g
from lib import io
from lib import data
from lib import utils
from lib import components

from lib_twitter import twitter_post

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

# twitter_post.gen()

# quit()

if 0:
    # json init month list
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath, create=True)
    month_list = []
    for month_num in range(0, 12):
        if month_num == 0: month_name = 'january'
        elif month_num == 1: month_name = 'february'
        elif month_num == 2: month_name = 'march'
        elif month_num == 3: month_name = 'april'
        elif month_num == 4: month_name = 'may'
        elif month_num == 5: month_name = 'june'
        elif month_num == 6: month_name = 'july'
        elif month_num == 7: month_name = 'august'
        elif month_num == 8: month_name = 'september'
        elif month_num == 9: month_name = 'october'
        elif month_num == 10: month_name = 'november'
        elif month_num == 11: month_name = 'december'
        month_list.append({
            'month_name': month_name,
            'month_ailments': [],
        })
    json_article['month_list'] = month_list
    io.json_write(json_article_filepath, json_article)

if 0:
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    for month_i, month in enumerate(json_article['month_list']):
        month_name = month['month_name']
        month_ailments = month['month_ailments']
        prompt = f'''
            List the 30 most common seasonal ailments people get in the month of {month_name.capitalize()}.
            Also, for common ailment give a confidence score from 1 to 10, indicating how sure you are that answer.
            Write as few words as possible.
            Reply in the following JSON format: 
            [
                {{"answer": "write common ailment 1 here", "score": "10"}}, 
                {{"answer": "write common ailment 2 here", "score": "5"}}, 
                {{"answer": "write common ailment 3 here", "score": "7"}}, 
                {{"answer": "write common ailment 4 here", "score": "2"}}, 
                {{"answer": "write common ailment 5 here", "score": "6"}}, 
                {{"answer": "write common ailment 6 here", "score": "3"}}, 
                {{"answer": "write common ailment 7 here", "score": "9"}}, 
                {{"answer": "write common ailment 8 here", "score": "4"}}, 
                {{"answer": "write common ailment 9 here", "score": "1"}}, 
                {{"answer": "write common ailment 10 here", "score": "8"}}, 
                {{"answer": "write common ailment 11 here", "score": "10"}}, 
                {{"answer": "write common ailment 12 here", "score": "5"}}, 
                {{"answer": "write common ailment 13 here", "score": "7"}}, 
                {{"answer": "write common ailment 14 here", "score": "2"}}, 
                {{"answer": "write common ailment 15 here", "score": "6"}}, 
                {{"answer": "write common ailment 16 here", "score": "3"}}, 
                {{"answer": "write common ailment 17 here", "score": "9"}}, 
                {{"answer": "write common ailment 18 here", "score": "4"}}, 
                {{"answer": "write common ailment 19 here", "score": "1"}}, 
                {{"answer": "write common ailment 20 here", "score": "8"}}, 
                {{"answer": "write common ailment 21 here", "score": "10"}}, 
                {{"answer": "write common ailment 22 here", "score": "5"}}, 
                {{"answer": "write common ailment 23 here", "score": "7"}}, 
                {{"answer": "write common ailment 24 here", "score": "2"}}, 
                {{"answer": "write common ailment 25 here", "score": "6"}}, 
                {{"answer": "write common ailment 26 here", "score": "3"}}, 
                {{"answer": "write common ailment 27 here", "score": "9"}}, 
                {{"answer": "write common ailment 28 here", "score": "4"}}, 
                {{"answer": "write common ailment 29 here", "score": "1"}}, 
                {{"answer": "write common ailment 30 here", "score": "8"}} 
            ]
            Only reply with the JSON, don't add additional info.
        '''
        prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        if json_data != {}:
            objects = []
            for item in json_data:
                try: answer = item['answer']
                except: continue
                try: score = item['score']
                except: continue
                objects.append({
                    "answer": answer, 
                    "score": score,
                })
        month['month_ailments'] = objects
        io.json_write(json_article_filepath, json_article)

def get_ailment_today():
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    return ailment

def ai_llm_thread():
    ailment = get_ailment_today()
    ailment_name = ailment['answer']
    prompt = f'''
        List the names of the 10 best types of herbal preparations to heal {ailment_name}.
        By types of herbal preparations I mean things like: tea, tincture, creams, etc.
        Don't include suppository.
        Don't include names of herbs.
        Use only 1 word for preparation.
        Also, for each answer give a confidence score from 1 to 10, indicating how sure you are that answer.
        Reply in the following JSON format: 
        [
            {{"answer": "write preparation 1 here", "score": "10"}}, 
            {{"answer": "write preparation 2 here", "score": "5"}}, 
            {{"answer": "write preparation 3 here", "score": "7"}}, 
            {{"answer": "write preparation 4 here", "score": "2"}}, 
            {{"answer": "write preparation 5 here", "score": "6"}}, 
            {{"answer": "write preparation 6 here", "score": "3"}}, 
            {{"answer": "write preparation 7 here", "score": "9"}}, 
            {{"answer": "write preparation 8 here", "score": "4"}}, 
            {{"answer": "write preparation 9 here", "score": "1"}}, 
            {{"answer": "write preparation 10 here", "score": "8"}} 
        ]
        Only reply with the JSON, don't add additional info.
        /no_think
    '''
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    preparation_list = []
    if json_data != {}:
        for item in json_data:
            try: answer = item['answer']
            except: continue
            try: score = item['score']
            except: continue
            preparation_list.append({
                "answer": answer, 
                "score": score,
            })
    preparation_list = sorted(preparation_list, key=lambda x: x['score'], reverse=True)
    print(preparation_list)
    ###
    preparation_name_list = []
    for preparation in preparation_list[:5]:
        preparation_name = preparation['answer']
        prompt = f'''
            List the names of the 10 best herbs used to make herbal {preparation_name} to heal {ailment_name}.
            Also, for each answer give a confidence score from 1 to 10, indicating how sure you are that answer.
            Reply in the following JSON format: 
            [
                {{"answer": "write herb 1 here", "score": "10"}}, 
                {{"answer": "write herb 2 here", "score": "5"}}, 
                {{"answer": "write herb 3 here", "score": "7"}}, 
                {{"answer": "write herb 4 here", "score": "2"}}, 
                {{"answer": "write herb 5 here", "score": "6"}}, 
                {{"answer": "write herb 6 here", "score": "3"}}, 
                {{"answer": "write herb 7 here", "score": "9"}}, 
                {{"answer": "write herb 8 here", "score": "4"}}, 
                {{"answer": "write herb 9 here", "score": "1"}}, 
                {{"answer": "write herb 10 here", "score": "8"}} 
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        herb_list = []
        if json_data != {}:
            for item in json_data:
                try: answer = item['answer']
                except: continue
                try: score = item['score']
                except: continue
                herb_list.append({
                    "answer": answer, 
                    "score": score,
                })
        herb_list = sorted(herb_list, key=lambda x: x['score'], reverse=True)
        herb_list = herb_list[:5]
        random.shuffle(herb_list)
        herb = herb_list[0]
        herb_name = herb['answer']
        preparation_name_list.append(f'{preparation_name}')
    ###
    herb_name_list = [herb['answer'] for herb in herb_list]
    herb_preparation_name_list = [
        f'{herb_name_list[0]} {preparation_name_list[0]}',
        f'{herb_name_list[1]} {preparation_name_list[1]}',
        f'{herb_name_list[2]} {preparation_name_list[2]}',
        f'{herb_name_list[3]} {preparation_name_list[3]}',
        f'{herb_name_list[4]} {preparation_name_list[4]}',
    ]
    thread = []
    for preparation_i, preparation_name in enumerate(herb_preparation_name_list):
        with open('assets/prompt/raw-mode.txt') as f: guidelines = f.read()
        guidelines = f'Use short and simple words. Use a down to earth tone. Use active language.'
        prompt = f'''
            Write a tweet about the following herbal remedy for {ailment_name}: {preparation_name}.
            Follow the STRUCTURE and GUIDELINES below to write the tweet.
            STRUCTURE:
            Start the tweet with the following one-liner: "{preparation_i+1}. {preparation_name}".
            Then explain why it works, including active constituents and how they interact with the body.
            End with a practical tip (without spelling the word "tip").
            GUIDELINES:
            {guidelines}
            Don't add bold and italics.
            Add an empty line between the tweet lines.
            Write less than 240 characters, about 3 sentences.
        '''
        prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        tweet = {
            'herb_name': herb_name_list[preparation_i],
            'preparation_name': preparation_name_list[preparation_i],
            'content': reply,
        }
        thread.append(tweet)
    for tweet in thread:
        print('#######################################')
        print(tweet)
        print('#######################################')
    for i, tweet in enumerate(thread):
        print(f'{i+1} - LEN: {len(tweet["content"])}')
    ###
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    ailment['thread'] = thread
    io.json_write(json_article_filepath, json_article)

if 0:
    ailment = get_ailment_today()
    ailment_name = ailment['answer']
    preparation_name_list = [
        'Tincture',
        'Steam',
        'Oil',
        'Lozenge',
        'Cream',
    ]
    herb_preparation_name_list = [
        'Clove Tincture',
        'Peppermint Steam',
        'Peppermint Oil',
        'Ginger Lozenge',
        'Chamomile Cream',
    ]
    herb_name_list = [
        'Clove',
        'Peppermint',
        'Peppermint',
        'Ginger',
        'Chamomile',
    ]
    thread = []
    for preparation_i, preparation_name in enumerate(herb_preparation_name_list):
        with open('assets/prompt/raw-mode.txt') as f: guidelines = f.read()
        guidelines = f'Use short and simple words. Use a down to earth tone. Use active language.'
        prompt = f'''
            Write a tweet about the following herbal remedy for {ailment_name}: {preparation_name}.
            Follow the STRUCTURE and GUIDELINES below to write the tweet.
            STRUCTURE:
            Start the tweet with the following one-liner: "{preparation_i+1}. {preparation_name}".
            Then explain why it works, including active constituents and how they interact with the body.
            End with a practical tip (without spelling the word "tip").
            GUIDELINES:
            {guidelines}
            Don't add bold and italics.
            Add an empty line between the tweet lines.
            Write less than 240 characters, about 3 sentences.
        '''
        prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        tweet = {
            'herb_name': herb_name_list[preparation_i],
            'preparation_name': preparation_name_list[preparation_i],
            'content': reply,
        }
        thread.append(tweet)
    for tweet in thread:
        print('#######################################')
        print(tweet)
        print('#######################################')
    for i, tweet in enumerate(thread):
        print(f'{i+1} - LEN: {len(tweet)}')
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    ailment['thread'] = thread
    io.json_write(json_article_filepath, json_article)

def ai_llm_txt():
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    thread = ailment['thread']
    tweets = ''
    for tweet in thread:
        tweets += tweet['content'] + '\n\n\n'
    with open('twitter/thread.txt', 'w') as f: f.write(tweets)

# ai_llm_thread()
# ai_llm_txt()
# quit()

if 1:
    import torch
    from diffusers import DiffusionPipeline
    from diffusers import StableDiffusionXLPipeline
    from diffusers import DPMSolverMultistepScheduler
    checkpoint_filepath = f'{g.VAULT}/stable-diffusion/checkpoints/xl/juggernautXL_ragnarokBy.safetensors'
    pipe = None
    quality = 100
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    thread = ailment['thread']
    for tweet_i, tweet in enumerate(thread):
        img_filepath = f'twitter/{tweet_i}.jpg'
        if os.path.exists(img_filepath): continue
        preparation_name = tweet['preparation_name']
        herb_name = tweet['herb_name']
        prompt = f'''
            {preparation_name}s,
            on a wooden table,
            surrounded by dry {herb_name},
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''
        negative_prompt = ''
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        img_filepath = f'twitter/{tweet_i}.jpg'
        image.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

    img_filepath = f'twitter/featured.jpg'
    if not os.path.exists(img_filepath):
    # if True:
        quality = 100
        if pipe == None:
            pipe = StableDiffusionXLPipeline.from_single_file(
                checkpoint_filepath, 
                torch_dtype=torch.float16, 
                use_safetensors=True, 
                variant="fp16"
            ).to('cuda')
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        month = datetime.now().date().month
        day = datetime.now().date().day
        json_article_filepath = f'twitter/data.json'
        json_article = io.json_read(json_article_filepath)
        ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
        thread = ailment['thread']
        preparations_names = [tweet['preparation_name'] for tweet in thread]
        preparations_names = ' '.join(preparations_names[:3])
        herbs_names = [tweet['herb_name'] for tweet in thread]
        herbs_names = ' '.join(herbs_names[:3])
        prompt = f'''
            herbal {thread[0]['preparation_name']} made with dry {thread[0]['herb_name']},
            herbal {thread[1]['preparation_name']} made with dry {thread[1]['herb_name']},
            herbal {thread[2]['preparation_name']} made with dry {thread[2]['herb_name']},
            on a wooden table,
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''
        print(prompt)
        negative_prompt = ''
        w = 1216
        h = 832
        ratio = 0.9
        # image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=w, height=h, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        img_filepath = f'twitter/featured.jpg'
        image.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

if 1:
    img_w = 768
    img_h = 768
    img = Image.open('twitter/featured.jpg')
    ###
    draw = ImageDraw.Draw(img)
    month = datetime.now().date().month
    day = datetime.now().date().day
    json_article_filepath = f'twitter/data.json'
    json_article = io.json_read(json_article_filepath)
    ailment = json_article['month_list'][month-1]['month_ailments'][day-1]
    text = f'{ailment["answer"]} remedies'
    font_size = 80
    font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font_path = f"assets/fonts/allura/Allura-Regular.ttf"
    font_path = f"assets/fonts/arial/ARIAL.TTF"
    font_path = f"assets/fonts/lustria/Lustria-Regular.ttf"
    font_path = f"assets/fonts/Quicksand/static/Quicksand-Regular.ttf"
    font_path = f"assets/fonts/Quicksand/static/Quicksand-Bold.ttf"
    font_path = f"assets/fonts/helvetica/Helvetica.ttf"
    font = ImageFont.truetype(font_path, font_size)
    ###
    lines = []
    line = ''
    for word in text.split():
        _, _, line_w, line_h = font.getbbox(line)
        _, _, word_w, word_h = font.getbbox(word)
        if line_w + word_w < img_w - 300:
            line += word + ' '
        else:
            lines.append(line.strip())
            line = word + ' '
    if line.strip() != '':
        lines.append(line.strip())
    ###
    rect_h = 192
    draw.rectangle(((0, img_h-rect_h), (img_w, img_h)), fill="#2f3e2f")
    draw.rectangle(((0, img_h-rect_h), (img_w, img_h)), fill=(20, 20, 16))
    draw.rectangle(((0, img_h-rect_h), (img_w, img_h)), fill=(18, 24, 28))
    ###
    y_cur = 0
    y_cur += img_h - rect_h + 24
    line_height = 1.0
    for line in lines:
        line = line.upper()
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, '#ffffff', font=font)
        y_cur += font_size*line_height
    ###
    '''
    logo = Image.open('assets/logo/terrawhisper-logo-round.png').convert('RGBA')
    logo_size = 64
    logo = img_resize(logo, w=logo_size, h=logo_size)
    img.paste(logo, (img_w//2 - logo_size//2, img_h - logo_size - logo_size), logo)
    '''
    ###
    '''
    line = 'terrawhisper.com'
    font_size = 16
    font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((img_w//2 - line_w//2, img_h - font_size - 64), line, '#ffffff', font=font)
    ###
    '''
    ###
    img.save('twitter/featured-final.jpg')
    img.show()

