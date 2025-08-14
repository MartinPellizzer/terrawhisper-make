import os
import random
import shutil

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler 

from torchvision import transforms
import matplotlib.pyplot as plt
from transformers import AutoModelForImageSegmentation

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import numpy as np

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import media

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'
pipe = None
bg_model = None

def pipe_init():
    global pipe
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            g.checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

herb_list = data.preparations_popular_100('teas')
if 0:
    for herb in herb_list:
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        herb_name_common = herb_entity['herb_common_names'][0]['answer']
        print(f'''{{'herb_name_scientific': '{herb_name_scientific}', 'herb_name_common': '{herb_name_common}'}},''')
    quit()

'''
herb_list = [
  {"herb_name_scientific":"Matricaria chamomilla","herb_name_common":"Chamomile"},
  {"herb_name_scientific":"Mentha x piperita","herb_name_common":"Peppermint"},
  {"herb_name_scientific":"Lavandula angustifolia","herb_name_common":"Lavender"},
  {"herb_name_scientific":"Echinacea purpurea","herb_name_common":"Echinacea"},
  {"herb_name_scientific":"Allium sativum","herb_name_common":"Garlic"}, {"herb_name_scientific":"Curcuma longa","herb_name_common":"Turmeric"},
  {"herb_name_scientific":"Taraxacum officinale","herb_name_common":"Dandelion"},
  {"herb_name_scientific":"Hypericum perforatum","herb_name_common":"St. John's Wort"},
  {"herb_name_scientific":"Melissa officinalis","herb_name_common":"Lemon Balm"},
  {"herb_name_scientific":"Rosmarinus officinalis","herb_name_common":"Rosemary"},
  {"herb_name_scientific":"Salvia officinalis","herb_name_common":"Sage"},
  {"herb_name_scientific":"Panax ginseng","herb_name_common":"Ginseng"},
  {"herb_name_scientific":"Ginkgo biloba","herb_name_common":"Ginkgo"},
  {"herb_name_scientific":"Valeriana officinalis","herb_name_common":"Valerian"},
  {"herb_name_scientific":"Serenoa repens","herb_name_common":"Saw Palmetto"},
  {"herb_name_scientific":"Hydrastis canadensis","herb_name_common":"Goldenseal"},
  {"herb_name_scientific":"Silybum marianum","herb_name_common":"Milk Thistle"},
  {"herb_name_scientific":"Chrysanthemum parthenium","herb_name_common":"Feverfew"},
  {"herb_name_scientific":"Mentha pulegium","herb_name_common":"Pennyroyal"},
  {"herb_name_scientific":"Potentilla reptans","herb_name_common":"Cinquefoil"},
  {"herb_name_scientific":"Aquilegia vulgaris","herb_name_common":"Columbine"},
  {"herb_name_scientific":"Digitalis purpurea","herb_name_common":"Foxglove"},
  {"herb_name_scientific":"Solidago virgaurea","herb_name_common":"Goldenrod"},
  {"herb_name_scientific":"Alchemilla vulgaris","herb_name_common":"Lady's Mantle"},
  {"herb_name_scientific":"Levisticum officinale","herb_name_common":"Lovage"},
  {"herb_name_scientific":"Papaver rhoeas","herb_name_common":"Common Poppy"},
  {"herb_name_scientific":"Primula vulgaris","herb_name_common":"Primrose"},
  {"herb_name_scientific":"Verbena officinalis","herb_name_common":"Vervain"},
  {"herb_name_scientific":"Pyrola minor","herb_name_common":"Wintergreen"},
  {"herb_name_scientific":"Galium odoratum","herb_name_common":"Sweet Woodruff"},
  {"herb_name_scientific":"Achillea millefolium","herb_name_common":"Yarrow"},
  {"herb_name_scientific":"Aloe vera","herb_name_common":"Aloe Vera"},
  {"herb_name_scientific":"Withania somnifera","herb_name_common":"Ashwagandha"},
  {"herb_name_scientific":"Agastache foeniculum","herb_name_common":"Anise Hyssop"},
  {"herb_name_scientific":"Arnica montana","herb_name_common":"Arnica"},
  {"herb_name_scientific":"Platycodon grandiflorus","herb_name_common":"Balloon Flower"},
  {"herb_name_scientific":"Lippia dulcis","herb_name_common":"Aztec Sweet Herb"},
  {"herb_name_scientific":"Ocimum basilicum","herb_name_common":"Basil"},
  {"herb_name_scientific":"Ocimum sanctum","herb_name_common":"Holy Basil (Tulsi)"},
  {"herb_name_scientific":"Foeniculum vulgare","herb_name_common":"Fennel"},
  {"herb_name_scientific":"Trigonella foenum-graecum","herb_name_common":"Fenugreek"},
  {"herb_name_scientific":"Borago officinalis","herb_name_common":"Borage"},
  {"herb_name_scientific":"Sambucus nigra","herb_name_common":"Elderberry"},
  {"herb_name_scientific":"Glycyrrhiza glabra","herb_name_common":"Licorice"},
  {"herb_name_scientific":"Ferula foetida","herb_name_common":"Asafoetida"},
  {"herb_name_scientific":"Hamamelis virginiana","herb_name_common":"Witch Hazel"},
  {"herb_name_scientific":"Symphytum officinale","herb_name_common":"Comfrey"},
  {"herb_name_scientific":"Syzygium aromaticum","herb_name_common":"Clove"},
  {"herb_name_scientific":"Anethum graveolens","herb_name_common":"Dill"},
  {"herb_name_scientific":"Tragopogon porrifolius","herb_name_common":"Salsify"},
  {"herb_name_scientific":"Hibiscus sabdariffa","herb_name_common":"Sorrel (Hibiscus)"},
  {"herb_name_scientific":"Prunella vulgaris","herb_name_common":"Self-heal"},
  {"herb_name_scientific":"Salvia fruticosa","herb_name_common":"Mountain Sage"},
  {"herb_name_scientific":"Peumus boldus","herb_name_common":"Boldo"},
  {"herb_name_scientific":"Anethum graveolens","herb_name_common":"Dill"},
  {"herb_name_scientific":"Borago officinalis","herb_name_common":"Borage"},
  {"herb_name_scientific":"Cinnamomum verum","herb_name_common":"Cinnamon"},
  {"herb_name_scientific":"Capsicum annum","herb_name_common":"Cayenne Pepper"},
  {"herb_name_scientific":"Mentha arvensis","herb_name_common":"Field Mint"},
  {"herb_name_scientific":"Salvia sclarea","herb_name_common":"Clary Sage"},
  {"herb_name_scientific":"Castanea sativa","herb_name_common":"Chestnut"},
  {"herb_name_scientific":"Plantago major","herb_name_common":"Plantain"},
  {"herb_name_scientific":"Calendula officinalis","herb_name_common":"Marigold"},
  {"herb_name_scientific":"Capsella bursa-pastoris","herb_name_common":"Shepherd's Purse"},
  {"herb_name_scientific":"Centella asiatica","herb_name_common":"Gotu Kola"},
  {"herb_name_scientific":"Eucalyptus globulus","herb_name_common":"Eucalyptus"},
  {"herb_name_scientific":"Salix alba","herb_name_common":"White Willow"},
  {"herb_name_scientific":"Inula helenium","herb_name_common":"Elecampane"},
  {"herb_name_scientific":"Gentiana lutea","herb_name_common":"Gentian"},
  {"herb_name_scientific":"Taraxacum officinale","herb_name_common":"Dandelion"},
  {"herb_name_scientific":"Capsicum frutescens","herb_name_common":"Tabasco Pepper"},
  {"herb_name_scientific":"Taraxacum laevigatum","herb_name_common":"Blue Dandelion"},
  {"herb_name_scientific":"Lycopus virginicus","herb_name_common":"Bugleweed"},
  {"herb_name_scientific":"Agrimonia eupatoria","herb_name_common":"Agrimony"},
  {"herb_name_scientific":"Adiantum capillus-veneris","herb_name_common":"Maidenhair Fern"},
  {"herb_name_scientific":"Achillea ptarmica","herb_name_common":"Sneezewort"},
  {"herb_name_scientific":"Tanacetum balsamita","herb_name_common":"Alecost"},
  {"herb_name_scientific":"Ocimum × citriodorum","herb_name_common":"Lemon Basil"},
  {"herb_name_scientific":"Syzygium polyanthum","herb_name_common":"Indonesian Bay Leaf"},
  {"herb_name_scientific":"Pimenta racemosa","herb_name_common":"West Indian Bay Leaf"},
  {"herb_name_scientific":"Litsea glaucescens","herb_name_common":"Mexican Bay Leaf"},
  {"herb_name_scientific":"Hypericum perforatum","herb_name_common":"St. John's Wort"},
  {"herb_name_scientific":"Trigonella caerulea","herb_name_common":"Blue Fenugreek"},
  {"herb_name_scientific":"Boesenbergia rotunda","herb_name_common":"Fingerroot"},
  {"herb_name_scientific":"Houttuynia cordata","herb_name_common":"Fish Mint"},
  {"herb_name_scientific":"Dysphania ambrosioides","herb_name_common":"Epazote"},
  {"herb_name_scientific":"Borago officinalis","herb_name_common":"Borage"},
  {"herb_name_scientific":"Ocimum gratissimum","herb_name_common":"African Basil"},
  {"herb_name_scientific":"Ocimum basilicum var. thyrsiflora","herb_name_common":"Thai Basil"},
  {"herb_name_scientific":"Laurus nobilis","herb_name_common":"Bay Leaf"},
  {"herb_name_scientific":"Peumus boldus","herb_name_common":"Boldo"},
  {"herb_name_scientific": "Rheum palmatum", "herb_name_common": "Chinese Rhubarb"},
  {"herb_name_scientific": "Cnicus benedictus", "herb_name_common": "Blessed Thistle"},
]
'''

