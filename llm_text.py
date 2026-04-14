import textwrap

from lib import llm

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

running = True
while running:
    val = input('>>')
    if val == 'q': 
        running = False
    else:
        with open('llm-prompt.txt') as f: 
            content = f.read().strip()
            prompt = textwrap.dedent(content).strip()
            prompt = prompt.split('===')[0]
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            print('########################################')
            print(reply)
            print('########################################')
