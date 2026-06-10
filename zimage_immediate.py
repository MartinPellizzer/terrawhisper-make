from lib import zimage

def image_gen():
    running = True
    while running:
        val = input('>>')
        if val == 'q': return
        with open('prompts/zimage.txt') as f: content = f.read().strip()
        params, prompt = content.split('---')
        
        output_filepath = f'test.jpg'
        w = 768
        h = 768
        for line in params.split('\n'):
            if line.startswith('w:'):
                w = int(line.replace('w:', '').strip())
            if line.startswith('h:'):
                h = int(line.replace('h:', '').strip())
            if line.startswith('output_filepath:'):
                output_filepath = line.replace('output_filepath:', '').strip()

        prompt = prompt.strip()
        if prompt[-1] == ',': prompt = prompt[:-1]
        print(f'w:{w}')
        print(f'h:{h}')
        print(prompt)
        print()
        # continue
        image = zimage.image_create(
            output_filepath=output_filepath, 
            prompt=prompt, width=w, height=h, seed=-1
        )

image_gen()
