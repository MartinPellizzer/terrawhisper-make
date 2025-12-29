from lib import g
from lib import io
from lib import polish

def is_herb_in_list(herb_tmp, herbs):
    found = False
    for herb in herbs:
        if herb['herb_name_scientific'] == herb_tmp['herb_name_scientific']:
            found = True
            break
    return found

def herbs_primary_get():
    herbs = []
    ###
    herbs_filepaths = [
        f'{g.database_folderpath}/csv/herbs-book-0001.csv',
        f'{g.database_folderpath}/csv/herbs-legacy.csv',
    ]
    for herbs_filepath in herbs_filepaths:
        herbs_tmp = io.csv_to_dict(herbs_filepath)
        for herb_tmp in herbs_tmp:
            herb_tmp_name_scientific = herb_tmp['herb_name_scientific'].lower().strip()
            herb_tmp_name_scientific = herb_tmp_name_scientific.replace('×', 'x')
            herb_tmp['herb_name_scientific'] = herb_tmp_name_scientific
            herb_tmp_slug = polish.sluggify(herb_tmp_name_scientific)
            found = is_herb_in_list(herb_tmp, herbs)
            if not found: herbs.append(herb_tmp)
    ###
    herbs = sorted(herbs, key=lambda x: x['herb_name_scientific'], reverse=False)
    for herb in herbs:
        print(herb)
    print(len(herbs))
    # quit()
    return herbs

def herbs_primary_medicinal_get():
    herbs = herbs_primary_get()
    herbs_medicinal = []
    for herb in herbs:
        print(herb)
        ssot_herb_filepath = f'''{g.database_folderpath}/ssot/herbs/herbs-primary/{herb['herb_slug']}.json'''
        if herb_medicine_or_poison_get(ssot_herb_filepath) == 'medicine':
            herbs_medicinal.append(herb)
    herbs_medicinal = sorted(herbs_medicinal, key=lambda x: x['herb_name_scientific'], reverse=False)
    # print(len(herbs_medicinal))
    return herbs_medicinal

def herbs_primary_medicinal_get_old():
    herbs = herbs_primary_get()
    herbs_medicinal = []
    for herb in herbs:
        print(herb)
        entities_herbs_folderpath = f''
        entity_herb_filepath = f'''{g.database_folderpath}/entities/herbs/{herb['herb_slug']}.json'''
        if herb_medicine_or_poison_get(entity_herb_filepath) == 'medicine':
            herbs_medicinal.append(herb)
    herbs_medicinal = sorted(herbs_medicinal, key=lambda x: x['herb_name_scientific'], reverse=False)
    # print(len(herbs_medicinal))
    return herbs_medicinal

def herbs_by_ailments():
    output_herb_list = []
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparation_list):
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            print(f'PREPARATION: {preparation_slug}')
            url_relative = f'ailments/{ailment_slug}/{preparation_slug}'
            json_article_filepath = f'{g.database_folderpath}/json/{url_relative}.json'
            json_article = io.json_read(json_article_filepath)
            json_article_preparation_list = json_article['preparations']
            for json_article_preparation in json_article_preparation_list[:10]:
                json_article_herb_name_scientific = json_article_preparation['herb_name_scientific']
                print(json_article_preparation)
                if json_article_herb_name_scientific not in output_herb_list:
                    output_herb_list.append(json_article_herb_name_scientific)

def herb_medicine_or_poison_get(entity_herb_filepath):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    herb_medicine_or_poison = entity_herb['medicine_or_poison']
    medicine_or_poison = ''
    medicine_score = 0
    poison_score = 0
    inert_score = 0
    for obj in herb_medicine_or_poison:
        if 'answer' in obj:
            answer = obj['answer']
            total_score = obj['total_score']
            if answer == 'medicine':
                medicine_score = total_score
            elif answer == 'poison':
                poison_score = total_score
            elif answer == 'inert':
                inert_score = total_score
            
    if medicine_score > poison_score and medicine_score > inert_score:
        medicine_or_poison = 'medicine'
    elif poison_score > medicine_score and poison_score > inert_score:
        medicine_or_poison = 'poison'
    else:
        medicine_or_poison = 'inert'
    return medicine_or_poison

def herbs_popular_get(preparation_slug, herbs_num):
    herbs = []
    ailments = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparations = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailments):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparations):
            _preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            print(f'PREPARATION: {preparation_slug}')
            if preparation_slug != _preparation_slug: continue
            url_relative = f'ailments/{ailment_slug}/{preparation_slug}'
            json_article_filepath = f'''{g.database_folderpath}/json/{url_relative}.json'''
            json_article = io.json_read(json_article_filepath)
            json_article_preparations = json_article['preparations']
            for json_article_preparation in json_article_preparations:
                herb_name_scientific = json_article_preparation['herb_name_scientific']
                # herb_name_scientific = herb_name_scientific.replace('mentha piperita', 'mentha x piperita')
                found = False
                for herb in herbs:
                    if herb['herb_name_scientific'] == herb_name_scientific:
                        herb['mentions'] += 1
                        found = True
                        break
                if not found:
                    herbs.append({
                        'herb_name_scientific': herb_name_scientific,
                        'mentions': 1,
                    })
            # quit()
    herbs = sorted(herbs, key=lambda x: x['mentions'], reverse=True)
    for herb in herbs:
        print(herb)
    print(len(herbs))
    herbs = herbs[:herbs_num]

    return herbs

def herb_name_common_get(herb_slug):
    herb_name_common = ''
    try:
        herb_slug = herb_slug.replace('mentha-piperita', 'mentha-x-piperita')
        ssot_herb_primary_filepath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json'
        herb_data = io.json_read(ssot_herb_primary_filepath)
        herb_name_common = herb_data['herb_names_common'][0]['answer']
    except:
        pass
    return herb_name_common

########################################
# return ailments grouped by system
########################################
def systems_ailments_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if system_slug == cluster['system_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'system_slug': system_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

########################################
# return ailments grouped by organ
########################################
def ailments_by_organ_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if organ_slug == cluster['organ_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'organ_slug': organ_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

def organs_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    organs = []
    for ailment in ailments:
        if ailment['organ_slug'] not in organs: organs.append(ailment['organ_slug'])
    return organs

def systems_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    systems = []
    for ailment in ailments:
        if ailment['system_slug'] not in systems: systems.append(ailment['system_slug'])
    return systems