herb_list = [
    {'herb_name_scientific': 'Zingiber officinale', 'herb_name_common': 'ginger'},
    {'herb_name_scientific': 'Glycyrrhiza glabra', 'herb_name_common': 'licorice'},
    {'herb_name_scientific': 'Ginkgo biloba', 'herb_name_common': 'ginkgo'},
    {'herb_name_scientific': 'Lavandula angustifolia', 'herb_name_common': 'lavender'},
    {'herb_name_scientific': 'Echinacea purpurea', 'herb_name_common': 'coneflower'},
    {'herb_name_scientific': 'Curcuma longa', 'herb_name_common': 'turmeric'},
    {'herb_name_scientific': 'Rosmarinus officinalis', 'herb_name_common': 'rosemary'},
    {'herb_name_scientific': 'Eucalyptus globulus', 'herb_name_common': 'blue gum'},
    {'herb_name_scientific': 'Silybum marianum', 'herb_name_common': 'milk thistle'},
    {'herb_name_scientific': 'Melissa officinalis', 'herb_name_common': 'lemon balm'},
    {'herb_name_scientific': 'Cinchona officinalis', 'herb_name_common': 'quinine'},
    {'herb_name_scientific': 'Achillea millefolium', 'herb_name_common': 'yarrow'},
    {'herb_name_scientific': 'Valeriana officinalis', 'herb_name_common': 'valerian'},
    {'herb_name_scientific': 'Sambucus nigra', 'herb_name_common': 'elderberry'},
    {'herb_name_scientific': 'Taraxacum officinale', 'herb_name_common': 'dandelion'},
    {'herb_name_scientific': 'Foeniculum vulgare', 'herb_name_common': 'fennel'},
    {'herb_name_scientific': 'Urtica dioica', 'herb_name_common': 'nettle'},
    {'herb_name_scientific': 'Hypericum perforatum', 'herb_name_common': 'st. john\'s wort'},
    {'herb_name_scientific': 'Mentha x piperita', 'herb_name_common': 'peppermint'},
    {'herb_name_scientific': 'Thymus vulgaris', 'herb_name_common': 'thyme'},
    {'herb_name_scientific': 'Calendula officinalis', 'herb_name_common': 'marigold'},
    {'herb_name_scientific': 'Salvia officinalis', 'herb_name_common': 'sage'},
    {'herb_name_scientific': 'Panax ginseng', 'herb_name_common': 'ginseng'},
    {'herb_name_scientific': 'Avena sativa', 'herb_name_common': 'oat'},
    {'herb_name_scientific': 'Passiflora incarnata', 'herb_name_common': 'passionflower'},
    {'herb_name_scientific': 'Astragalus membranaceus', 'herb_name_common': 'milk vetch'},
    {'herb_name_scientific': 'Cinnamomum verum', 'herb_name_common': 'cinnamon'},
    {'herb_name_scientific': 'Melaleuca alternifolia', 'herb_name_common': 'tea tree'},
    {'herb_name_scientific': 'Equisetum arvense', 'herb_name_common': 'horsetail'},
    {'herb_name_scientific': 'Cymbopogon citratus', 'herb_name_common': 'lemon grass'},
    {'herb_name_scientific': 'Camellia sinensis', 'herb_name_common': 'tea plant'},
    {'herb_name_scientific': 'Artemisia absinthium', 'herb_name_common': 'wormwood'},
    {'herb_name_scientific': 'Paeonia lactiflora', 'herb_name_common': 'peony'},
    {'herb_name_scientific': 'Angelica sinensis', 'herb_name_common': 'dong quai'},
    {'herb_name_scientific': 'Schisandra chinensis', 'herb_name_common': 'magnolia vine'},
    {'herb_name_scientific': 'Vitex agnus-castus', 'herb_name_common': 'chaste tree'},
    {'herb_name_scientific': 'Origanum vulgare', 'herb_name_common': 'oregano'},
    {'herb_name_scientific': 'Aloe vera', 'herb_name_common': 'aloe vera'},
    {'herb_name_scientific': 'Withania somnifera', 'herb_name_common': 'ashwagandha'},
    {'herb_name_scientific': 'Cassia auriculata', 'herb_name_common': 'tanner\'s cassia'},
    {"herb_name_scientific": "Prunella vulgaris", "herb_name_common": "self-heal"},
    {'herb_name_scientific': 'Symphytum officinale', 'herb_name_common': 'comfrey'},
    {'herb_name_scientific': 'Arnica montana', 'herb_name_common': 'arnica'},
    {'herb_name_scientific': 'Cimicifuga racemosa', 'herb_name_common': 'black cohosh'},
    {"herb_name_scientific": "Harpagophytum procumbens", "herb_name_common": "devil\'s claw"},
    {'herb_name_scientific': 'Plantago lanceolata', 'herb_name_common': 'buckhorn'},
    {'herb_name_scientific': 'Centella asiatica', 'herb_name_common': 'gotu kola'},
    {'herb_name_scientific': 'Euphrasia officinalis', 'herb_name_common': 'eyebright'},
    {'herb_name_scientific': 'Hydrastis canadensis', 'herb_name_common': 'goldenseal'},
    {'herb_name_scientific': 'Matricaria chamomilla', 'herb_name_common': 'chamomile'},
    {'herb_name_scientific': 'Cynara scolymus', 'herb_name_common': 'artichoke'},
    {'herb_name_scientific': 'Verbascum thapsus', 'herb_name_common': 'mullein'},
    {'herb_name_scientific': 'Bacopa monnieri', 'herb_name_common': 'hyssop'},
    {'herb_name_scientific': 'Angelica archangelica', 'herb_name_common': 'wild celery'},
    {'herb_name_scientific': 'Juniperus communis', 'herb_name_common': 'juniper'},
    {'herb_name_scientific': 'Vaccinium myrtillus', 'herb_name_common': 'bilberry'},
    {'herb_name_scientific': 'Trifolium pratense', 'herb_name_common': 'red clover'},
    {'herb_name_scientific': 'Saponaria officinalis', 'herb_name_common': 'soapwort'},
    {'herb_name_scientific': 'Ruscus aculeatus', 'herb_name_common': 'butcher\'s broom'},
    {'herb_name_scientific': 'Hamamelis virginiana', 'herb_name_common': 'witch hazel'},
    {'herb_name_scientific': 'Althaea officinalis', 'herb_name_common': 'marshmallow'},
    {'herb_name_scientific': 'Cuminum cyminum', 'herb_name_common': 'cumin'},
    {'herb_name_scientific': 'Crataegus monogyna', 'herb_name_common': 'hawthorn'},
    {'herb_name_scientific': 'Zanthoxylum bungeanum', 'herb_name_common': 'prickly ash'},
    {'herb_name_scientific': 'Berberis vulgaris', 'herb_name_common': 'barberry'},
    {'herb_name_scientific': 'Tribulus terrestris', 'herb_name_common': 'puncture vine'},
    {'herb_name_scientific': 'Serenoa repens', 'herb_name_common': 'saw palmetto'},
    {'herb_name_scientific': 'Rheum officinale', 'herb_name_common': 'rhubarb'},
    {'herb_name_scientific': 'Boswellia serrata', 'herb_name_common': 'frankincense'},
    {'herb_name_scientific': 'Arctium lappa', 'herb_name_common': 'burdock'},
    {'herb_name_scientific': 'Scutellaria baicalensis', 'herb_name_common': 'skullcap'},
    {'herb_name_scientific': 'Vitis vinifera', 'herb_name_common': 'grapevine'},
    {'herb_name_scientific': 'Rauvolfia serpentina', 'herb_name_common': 'snakeroot'},
    {'herb_name_scientific': 'Vaccinium macrocarpon', 'herb_name_common': 'cranberry'},
    {'herb_name_scientific': 'Coriandrum sativum', 'herb_name_common': 'cilantro'},
    {'herb_name_scientific': 'Pimpinella anisum', 'herb_name_common': 'anise'},
    {'herb_name_scientific': 'Peumus boldus', 'herb_name_common': 'boldo'},
    {'herb_name_scientific': 'Elettaria cardamomum', 'herb_name_common': 'cardamom'},
    {'herb_name_scientific': 'Gymnema sylvestre', 'herb_name_common': 'gymnema'},
    {'herb_name_scientific': 'Citrus reticulata', 'herb_name_common': 'mandarin'},
    {'herb_name_scientific': 'Cichorium intybus', 'herb_name_common': 'chicory'},
    {'herb_name_scientific': 'Terminalia chebula', 'herb_name_common': 'myrobalan'},
    {'herb_name_scientific': 'Ocimum basilicum', 'herb_name_common': 'basil'},
    {'herb_name_scientific': 'Humulus lupulus', 'herb_name_common': 'hops'},
    {'herb_name_scientific': 'Anethum graveolens', 'herb_name_common': 'dill'},
    {'herb_name_scientific': 'Ephedra sinica', 'herb_name_common': 'ma huang'},
    {'herb_name_scientific': 'Rhodiola rosea', 'herb_name_common': 'roseroot'},
    {'herb_name_scientific': 'Ulmus rubra', 'herb_name_common': 'slippery elm'},
    {'herb_name_scientific': 'Ligusticum wallichii', 'herb_name_common': 'chuan xiong'},
    {"herb_name_scientific": "Aspalathus linearis", "herb_name_common": "rooibos"},
    {'herb_name_scientific': 'Digitalis purpurea', 'herb_name_common': 'foxglove'},
    {'herb_name_scientific': 'Hyptis suaveolens', 'herb_name_common': 'pignut'},
    {'herb_name_scientific': 'Allium sativum', 'herb_name_common': 'garlic'},
    {'herb_name_scientific': 'Capsicum annuum', 'herb_name_common': 'cayenne'},
    {"herb_name_scientific": "Commiphora myrrha", "herb_name_common": "myrrh"},
    {"herb_name_scientific": "Chrysanthemum parthenium", "herb_name_common": "feverfew"},
    {"herb_name_scientific": "Papaver rhoeas", "herb_name_common": "poppy"},
    {"herb_name_scientific": "Primula vulgaris", "herb_name_common": "primrose"},
    {"herb_name_scientific": "Verbena officinalis", "herb_name_common": "vervain"},
    {"herb_name_scientific": "Uncaria tomentosa", "herb_name_common": "cat's claw"},
]
    # {'herb_name_scientific': 'Eurycoma longifolia', 'herb_name_common': 'tongkat ali'},
