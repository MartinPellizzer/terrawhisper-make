import os

def gen():
    herbs_folderpath = f'/home/ubuntu/vault/terrawhisper-old/terrawhisper/herbs'
    herbs_filenames = [filename for filename in os.listdir(herbs_folderpath) if os.path.isfile(f'{herbs_folderpath}/{filename}')]
    herbs_slugs = [x.split('.')[0] for x in herbs_filenames]
    print(len(herbs_slugs))
    print(herbs_slugs[0])
    with open('herbs_legacy.csv', 'w', encoding='utf-8') as f:
        for herb_slug in herbs_slugs:
            herb_name_scientific = herb_slug.strip().capitalize().replace('-', ' ')
            f.write(f'{herb_slug}\\{herb_name_scientific}\n')

gen()
