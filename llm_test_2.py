
from lib import llm

model_filepath = '/home/ubuntu/vault-tmp/llm/Qwen3.5-27B-Q4_0.gguf'
model_filepath = ''

import textwrap
prompt = textwrap.dedent(f'''
    test
    /no_think
''').strip()
reply = llm.reply(prompt, model_filepath)
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