# herb_list = sorted(herb_list, key=lambda x: x['herb_name_common'].lower(), reverse=False)
for herb in herb_list:
    print(herb['herb_name_common'].title())
quit()

def ai_img_herb(herb_i, herb_name='scientific'):
    herb = herb_list[herb_i]
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = herb['herb_name_common']
    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
    image_folderpath = f'assets/shop/labels/herbs'
    try: os.makedirs(image_folderpath)
    except: pass
    image_filepath = f'{image_folderpath}/{herb_i}-{herb_slug}.jpg'
    if herb_name == 'common':
        herb_name_prompt = herb_name_common
    else:
        herb_name_prompt = herb_name_scientific
    positive_prompt = f'''
        {herb_name_prompt}, line drawing, monochrome,
        paper, antique, old, 
        victorian, vintage, rustic, elegant,
        light background,
        high resolution
    '''
    negative_prompt = f'''
        text, watermark 
    '''
    img_w = 832
    img_h = 1216
    images_filepaths = []
    pipe_init()
    image = pipe(
        prompt=positive_prompt, 
        negative_prompt=negative_prompt, 
        width=img_w, 
        height=img_h, 
        num_inference_steps=25, 
        guidance_scale=6.0
    ).images[0]
    image.save(image_filepath)
    # image.show()

def ai_img_herbs():
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        image_filepath = f'assets/shop/labels/valid/{herb_slug}.jpg'
        ##
        img_tmp_filepath = f'assets/shop/labels/tmp/{herb_slug}.jpg'
        img_valid_filepath = f'assets/shop/labels/valid/{herb_slug}.jpg'
        if os.path.exists(img_valid_filepath):
            continue
        positive_prompt = f'''
            {herb_name_scientific}, line drawing, grayscale, monochrome,
            paper, antique, old, apothecary,
            victorian, vintage, rustic, elegant,
            light background,
            high resolution
        '''
        negative_prompt = f'''
            text, watermark 
        '''
        img_w = 832
        img_h = 1216
        images_filepaths = []
        pipe_init()
        image = pipe(
            prompt=positive_prompt, 
            negative_prompt=negative_prompt, 
            width=img_w, 
            height=img_h, 
            num_inference_steps=25, 
            guidance_scale=6.0
        ).images[0]
        image.save(image_filepath)
        # image.show()

def ai_img_herbs_100():
    image_folderpath = f'assets/shop/labels/herbs'
    try: os.makedirs(image_folderpath)
    except: pass
    image_tmp_folderpath = f'assets/shop/labels/herbs/tmp'
    try: os.makedirs(image_tmp_folderpath)
    except: pass
    image_valid_folderpath = f'assets/shop/labels/herbs/valid'
    try: os.makedirs(image_valid_folderpath)
    except: pass
    for herb_i, herb in enumerate(herb_list):
        print(herb_i)
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        ###
        img_tmp_filepath = f'{image_tmp_folderpath}/{herb_i}-{herb_slug}.jpg'
        img_valid_filepath = f'{image_valid_folderpath}/{herb_i}-{herb_slug}.jpg'
        if os.path.exists(img_valid_filepath): continue
        positive_prompt = f'''
            {herb_name_scientific}, line drawing, monochrome,
            paper, antique, old, 
            victorian, vintage, rustic, elegant,
            light background,
            high resolution
        '''
        negative_prompt = f'''
            text, watermark 
        '''
        img_w = 832
        img_h = 1216
        images_filepaths = []
        pipe_init()
        image = pipe(
            prompt=positive_prompt, 
            negative_prompt=negative_prompt, 
            width=img_w, 
            height=img_h, 
            num_inference_steps=25, 
            guidance_scale=6.0
        ).images[0]
        image.save(img_tmp_filepath)
        # image.show()

def ai_img_herbs_desaturate():
    input_folderpath = f'assets/shop/labels/alpha'
    output_folderpath = f'assets/shop/labels/desaturated'
    for herb_i, herb in enumerate(herb_list):
        image_filepath = f'{output_folderpath}/{herb}.png'
        image = Image.open(image_filepath)
        converter = ImageEnhance.Color(image)
        image = converter.enhance(0)
        image.save(image_filepath)

def ai_img_herbs_100_alpha():
    input_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/valid'
    try: os.makedirs(input_folderpath)
    except: pass
    output_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/alpha'
    try: os.makedirs(output_folderpath)
    except: pass
    for herb_i, herb in enumerate(herb_list):
        # herb_slug = herb['herb_slug']
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        image_filepath = f'{input_folderpath}/{herb_i}-{herb_slug}.jpg'
        image = Image.open(image_filepath)
        global bg_model
        if not bg_model:
            bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
        torch.set_float32_matmul_precision(['high', 'highest'][0])
        bg_model.to('cuda')
        bg_model.eval()
        # Data settings
        image_size = (832, 1216)
        transform_image = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        input_images = transform_image(image).unsqueeze(0).to('cuda')
        # Prediction
        with torch.no_grad():
            preds = bg_model(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        image.putalpha(mask)
        image_filepath = f'{output_folderpath}/{herb_i}-{herb_slug}.png'
        image.save(image_filepath)

def ai_img_herbs_alpha():
    input_folderpath = f'assets/shop/labels/valid'
    output_folderpath = f'assets/shop/labels/alpha'
    for herb_i, herb in enumerate(herb_list):
        image_filepath = f'{input_folderpath}/{herb}.jpg'
        image = Image.open(image_filepath)
        global bg_model
        if not bg_model:
            bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
        torch.set_float32_matmul_precision(['high', 'highest'][0])
        bg_model.to('cuda')
        bg_model.eval()
        # Data settings
        image_size = (832, 1216)
        transform_image = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        input_images = transform_image(image).unsqueeze(0).to('cuda')
        # Prediction
        with torch.no_grad():
            preds = bg_model(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        image.putalpha(mask)
        image_filepath = f'{output_folderpath}/{herb}.png'
        image.save(image_filepath)

def ai_img_herb_alpha(herb_i):
    input_folderpath = f'assets/shop/labels/valid'
    output_folderpath = f'assets/shop/labels/alpha'
    herb = herb_list[herb_i]
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = herb['herb_name_common']
    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
    image_filepath = f'{input_folderpath}/{herb_i}-{herb_slug}.jpg'
    image = Image.open(image_filepath)
    global bg_model
    if not bg_model:
        bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    torch.set_float32_matmul_precision(['high', 'highest'][0])
    bg_model.to('cuda')
    bg_model.eval()
    # Data settings
    image_size = (832, 1216)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    input_images = transform_image(image).unsqueeze(0).to('cuda')
    # Prediction
    with torch.no_grad():
        preds = bg_model(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)
    image_filepath = f'{output_folderpath}/{herb_i}-{herb_slug}.png'
    image.save(image_filepath)

def labels_images():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_2x3_w = 2 * dpi
    label_2x3_h = 3 * dpi
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'assets/shop/labels/final/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_2x3_w, label_2x3_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((600, 900))
        label.paste(background, (0, 0))
        ##
        herb_y = 60
        herb_size_mul = 0.80
        herb_w = int(600 * herb_size_mul)
        herb_h = int(900 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = herb_image.resize((herb_w, herb_h))
        label.paste(herb_image, (int(label_2x3_w//2 - herb_w//2), int(label_2x3_h//2 - herb_h//2) + herb_y), herb_image)
        ##
        line = herb_name_common
        font_size = 56
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_2x3_w//2 - line_w//2, 60), line, '#423626', font=font)
        ##
        line = herb_name_scientific
        font_size = 18
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        # _, _, line_w, line_h = font.getbbox(line)
        # draw.text((label_2x3_w//2 - line_w//2, 130), line, '#423626', font=font)
        letter_spacing = 5
        x_cur = 0
        for char_i, char in enumerate(line):
            _, _, char_w, char_h = font.getbbox(char)
            x_cur += char_w + letter_spacing
        line_w = x_cur
        x_cur = 0
        for char_i, char in enumerate(line):
            _, _, char_w, char_h = font.getbbox(char)
            draw.text((label_2x3_w//2 - line_w//2 + x_cur + letter_spacing, 130), char, '#423626', font=font)
            x_cur += char_w + letter_spacing
        ##
        label = label.convert('RGB')
        label.save(label_filepath, format='JPEG', quality=30)
        # label.show()

def label_image(herb_i):
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_2x3_w = 2 * dpi
    label_2x3_h = 3 * dpi
    herb = herb_list[herb_i]
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = herb['herb_name_common']
    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
    label_filepath = f'assets/shop/labels/final/{herb_i}-{herb_slug}.jpg'
    label = Image.new(mode="RGBA", size=(label_2x3_w, label_2x3_h), color='#ffffff')
    draw = ImageDraw.Draw(label)
    ##
    background = Image.open(background_filepath)
    background = background.resize((600, 900))
    label.paste(background, (0, 0))
    ##
    herb_y = 60
    herb_size_mul = 0.80
    herb_w = int(600 * herb_size_mul)
    herb_h = int(900 * herb_size_mul)
    herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
    herb_image = Image.open(herb_filepath)
    herb_image = herb_image.resize((herb_w, herb_h))
    label.paste(herb_image, (int(label_2x3_w//2 - herb_w//2), int(label_2x3_h//2 - herb_h//2) + herb_y), herb_image)
    ##
    line = herb_name_common
    font_size = 56
    font_family, font_weight = 'cinzel-decorative', 'regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((label_2x3_w//2 - line_w//2, 60), line, '#423626', font=font)
    ##
    line = herb_name_scientific
    font_size = 18
    font_family, font_weight = 'vollkorn-sc', 'regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((label_2x3_w//2 - line_w//2, 130), line, '#423626', font=font)
    ##
    label = label.convert('RGB')
    label.save(label_filepath, format='JPEG', quality=30)
    # label.show()

'''
labels_images()
'''
# ai_img_herbs()
# ai_img_herbs_alpha()

while False:
    herb_i = int(input(f'insert number >> '))
    ai_img_herb(herb_i, herb_name='scientific')
    # ai_img_herb(herb_i, herb_name='common')
    ai_img_herb_alpha(herb_i)
    label_image(herb_i)

# ai_img_herbs_desaturate()
# ai_img_herbs_alpha()
# labels_images()
def sheet_labels():
    a4_w = 2480
    a4_h = 3508
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    row_num = 4
    col_num = 4
    img_i = 0
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (600*col_i, 900*row_i))
                img_i += 1
    # sheet.show()


def sheet_rectangles_1x2_625():
    a4_w = 2480
    a4_h = 3508
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    row_num = 4
    col_num = 5
    gap = 30
    mx = 400
    my = 800
    img_i = 0
    label_w = int(1 * 300)
    label_h = int(2.625 * 300)
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-1x2_625/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/1x2.625/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/1x2.625-1.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_rectangles_2x3():
    a4_w = 2480
    a4_h = 3508
    col_num = 3
    row_num = 2
    gap = 30
    mx = 300
    my = 600
    img_i = 0
    label_w = int(2 * 300)
    label_h = int(3 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-2x3/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/2x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x3-1.jpg'
    sheet.save(output_filepath)
    ###
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-2x3/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/2x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x3-2.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_rectangles_3x4():
    a4_w = 2480
    a4_h = 3508
    col_num = 2
    row_num = 2
    gap = 30
    mx = 300
    my = 600
    img_i = 0
    label_w = int(3 * 300)
    label_h = int(4 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-3x4/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-1.jpg'
    sheet.save(output_filepath)
    ###
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-3x4/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-2.jpg'
    sheet.save(output_filepath)
    ###
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-rectangle-3x4/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/rectangle/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-3.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def labels_rectangle_1x2_625():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(1 * dpi)
    label_h = int(2.625 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'assets/shop/labels/final-rectangle-1x2_625/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += 100
        font_size = 32
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = []
        line = ''
        for word in herb_name_common.split():
            _, _, line_w, line_h = font.getbbox(line)
            _, _, word_w, word_h = font.getbbox(word)
            if line_w + word_w > 200:
                if line.strip() == '':
                    line += word + ' '
                else:
                    lines.append(line.strip())
                    line = word + ' '
            else:
                line += word + ' '
        if line.strip() != '':
            lines.append(line.strip())
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
            y_cur += 50
        ##
        line = herb_name_scientific
        font_size = 18
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = line.split()
        for line in lines:
            letter_spacing = 5
            x_cur = 0
            for char_i, char in enumerate(line):
                _, _, char_w, char_h = font.getbbox(char)
                x_cur += char_w + letter_spacing
            line_w = x_cur
            x_cur = 0
            for char_i, char in enumerate(line):
                _, _, char_w, char_h = font.getbbox(char)
                draw.text((label_w//2 - line_w//2 + x_cur + letter_spacing, y_cur), char, '#423626', font=font)
                x_cur += char_w + letter_spacing
            y_cur += 25
        ##
        herb_y = 100
        herb_size_mul = 0.35
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/rectangle/1x2.625'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_rectangle_2x3():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(3 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'assets/shop/labels/final-rectangle-2x3/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += 100
        line = herb_name_common
        font_size = 56
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += 80
        ##
        line = herb_name_scientific
        font_size = 32
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = 100
        herb_size_mul = 0.50
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/rectangle/2x3'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_rectangle_3x4():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(4 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'assets/shop/labels/final-rectangle-3x4/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += 100
        line = herb_name_common
        font_size = 64
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += 80
        ##
        line = herb_name_scientific
        font_size = 32
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = 100
        herb_size_mul = 0.75
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/rectangle/3x4'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def assets_rectangle_1x2_625():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(1 * dpi)
    label_h = int(2.625 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/rectangle/1x2.625'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_rectangle_2x3():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(3 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/rectangle/2x3'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_rectangle_3x4():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(4 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/rectangle/3x4'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def labels_square_1_5x1_5():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(1.5 * dpi)
    label_h = int(1.5 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'assets/shop/labels/final-square-1_5x1_5/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += 30
        line = herb_name_common
        font_size = 40
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += 50
        ##
        line = herb_name_scientific
        font_size = 24
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = 50
        herb_size_mul = 0.25
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/square/1.5x1.5'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_square_2x2():
    label_folderpath = f'assets/shop/labels/final-square-2x2'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 56
    herb_name_scientific_size = 24
    herb_name_common_y = 40
    herb_name_scientific_y = 70
    herb_image_size = 0.35
    herb_image_y = 60
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(2 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += herb_name_scientific_y
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/square/2x2'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_square_3x3():
    label_folderpath = f'assets/shop/labels/final-square-3x3'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 64
    herb_name_common_y = 60
    herb_name_scientific_size = 32
    herb_name_scientific_y = 80
    herb_image_size = 0.50
    herb_image_y = 70
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(3 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += herb_name_scientific_y
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/square/3x3'
        ### mask
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def sheet_square_1_5x1_5():
    a4_w = 2480
    a4_h = 3508
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    row_num = 4
    col_num = 3
    gap = 30
    mx = 500
    my = 800
    img_i = 0
    label_w = int(1.5 * 300)
    label_h = int(1.5 * 300)
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-square-1_5x1_5/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/square/1.5x1.5/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/1.5x1.5-1.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_square_2x2():
    a4_w = 2480
    a4_h = 3508
    col_num = 3
    row_num = 4
    gap = 30
    mx = 300
    my = 600
    img_i = 0
    label_w = int(2 * 300)
    label_h = int(2 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-square-2x2/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/square/2x2/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x2-1.jpg'
    sheet.save(output_filepath)
    ###
    # sheet.show()

def sheet_square_3x3():
    a4_w = 2480
    a4_h = 3508
    col_num = 2
    row_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(3 * 300)
    label_h = int(3 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-square-3x3/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/square/3x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x3-1.jpg'
    sheet.save(output_filepath)
    ###
    mx = 300
    my = 600
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                image_filepath = f'assets/shop/labels/final-square-3x3/{img_i}-{herb_slug}.jpg'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my))
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/square/3x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x3-2.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def assets_square_1_5x1_5():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(1.5 * dpi)
    label_h = int(1.5 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/square/1.5x1.5'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_square_2x2():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(2 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/square/2x2'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_square_3x3():
    background_filepath = f'assets/shop/labels/rectangle-vertical.jpg'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(3 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/square/3x3'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def labels_round_1x1():
    label_folderpath = f'assets/shop/labels/final-round-1x1'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 20
    herb_name_common_x = 50
    herb_name_scientific_size = 14
    herb_name_scientific_x = 220
    herb_image_size = 0.15
    herb_image_y = 0
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(1 * dpi)
    label_h = int(1 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_common_x, label_h//2 - text_image_h//2), text_image)
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_scientific_x, label_h//2 - text_image_h//2), text_image)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/round/1x1'
        ### mask
        label = label.convert('RGBA')
        '''
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        '''
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_round_2x2():
    label_folderpath = f'assets/shop/labels/final-round-2x2'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 40
    herb_name_common_x = 100
    herb_name_scientific_size = 24
    herb_name_scientific_x = 440
    herb_image_size = 0.30
    herb_image_y = 0
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(2 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_common_x, label_h//2 - text_image_h//2), text_image)
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_scientific_x, label_h//2 - text_image_h//2), text_image)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/round/2x2'
        ### mask
        label = label.convert('RGBA')
        '''
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        '''
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_round_3x3():
    label_folderpath = f'assets/shop/labels/final-round-3x3'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 60
    herb_name_common_x = 150
    herb_name_scientific_size = 36
    herb_name_scientific_x = 660
    herb_image_size = 0.45
    herb_image_y = 0
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(3 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_common_x, label_h//2 - text_image_h//2), text_image)
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        text_image = Image.new('RGBA', (line_w, line_h))
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), line, '#423626', font=font)
        text_image = text_image.rotate(90, expand=1)
        text_image_w, text_image_h = text_image.size
        label.paste(text_image, (herb_name_scientific_x, label_h//2 - text_image_h//2), text_image)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/round/3x3'
        ### mask
        label = label.convert('RGBA')
        '''
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        '''
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def sheet_round_1x1():
    a4_w = 2480
    a4_h = 3508
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    row_num = 3
    col_num = 4
    gap = 30
    mx = 600
    my = 1200
    img_i = 0
    label_w = int(1 * 300)
    label_h = int(1 * 300)
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-round-1x1/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/round/1x1/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/round/1x1/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/1x1-1.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_round_2x2():
    a4_w = 2480
    a4_h = 3508
    col_num = 3
    row_num = 4
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(2 * 300)
    label_h = int(2 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-round-2x2/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/round/2x2/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/round/2x2/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x2-1.jpg'
    sheet.save(output_filepath)
    ###
    # sheet.show()

def sheet_round_3x3():
    a4_w = 2480
    a4_h = 3508
    col_num = 2
    row_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(3 * 300)
    label_h = int(3 * 300)
    output_folderpath = f'assets/shop/labels/public/vintage/round/3x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-round-3x3/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/round/3x3/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_filepath = f'{output_folderpath}/3x3-1.jpg'
    sheet.save(output_filepath)
    ###
    my = 600
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-round-3x3/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/round/3x3/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_filepath = f'{output_folderpath}/3x3-2.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def assets_round_1x1():
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(1 * dpi)
    label_h = int(1 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/round/1x1'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_round_2x2():
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(2 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/round/2x2'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_round_3x3():
    background_filepath = f'assets/shop/labels/round.png'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(3 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/round/3x3'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0, 0), (label_w, label_h)), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

# labels_rectangle_1x2_625()
# label_rectangle_1x2_625_blank()

def labels_oval_1_5x2_5():
    label_folderpath = f'assets/shop/labels/final-oval-1_5x2_5'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 24
    herb_name_common_y = 120
    herb_name_scientific_size = 18
    herb_name_scientific_y = 40
    herb_image_size = 0.35
    herb_image_y = 50
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(1.5 * dpi)
    label_h = int(2.5 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += herb_name_scientific_y
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/oval/1.5x2.5'
        ### mask
        label = label.convert('RGBA')
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.02)), (label_w-int(label_w*0.05), label_h-int(label_h*0.02))), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_oval_2x3():
    label_folderpath = f'assets/shop/labels/final-oval-2x3'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 36
    herb_name_common_y = 160
    herb_name_scientific_size = 24
    herb_name_scientific_y = 60
    herb_image_size = 0.40
    herb_image_y = 60
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(3 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += herb_name_scientific_y
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/oval/2x3'
        ### mask
        label = label.convert('RGBA')
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.02)), (label_w-int(label_w*0.05), label_h-int(label_h*0.02))), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_oval_3x4():
    label_folderpath = f'assets/shop/labels/final-oval-3x4'
    try: os.makedirs(label_folderpath)
    except: pass
    herb_name_common_size = 48
    herb_name_common_y = 200
    herb_name_scientific_size = 36
    herb_name_scientific_y = 70
    herb_image_size = 0.55
    herb_image_y = 80
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(4 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_common = herb['herb_name_common']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ##
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ##
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        y_cur += herb_name_scientific_y
        ##
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ##
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_filepath = f'assets/shop/labels/alpha/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ###
        label_folderpath = f'assets/shop/labels/public/vintage/oval/3x4'
        ### mask
        label = label.convert('RGBA')
        mask = Image.new('RGB', (label_w, label_h), '#000000')
        draw = ImageDraw.Draw(mask)
        draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.01)), (label_w-int(label_w*0.05), label_h-int(label_h*0.01))), fill="#ffffff")
        mask = mask.convert('L')
        label.putalpha(mask)
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ###
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def assets_oval_1_5x2_5():
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(1.5 * dpi)
    label_h = int(2.5 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/oval/1.5x2.5'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.01)), (label_w-int(label_w*0.05), label_h-int(label_h*0.01))), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_oval_2x3():
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(3 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/oval/2x3'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.01)), (label_w-int(label_w*0.05), label_h-int(label_h*0.01))), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def assets_oval_3x4():
    background_filepath = f'assets/shop/labels/oval.png'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(4 * dpi)
    label_folderpath = f'assets/shop/labels/public/vintage/oval/3x4'
    label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
    background = Image.open(background_filepath)
    background = background.resize((label_w, label_h))
    label.paste(background, (0, 0))
    ### mask
    mask = Image.new('RGB', (label_w, label_h), '#000000')
    draw = ImageDraw.Draw(mask)
    draw.ellipse(((0+int(label_w*0.05), 0+int(label_h*0.01)), (label_w-int(label_w*0.05), label_h-int(label_h*0.01))), fill="#ffffff")
    mask = mask.convert('L')
    label.putalpha(mask)
    label_assets_folderpath = f'{label_folderpath}/assets'
    try: os.makedirs(label_assets_folderpath)
    except: pass
    label_assets_filepath = f'{label_assets_folderpath}/background.png'
    label.save(label_assets_filepath)

def sheet_oval_1_5x2_5():
    a4_w = 2480
    a4_h = 3508
    row_num = 4
    col_num = 4
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(1.5 * 300)
    label_h = int(2.5 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-1_5x2_5/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/1.5x2.5/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    # sheet.show()
    # quit()
    output_folderpath = f'assets/shop/labels/public/vintage/oval/1.5x2.5/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/1.5x2.5-1.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_oval_2x3():
    a4_w = 2480
    a4_h = 3508
    col_num = 2
    row_num = 3
    gap = 30
    mx = 600
    my = 300
    img_i = 0
    label_w = int(2 * 300)
    label_h = int(3 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-2x3/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/2x3/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/oval/2x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x3-1.jpg'
    sheet.save(output_filepath)
    ###
    my = 600
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-2x3/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/2x3/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/oval/2x3/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/2x3-2.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def sheet_oval_3x4():
    a4_w = 2480
    a4_h = 3508
    col_num = 2
    row_num = 2
    gap = 30
    mx = 300
    my = 600
    img_i = 0
    label_w = int(3 * 300)
    label_h = int(4 * 300)
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-3x4/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/oval/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-1.jpg'
    sheet.save(output_filepath)
    # sheet.show()
    ###
    my = 600
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-3x4/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/oval/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-2.jpg'
    sheet.save(output_filepath)
    # sheet.show()
    ###
    my = 900
    sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
    for row_i in range(row_num):
        for col_i in range(col_num):
            if img_i < len(herb_list):
                herb = herb_list[img_i]
                print(herb)
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                # image_filepath = f'assets/shop/labels/final-oval-3x4/{img_i}-{herb_slug}.jpg'
                image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{img_i}-{herb_slug}.png'
                image = Image.open(image_filepath)
                sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    sheet = sheet.convert('RGB')
    output_folderpath = f'assets/shop/labels/public/vintage/oval/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-3.jpg'
    sheet.save(output_filepath)
    # sheet.show()

def pin_oval():
    pin_w = 1000
    pin_h = 1500
    row_num = 10
    scale = 0.27
    label_w = int(3 * 300 * scale)
    label_h = int(4 * 300 * scale)
    col_num = pin_w // label_w
    col_num = 5
    # label_w = pin_w // col_n
    # label_h = pin_h // row_n
    gap = 0
    img_i = 0
    mx = -100
    my = -50
    pin_image = Image.new(mode="RGBA", size=(pin_w, pin_h), color=g.color_linen)
    herb_list_shuffle = herb_list[:]
    random.shuffle(herb_list_shuffle)
    for row_i in range(row_num):
        for col_i in range(col_num):
            img_i = img_i % len(herb_list_shuffle)
            if img_i < len(herb_list_shuffle):
                herb = herb_list_shuffle[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                herb_filename_correct = ''
                for herb_filename in os.listdir(f'assets/shop/labels/public/vintage/oval/3x4/png'):
                    if herb_slug in herb_filename:
                        herb_filename_correct = herb_filename
                        break
                image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{herb_filename_correct}'
                image = Image.open(image_filepath)
                image = img_resize(image, label_w, label_h)
                pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    pin_image = pin_image.convert('RGB')
    draw = ImageDraw.Draw(pin_image)
    draw.rectangle(((0, pin_h//2 - 160), (pin_w, pin_h//2 + 160)), fill=g.color_carbon_powder)
    # circle
    circle_size = 420
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=g.color_carbon_powder)
    # number
    color = g.color_linen
    line = '120'
    font_size = 192
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - 220), line, color, font=font)
    # text
    gap = 50
    y_off = 0
    line = 'herb jar labels'.title()
    font_size = 96
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - gap + y_off), line, color, font=font)
    ###
    line = 'download'.title()
    font_size = 96
    font_family, font_weight = 'Allura', 'Regular'
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 + gap + y_off), line, color, font=font)
    # copyright
    y_off = 120
    draw.rectangle(((pin_w//2 - 100, pin_h - y_off), (pin_w//2 + 100, pin_h - y_off + 40)), fill=g.color_carbon_powder)
    line = 'terrawhisper.com'.upper()
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off + 10), line, color, font=font)
    '''
    output_folderpath = f'assets/shop/labels/public/vintage/oval/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-1.jpg'
    sheet.save(output_filepath)
    '''
    pin_image.show()

def pin_round():
    pin_w = 1000
    pin_h = 1500
    row_num = 10
    scale = 0.30
    label_w = int(3 * 300 * scale)
    label_h = int(3 * 300 * scale)
    col_num = pin_w // label_w
    col_num = 5
    # label_w = pin_w // col_n
    # label_h = pin_h // row_n
    gap = 30
    img_i = 0
    mx = -100
    my = -100
    pin_image = Image.new(mode="RGBA", size=(pin_w, pin_h), color=g.color_linen)
    herb_list_shuffle = herb_list[:]
    random.shuffle(herb_list_shuffle)
    for row_i in range(row_num):
        for col_i in range(col_num):
            img_i = img_i % len(herb_list_shuffle)
            if img_i < len(herb_list_shuffle):
                herb = herb_list_shuffle[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                herb_filename_correct = ''
                for herb_filename in os.listdir(f'assets/shop/labels/public/vintage/oval/3x4/png'):
                    if herb_slug in herb_filename:
                        herb_filename_correct = herb_filename
                        break
                image_filepath = f'assets/shop/labels/public/vintage/round/3x3/png/{herb_filename_correct}'
                image = Image.open(image_filepath)
                image = img_resize(image, label_w, label_h)
                pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    pin_image = pin_image.convert('RGB')
    draw = ImageDraw.Draw(pin_image)
    draw.rectangle(((0, pin_h//2 - 160), (pin_w, pin_h//2 + 160)), fill=g.color_carbon_powder)
    # circle
    circle_size = 420
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=g.color_carbon_powder)
    # number
    color = g.color_linen
    line = '120'
    font_size = 192
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - 220), line, color, font=font)
    # text
    gap = 50
    y_off = 0
    line = 'herb jar labels'.title()
    font_size = 96
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - gap + y_off), line, color, font=font)
    ###
    line = 'download'.title()
    font_size = 96
    font_family, font_weight = 'Allura', 'Regular'
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 + gap + y_off), line, color, font=font)
    # copyright
    y_off = 120
    draw.rectangle(((pin_w//2 - 100, pin_h - y_off), (pin_w//2 + 100, pin_h - y_off + 40)), fill=g.color_carbon_powder)
    line = 'terrawhisper.com'.upper()
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off + 10), line, color, font=font)
    '''
    output_folderpath = f'assets/shop/labels/public/vintage/oval/3x4/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/3x4-1.jpg'
    sheet.save(output_filepath)
    '''
    pin_image.show()

def pin_mix():
    pin_w = 1000
    pin_h = 1500
    row_num = 10
    scale = 0.30
    col_num = 5
    gap = 30
    img_i = 0
    mx = -100
    my = -100
    pin_image = Image.new(mode="RGBA", size=(pin_w, pin_h), color=g.color_linen)
    herb_list_shuffle = herb_list[:]
    random.shuffle(herb_list_shuffle)
    for row_i in range(row_num):
        for col_i in range(col_num):
            img_i = img_i % len(herb_list_shuffle)
            if img_i < len(herb_list_shuffle):
                herb = herb_list_shuffle[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                herb_filename_correct = ''
                for herb_filename in os.listdir(f'assets/shop/labels/public/vintage/oval/3x4/png'):
                    if herb_slug in herb_filename:
                        herb_filename_correct = herb_filename
                        break
                rnd = random.randint(0, 3)
                if rnd == 0:
                    image_filepath = f'assets/shop/labels/public/vintage/round/3x3/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(3 * 300 * scale)
                elif rnd == 1:
                    image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(4 * 300 * scale)
                elif rnd == 2:
                    image_filepath = f'assets/shop/labels/public/vintage/square/3x3/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(3 * 300 * scale)
                else:
                    image_filepath = f'assets/shop/labels/public/vintage/rectangle/3x4/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(4 * 300 * scale)

                image = Image.open(image_filepath)
                image = img_resize(image, label_w, label_h)
                label_w = int(3 * 300 * scale)
                label_h = int(4 * 300 * scale)
                pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    pin_image = pin_image.convert('RGB')
    draw = ImageDraw.Draw(pin_image)
    draw.rectangle(((0, pin_h//2 - 160), (pin_w, pin_h//2 + 160)), fill=g.color_carbon_powder)
    # circle
    circle_size = 420
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=g.color_carbon_powder)
    # number
    color = g.color_linen
    line = '120'
    font_size = 192
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - 220), line, color, font=font)
    # text
    gap = 50
    y_off = 0
    line = 'herb jar labels'.title()
    font_size = 96
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - gap + y_off), line, color, font=font)
    ###
    line = 'download'.title()
    font_size = 96
    font_family, font_weight = 'Allura', 'Regular'
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 + gap + y_off), line, color, font=font)
    # copyright
    y_off = 120
    draw.rectangle(((pin_w//2 - 100, pin_h - y_off), (pin_w//2 + 100, pin_h - y_off + 40)), fill=g.color_carbon_powder)
    line = 'terrawhisper.com'.upper()
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off + 10), line, color, font=font)
    output_folderpath = f'assets/shop/labels/public/vintage/listing'
    try: os.makedirs(output_folderpath)
    except: pass
    output_filepath = f'{output_folderpath}/cover-1.jpg'
    pin_image.save(output_filepath)
    # pin_image.show()

# rectangle
if 0:
    labels_rectangle_1x2_625()
    labels_rectangle_2x3()
    labels_rectangle_3x4()
if 0:
    sheet_rectangles_1x2_625()
    sheet_rectangles_2x3()
    sheet_rectangles_3x4()
if 0:
    assets_rectangle_1x2_625()
    assets_rectangle_2x3()
    assets_rectangle_3x4()

# square
if 0:
    labels_square_1_5x1_5()
    labels_square_2x2()
    labels_square_3x3()
if 0:
    sheet_square_1_5x1_5()
    sheet_square_2x2()
    sheet_square_3x3()
if 0:
    assets_square_1_5x1_5()
    assets_square_2x2()
    assets_square_3x3()

# round
if 0:
    labels_round_1x1()
    labels_round_2x2()
    labels_round_3x3()
if 0:
    sheet_round_1x1()
    sheet_round_2x2()
    sheet_round_3x3()
if 0:
    assets_round_1x1()
    assets_round_2x2()
    assets_round_3x3()

# oval
if 0:
    labels_oval_1_5x2_5()
    labels_oval_2x3()
    labels_oval_3x4()
if 0:
    sheet_oval_1_5x2_5()
    sheet_oval_2x3()
    sheet_oval_3x4()
if 0:
    assets_oval_1_5x2_5()
    assets_oval_2x3()
    assets_oval_3x4()

# pin_oval()
# pin_round()
# pin_mix()

###########################################################
# ;100 herbs
###########################################################
def text_to_lines(text, font, herb_name_width_max):
    text = text.strip()
    lines = []
    line = ''
    for word in text.split():
        _, _, line_w, line_h = font.getbbox(line)
        _, _, word_w, word_h = font.getbbox(word)
        if line_w + word_w < herb_name_width_max:
            line += f'{word} '
        else:
            if len(line.strip().split()) == 0:
                lines.append(word.strip())
            else:
                lines.append(line.strip())
                line = f'{word} '
    if line.strip() != '':
        lines.append(line.strip())
    print(lines)
    return lines

def labels_100_oval_1x2():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/1x2'
    herb_name_common_size = 24
    herb_name_common_y = 120
    herb_name_scientific_size = 18
    herb_name_scientific_y = 40
    herb_image_size = 0.45
    herb_image_y = 70
    background_filepath = f'assets/shop/labels/oval-alpha-2.png'
    dpi = 300
    label_w = int(1 * dpi)
    label_h = int(2 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        herb_name_common = herb_entity['herb_common_names'][0]['answer']
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ### background
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ### name common
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = text_to_lines(line, font)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
            y_cur += font_size*1.2
        # y_cur += herb_name_scientific_y
        ### name scientific
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ### herb image
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_alpha_folderpath = f'assets/shop/labels/herbs/alpha'
        herb_filepath = f'{herb_alpha_folderpath}/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ### png
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ### jpg
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_100_oval_2x3():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/2x3'
    herb_name_common_size = 36
    herb_name_common_y = 120
    herb_name_scientific_size = 18
    herb_name_scientific_y = 40
    herb_image_size = 0.45
    herb_image_y = 70
    background_filepath = f'assets/shop/labels/oval-alpha-2.png'
    dpi = 300
    label_w = int(2 * dpi)
    label_h = int(3 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        herb_name_common = herb_entity['herb_common_names'][0]['answer']
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ### background
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ### name common
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = text_to_lines(line, font)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
            y_cur += font_size*1.2
        # y_cur += herb_name_scientific_y
        ### name scientific
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ### herb image
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_alpha_folderpath = f'assets/shop/labels/herbs/alpha'
        herb_filepath = f'{herb_alpha_folderpath}/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ### png
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ### jpg
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_100_oval_3x5():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/3x5'
    herb_name_common_size = 36
    herb_name_common_y = 120
    herb_name_scientific_size = 18
    herb_name_scientific_y = 40
    herb_image_size = 0.45
    herb_image_y = 70
    background_filepath = f'assets/shop/labels/oval-alpha-2.png'
    dpi = 300
    label_w = int(3 * dpi)
    label_h = int(5 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        herb_name_common = herb_entity['herb_common_names'][0]['answer']
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ### background
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ### name common
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = text_to_lines(line, font)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
            y_cur += font_size*1.2
        # y_cur += herb_name_scientific_y
        ### name scientific
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ### herb image
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_alpha_folderpath = f'assets/shop/labels/herbs/alpha'
        herb_filepath = f'{herb_alpha_folderpath}/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ### png
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ### jpg
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def labels_100_oval_5x8():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/5x8'
    herb_name_common_size = 36
    herb_name_common_y = 120
    herb_name_scientific_size = 18
    herb_name_scientific_y = 40
    herb_image_size = 0.45
    herb_image_y = 70
    background_filepath = f'assets/shop/labels/oval-alpha-2.png'
    dpi = 300
    label_w = int(5 * dpi)
    label_h = int(8 * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        herb_name_common = herb_entity['herb_common_names'][0]['answer']
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ### background
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ### name common
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = text_to_lines(line, font)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
            y_cur += font_size*1.2
        # y_cur += herb_name_scientific_y
        ### name scientific
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
        ### herb image
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        herb_alpha_folderpath = f'assets/shop/labels/herbs/alpha'
        herb_filepath = f'{herb_alpha_folderpath}/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = img_resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ### png
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        # label.show()
        ### jpg
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # label.show()
        # quit()

def sheets_100_oval_1x2():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/1x2'
    a4_w = 2480
    a4_h = 3508
    row_num = 3
    col_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(1 * 300)
    label_h = int(2 * 300)
    completed = False
    sheet_list = []
    for sheet_i in range(999):
        if completed: break
        sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
        for row_i in range(row_num):
            for col_i in range(col_num):
                if img_i < len(herb_list):
                    herb = herb_list[img_i]
                    herb_name_scientific = herb['herb_name_scientific']
                    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                    image_filepath = f'{label_folderpath}/png/{img_i}-{herb_slug}.png'
                    image = Image.open(image_filepath)
                    sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                    img_i += 1
                else:
                    completed = True
        sheet_list.append(sheet)
    output_folderpath = f'{label_folderpath}/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    for sheet_i, sheet in enumerate(sheet_list):
        sheet = sheet.convert('RGB')
        # sheet.show()
        # quit()
        output_filepath = f'{output_folderpath}/1x2-{sheet_i+1}.jpg'
        sheet.save(output_filepath)
        # sheet.show()

def sheets_100_oval_2x3():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/2x3'
    a4_w = 2480
    a4_h = 3508
    row_num = 3
    col_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(2 * 300)
    label_h = int(3 * 300)
    completed = False
    sheet_list = []
    for sheet_i in range(999):
        if completed: break
        sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
        for row_i in range(row_num):
            for col_i in range(col_num):
                if img_i < len(herb_list):
                    herb = herb_list[img_i]
                    herb_name_scientific = herb['herb_name_scientific']
                    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                    image_filepath = f'{label_folderpath}/png/{img_i}-{herb_slug}.png'
                    image = Image.open(image_filepath)
                    sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                    img_i += 1
                else:
                    completed = True
        sheet_list.append(sheet)
    output_folderpath = f'{label_folderpath}/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    for sheet_i, sheet in enumerate(sheet_list):
        sheet = sheet.convert('RGB')
        # sheet.show()
        # quit()
        output_filepath = f'{output_folderpath}/2x3-{sheet_i+1}.jpg'
        sheet.save(output_filepath)
        # sheet.show()

def sheets_100_oval_3x5():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/3x5'
    a4_w = 2480
    a4_h = 3508
    row_num = 3
    col_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(3 * 300)
    label_h = int(5 * 300)
    completed = False
    sheet_list = []
    for sheet_i in range(999):
        if completed: break
        sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
        for row_i in range(row_num):
            for col_i in range(col_num):
                if img_i < len(herb_list):
                    herb = herb_list[img_i]
                    herb_name_scientific = herb['herb_name_scientific']
                    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                    image_filepath = f'{label_folderpath}/png/{img_i}-{herb_slug}.png'
                    image = Image.open(image_filepath)
                    sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                    img_i += 1
                else:
                    completed = True
        sheet_list.append(sheet)
    output_folderpath = f'{label_folderpath}/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    for sheet_i, sheet in enumerate(sheet_list):
        sheet = sheet.convert('RGB')
        # sheet.show()
        # quit()
        output_filepath = f'{output_folderpath}/3x5-{sheet_i+1}.jpg'
        sheet.save(output_filepath)
        # sheet.show()

def sheets_100_oval_5x8():
    label_folderpath = f'assets/shop/labels/public/100/vintage/oval/5x8'
    a4_w = 2480
    a4_h = 3508
    row_num = 3
    col_num = 3
    gap = 30
    mx = 300
    my = 300
    img_i = 0
    label_w = int(5 * 300)
    label_h = int(8 * 300)
    completed = False
    sheet_list = []
    for sheet_i in range(999):
        if completed: break
        sheet = Image.new(mode="RGBA", size=(a4_w, a4_h), color='#ffffff')
        for row_i in range(row_num):
            for col_i in range(col_num):
                if img_i < len(herb_list):
                    herb = herb_list[img_i]
                    herb_name_scientific = herb['herb_name_scientific']
                    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                    image_filepath = f'{label_folderpath}/png/{img_i}-{herb_slug}.png'
                    image = Image.open(image_filepath)
                    sheet.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                    img_i += 1
                else:
                    completed = True
        sheet_list.append(sheet)
    output_folderpath = f'{label_folderpath}/sheets'
    try: os.makedirs(output_folderpath)
    except: pass
    for sheet_i, sheet in enumerate(sheet_list):
        sheet = sheet.convert('RGB')
        # sheet.show()
        # quit()
        output_filepath = f'{output_folderpath}/5x8-{sheet_i+1}.jpg'
        sheet.save(output_filepath)
        # sheet.show()

def labels_100(shape, size, herb_image_size, herb_image_y, herb_name_common_size, herb_name_common_y, herb_name_common_width_max, herb_name_scientific_width_max, herb_name_scientific_size, herb_name_scientific_y, text_vertical=False, alpha=True, mod=False):
    label_folderpath = f'{g.assets_folderpath}/shop/labels/public/100/vintage/{shape}/{size}'
    if alpha:
        background_filepath = f'{g.assets_folderpath}/shop/labels/backgrounds/mod/{shape}-alpha.png'
    else:
        background_filepath = f'{g.assets_folderpath}/shop/labels/backgrounds/mod/{shape}.png'
    dpi = 300
    size_w, size_h = size.split('x')
    label_w = int(int(size_w) * dpi)
    label_h = int(int(size_h) * dpi)
    for herb_i, herb in enumerate(herb_list):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        # herb_entity = io.json_read(f'database/entities/herbs/{herb_slug}.json')
        # herb_name_common = herb_entity['herb_common_names'][0]['answer']
        herb_name_common = herb['herb_name_common']
        label_filepath = f'{label_folderpath}/{herb_i}-{herb_slug}.jpg'
        label = Image.new(mode="RGBA", size=(label_w, label_h), color='#ffffff')
        draw = ImageDraw.Draw(label)
        ### background
        background = Image.open(background_filepath)
        background = background.resize((label_w, label_h))
        label.paste(background, (0, 0))
        ### name common
        y_cur = 0
        y_cur += herb_name_common_y
        line = herb_name_common
        font_size = herb_name_common_size
        font_family, font_weight = 'cinzel-decorative', 'regular'
        font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        lines = text_to_lines(line, font, herb_name_common_width_max)
        if text_vertical:
            line = lines[0]
            _, _, line_w, line_h = font.getbbox(line)
            text_image = Image.new('RGBA', (line_w, line_h))
            text_image_draw = ImageDraw.Draw(text_image)
            text_image_draw.text((0, 0), line, '#423626', font=font)
            text_image = text_image.rotate(90, expand=1)
            text_image_w, text_image_h = text_image.size
            label.paste(text_image, (herb_name_common_y, label_h//2 - text_image_h//2), text_image)
        else:
            for line in lines:
                _, _, line_w, line_h = font.getbbox(line)
                draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
                y_cur += font_size*1.2
        y_cur += herb_name_scientific_y
        ### name scientific
        line = herb_name_scientific
        font_size = herb_name_scientific_size
        font_family, font_weight = 'vollkorn-sc', 'regular'
        font_path = f"{g.assets_folderpath}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        lines = text_to_lines(line, font, herb_name_scientific_width_max)
        if text_vertical:
            line = lines[0]
            _, _, line_w, line_h = font.getbbox(line)
            text_image = Image.new('RGBA', (line_w, line_h))
            text_image_draw = ImageDraw.Draw(text_image)
            text_image_draw.text((0, 0), line, '#423626', font=font)
            text_image = text_image.rotate(90, expand=1)
            text_image_w, text_image_h = text_image.size
            label.paste(text_image, (herb_name_scientific_y, label_h//2 - text_image_h//2), text_image)
        else:
            for line in lines:
                _, _, line_w, line_h = font.getbbox(line)
                draw.text((label_w//2 - line_w//2, y_cur), line, '#423626', font=font)
                y_cur += font_size*1.2
        ### herb image
        herb_y = herb_image_y
        herb_size_mul = herb_image_size
        herb_w = int(832 * herb_size_mul)
        herb_h = int(1216 * herb_size_mul)
        if mod:
            herb_alpha_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/alpha-mod'
        else:
            herb_alpha_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/alpha'
        herb_filepath = f'{herb_alpha_folderpath}/{herb_i}-{herb_slug}.png'
        herb_image = Image.open(herb_filepath)
        herb_image = media.resize(herb_image, herb_w, herb_h)
        label.paste(herb_image, (int(label_w//2 - herb_w//2), int(label_h//2 - herb_h//2) + herb_y), herb_image)
        ### png
        label = label.convert('RGBA')
        label_png_folderpath = f'{label_folderpath}/png'
        try: os.makedirs(label_png_folderpath)
        except: pass
        label_png_filepath = f'{label_png_folderpath}/{herb_i}-{herb_slug}.png'
        label.save(label_png_filepath)
        ### jpg
        label_bg = Image.new('RGBA', (label_w, label_h), '#ffffff')
        label_bg.paste(label, (0, 0), label)
        label = label_bg
        label = label.convert('RGB')
        label_jpg_folderpath = f'{label_folderpath}/jpg'
        try: os.makedirs(label_jpg_folderpath)
        except: pass
        label_jpg_filepath = f'{label_jpg_folderpath}/{herb_i}-{herb_slug}.jpg'
        label.save(label_jpg_filepath, format='JPEG', quality=30)
        # quit()
        # break

def ai_img_herb_100(val=''):
    image_folderpath = f'{g.assets_folderpath}/shop/labels/herbs'
    try: os.makedirs(image_folderpath)
    except: pass
    image_tmp_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/tmp'
    try: os.makedirs(image_tmp_folderpath)
    except: pass
    image_valid_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/valid'
    try: os.makedirs(image_valid_folderpath)
    except: pass
    for herb_i, herb in enumerate(herb_list):
        print(f'{herb_i}/{len(herb_list)} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        ###
        img_tmp_filepath = f'{image_tmp_folderpath}/test.jpg'
        img_valid_filepath = f'{image_valid_folderpath}/{herb_i}-{herb_slug}.jpg'
        if os.path.exists(img_valid_filepath): continue
        if val.strip() != '':
            herb_name_scientific = val.strip()
        positive_prompt = f'''
            {herb_name_scientific}, line drawing, monochrome,
            paper, antique, old, 
            victorian, vintage, rustic, elegant,
            light background,
            high resolution
        '''
        negative_prompt = f'''
            text, watermark 
        '''
        img_w = 832
        img_h = 1216
        images_filepaths = []
        pipe_init()
        image = pipe(
            prompt=positive_prompt, 
            negative_prompt=negative_prompt, 
            width=img_w, 
            height=img_h, 
            num_inference_steps=25, 
            guidance_scale=6.0
        ).images[0]
        image.save(img_tmp_filepath)
        # image.show()
        return img_tmp_filepath, img_valid_filepath



####################################################################
####################################################################
####################################################################
if 0:
    img_valid_filepath = ''
    while True:
        val = input('gen >> ')
        if val == '': 
            img_tmp_filepath, img_valid_filepath = ai_img_herb_100()
        elif val == ' ': 
            shutil.copy2(img_tmp_filepath, img_valid_filepath)
            img_tmp_filepath, img_valid_filepath = ai_img_herb_100()
        else:
            img_tmp_filepath, img_valid_filepath = ai_img_herb_100(val)
    ai_img_herbs_100_alpha()

def calculate_image_state(image):
    img = image.convert('RGB')
    img_array = np.array(img) / 255.0

    brightness = np.mean(img_array)
    
    avg_color = np.mean(img_array, axis=(0, 1))

    hsv = np.array(img.convert('HSV'))
    saturation = np.mean(hsv[:, :, 1]) / 255.0

    contrast = np.std(img_array)
    
    return brightness, avg_color, saturation, contrast

def match_style(source_image, target_image):
    target_brightness, target_color, target_saturation, target_contrast = calculate_image_state(target_image)
    source_brightness, source_color, source_saturation, source_contrast = calculate_image_state(source_image)

    img = source_image.convert('RGB')
    brightness_factor = target_brightness / source_brightness if source_brightness > 0 else 1
    img = ImageEnhance.Brightness(img).enhance(brightness_factor)

    img_array = np.array(img) / 255.0
    current_color = np.mean(img_array, axis=(0, 1))
    color_factors = target_color / current_color
    img_balance = np.clip(img_array * color_factors, 0, 1)
    img = Image.fromarray((img_balance*255).astype(np.uint8))
    
    current_hsv = np.array(img.convert('HSV'))
    current_saturation = np.mean(current_hsv[:, :, 1]) / 255.0
    saturation_factor = target_saturation / current_saturation if current_saturation > 0 else 1
    img = ImageEnhance.Color(img).enhance(saturation_factor)

    img_array = np.array(img) / 255.0
    current_contrast = np.std(img_array)
    current_contrast *= 0.8
    contrast_factor = target_contrast / current_contrast if current_contrast > 0 else 1 
    img = ImageEnhance.Contrast(img).enhance(contrast_factor)
    
    return img

def valid_mod(input_folderpath_rel, output_folderpath_rel, target_filepath_rel):
    input_folderpath = f'{g.database_folderpath}/assets/shop/labels/{input_folderpath_rel}'
    output_folderpath = f'{g.database_folderpath}/assets/shop/labels/{output_folderpath_rel}'
    filename_list = sorted(os.listdir(input_folderpath))
    for filename in filename_list:
        input_filepath = f'{input_folderpath}/{filename}'
        output_filepath = f'{output_folderpath}/{filename}'
        '''
        source_filepath = f'{g.database_folderpath}/assets/shop/labels/herbs/valid/0-zingiber-officinale.jpg'
        source_filepath = f'{g.database_folderpath}/assets/shop/labels/herbs/valid/3-lavandula-angustifolia.jpg'
        target_filepath = f'{g.database_folderpath}/assets/shop/labels/oval-alpha.png'
        '''
        source_filepath = input_filepath
        target_filepath = f'{g.database_folderpath}/assets/shop/labels/{target_filepath_rel}'
        source_image = Image.open(source_filepath)
        target_image = Image.open(target_filepath)
        img = match_style(source_image, target_image)
        sheet = Image.new('RGB', (832*3, 1216), color='#ffffff')
        sheet.paste(target_image, (832*0, 0)) 
        sheet.paste(source_image, (832*1, 1)) 
        sheet.paste(img, (832*2, 0)) 
        # sheet.save(f'{g.database_folderpath}/assets/shop/labels/test.jpg')
        img.save(output_filepath)

# valid_mod('herbs/valid', 'herbs/valid-mod', 'oval-alpha.png')
# valid_mod('backgrounds/raw', 'backgrounds/mod', 'backgrounds/raw/oval-alpha.png')
# quit()

def alpha_mod():
    input_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/valid-mod'
    try: os.makedirs(input_folderpath)
    except: pass
    output_folderpath = f'{g.assets_folderpath}/shop/labels/herbs/alpha-mod'
    try: os.makedirs(output_folderpath)
    except: pass
    for herb_i, herb in enumerate(herb_list):
        # herb_slug = herb['herb_slug']
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        image_filepath = f'{input_folderpath}/{herb_i}-{herb_slug}.jpg'
        image = Image.open(image_filepath)
        global bg_model
        if not bg_model:
            bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
        torch.set_float32_matmul_precision(['high', 'highest'][0])
        bg_model.to('cuda')
        bg_model.eval()
        # Data settings
        image_size = (832, 1216)
        transform_image = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        input_images = transform_image(image).unsqueeze(0).to('cuda')
        # Prediction
        with torch.no_grad():
            preds = bg_model(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image.size)
        image.putalpha(mask)
        image_filepath = f'{output_folderpath}/{herb_i}-{herb_slug}.png'
        image.save(image_filepath)

# alpha_mod()

# oval
if 1:
    if 1:
        labels_100(
            'oval', '1x2', 
            herb_name_common_size = 20,
            herb_name_common_y = 140,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 16,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 100,
            herb_image_size = 0.20,
            herb_image_y = 60,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'oval', '2x3', 
            herb_name_common_size = 40,
            herb_name_common_y = 200,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 20,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.35,
            herb_image_y = 70,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'oval', '3x5', 
            herb_name_common_size = 60,
            herb_name_common_y = 320,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 36,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.60,
            herb_image_y = 100,
            text_vertical = False,
            mod = True,
        )
    if 0:
        sheets_100_oval_1x2()
        sheets_100_oval_2x3()
        sheets_100_oval_3x5()

# rectangle
if 1:
    if 1:
        labels_100(
            'rectangle', '1x2', 
            herb_name_common_size = 20,
            herb_name_common_y = 140,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 16,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 100,
            herb_image_size = 0.20,
            herb_image_y = 60,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'rectangle', '2x3', 
            herb_name_common_size = 40,
            herb_name_common_y = 200,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 20,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.35,
            herb_image_y = 70,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'rectangle', '3x5', 
            herb_name_common_size = 60,
            herb_name_common_y = 320,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 36,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.60,
            herb_image_y = 100,
            text_vertical = False,
            mod = True,
        )

# square
if 1:
    if 1:
        labels_100(
            'square', '1x1', 
            herb_name_common_size = 20,
            herb_name_common_y = 60,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 14,
            herb_name_scientific_y = 5,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.10,
            herb_image_y = 30,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'square', '2x2', 
            herb_name_common_size = 40,
            herb_name_common_y = 110,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 20,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.25,
            herb_image_y = 60,
            text_vertical = False,
            mod = True,
        )
    if 1:
        labels_100(
            'square', '3x3', 
            herb_name_common_size = 60,
            herb_name_common_y = 160,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 30,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.40,
            herb_image_y = 90,
            text_vertical = False,
            mod = True,
        )

# round
if 1:
    if 1:
        labels_100(
            'round', '1x1', 
            herb_name_common_size = 18,
            herb_name_common_y = 70,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 12,
            herb_name_scientific_y = 5,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.10,
            herb_image_y = 30,
            # text_vertical = True,
            mod = True,
        ),
    if 1:
        labels_100(
            'round', '2x2', 
            herb_name_common_size = 36,
            herb_name_common_y = 130,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 18,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.20,
            herb_image_y = 50,
            # text_vertical = True,
            mod = True,
        ),
    if 1:
        labels_100(
            'round', '3x3', 
            herb_name_common_size = 54,
            herb_name_common_y = 200,
            herb_name_common_width_max = 9999,
            herb_name_scientific_size = 24,
            herb_name_scientific_y = 10,
            herb_name_scientific_width_max = 9999,
            herb_image_size = 0.30,
            herb_image_y = 70,
            # text_vertical = True,
            mod = True,
        ),

