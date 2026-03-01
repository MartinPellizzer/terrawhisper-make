import json

from lib import llm

if 0:
    prompt = f'''
        I have a website where the source context is "herbal medicine". basically "herbal medicine" is the site-wise context. give me a list of the core entities, meaning the entities that must be present to describe "herbal medicine", otherwise it will not stand by its own.
        /no_think
    '''
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

if 0:
    prompt = f'''
        I have a website where the source context is "herbal medicine". basically "herbal medicine" is the site-wise context. 
        Inside this source context, I have the following central entity: 
        "Medicinal Plants"

        Give me a list of the core attributes of this central entity, meaning the attributes that must be present to describe the central entity, otherwise it will not stand by its own. By core attributes, I mean clusters of attributes.
        /no_think
    '''
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def article_title_tag(source_context, central_entity):
    prompt = f'''
        I'm writing an article about the core entity "{central_entity}", which is for a website where the source context is "{source_context}". 
        Write the most optimized meta title tag for this article.
        The title must be an "expansion" of core entity for the source context, without going out of boundaries of the search intent.
        Reply only with the title tag.
        /no_think
    '''
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def article_h1(source_context, central_entity):
    prompt = f'''
        I'm writing an article about the core entity "{central_entity}", which is for a website where the source context is "{source_context}". 
        Write the most optimized h1 heading for this article.
        The h1 must be an "expansion" of core entity for the source context, without going out of boundaries of the search intent.
        Reply in html code.
        Reply only with the heading.
        /no_think
    '''
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def article_h1_subordinate(source_context, central_entity, brief):
    prompt = f'''
        I'm writing an article about the core entity "{central_entity}", which is for a website where the source context is "{source_context}". 
        Below i will give you one section i have to write, and i want you to write it based on koray rules and microsemantic. in specific, i need you to write the subordinate text. 
        The subordinate text must follow the brief and include the core entities to cover, must answer the implicit question an intent of the heading in the most direct, clear, detailed way possible without fluff, in about 40-60 words and 2-3 sentences. 
        Don't give me bold or italicized text. 
        Reply in html code, including the heading in the reply too.

        {brief}
        /no_think
    '''
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

if 0:
    article_title_tag(
        source_context='herbal medicine', 
        central_entity='herbal medicine',
    )

    article_h1(
        source_context='herbal medicine', 
        central_entity='herbal medicine',
    )

    article_h1_subordinate(
        source_context='herbal medicine', 
        central_entity='herbal medicine',
        brief=f'''
            h1 herbal medicine
            start with entity definition
            end by introducing the article
        ''',
    )



def attribute_clusters(source_context, central_entity):
    import textwrap
    prompt = textwrap.dedent(f'''
        I have a website where the source context is "{source_context}", which is the site-wise context. 
        One of the "central entities" of this source context is the following and I want to focus on it:
        {central_entity}
        Give me a list of the attribute clusters (sub-topics) for this specific entity, meaning the attribute clusters that must be present to describe this one, otherwise it will not stand by its own.
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    return reply

def attribute_clusters_format(source_context, central_entity, data):
    import textwrap
    prompt = textwrap.dedent(f'''
        I have the central entity "{central_entity}", in the context of "{source_context}" (site-wise source context).
        This central entity has the following attribute clusters, that you can find below.
        I want you to give me a JSON with these attribute clusters.
        Format the JSON like this:
        [
            {{"cluster_name": "insert cluster name here"}},
            {{"cluster_name": "insert cluster name here"}},
            {{"cluster_name": "insert cluster name here"}}
        ]
        Reply only with the JSON.
        The list of attribute clusters is this:
        {data}
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    json_data = json.loads(reply)
    return json_data

def seed_attribute_cluster_attribute(source_context, central_entity, data):
    import textwrap
    prompt = textwrap.dedent(f'''
        I have the central entity "{central_entity}", in the context of "{source_context}" (site-wise source context). 
        This central entity has the following attribute cluster I want to focus on:
        {data}
        Give me a list of the core attributes for this specific attribute cluster, meaning the attributes that must be present to describe this cluster, otherwise the cluster will not stand by its own.
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    return reply

def seed_attribute_cluster_sub_topics(source_context, central_entity, data):
    import textwrap
    prompt = textwrap.dedent(f'''
        I have the central entity "{central_entity}", in the context of "{source_context}" (site-wise source context). 
        This central entity has the following attribute cluster I want to focus on:
        {data}
        Give me a list of the core sub-topics for this specific attribute cluster, meaning the sub-topics that must be present to describe this cluster, otherwise the cluster will not stand by its own.
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    return reply


def central_entities_pick(source_context, central_entity, central_entities):
    import textwrap
    prompt = textwrap.dedent(f'''
        I have the core entity "herbal medicine", in the context of "herbal medicine" (site-wise source context).
        This core entity has the node "Safety & Regulatory Framework in Herbal Medicine", and i want to focus on it.
        Here's a list of the "core entity clusters" of this node, and I want you to choose the 5-7 most representative of this entity, the ones that are most specific and less likely to go out of boundaries, which i'll use to write an overview section about this entity that will ultimately link to the child page where i'll list them all and cover everything in depth.
        To be more specific, I want the core entity clusters, not the single entity instances in a cluster.
        Here's the list of "core entity clusters" to choose from:
        {central_entities}
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def central_entities_pick(source_context, central_entity, central_entities):
    import textwrap
    prompt = textwrap.dedent(f'''
            i have the core entity "Safety & Regulatory Framework", in the context of "herbal medicine" (site-wise source context). this core entity has the following sub-core entity i want to focus on:

            give me a list of the core entities for this specific sub-core entity, meaning the entities that must be present to describe this one, otherwise it will not stand by its own. don't include core entities that will be covered in the other sub-core entities listed below:
        /no_think
    ''').strip()
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

if 1:
    res = attribute_clusters(
        source_context='herbal medicine', 
        central_entity='medicinal plants',
    )
    data = attribute_clusters_format(
        source_context='herbal medicine', 
        central_entity='medicinal plants',
        data=res
    )
    '''
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[0]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[0]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[0]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[1]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[1]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[1]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[2]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[2]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[2]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[2]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[3]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[3]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[3]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[3]['cluster_name'],
    )
    '''
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[4]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='garlic',
        data=data[4]['cluster_name'],
    )
    seed_attribute_cluster_attribute(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[4]['cluster_name'],
    )
    seed_attribute_cluster_sub_topics(
        source_context='herbal medicine', 
        central_entity='medicinal plant',
        data=data[4]['cluster_name'],
    )

if 0:
    central_entities_pick(
        source_context='herbal medicine', 
        central_entity='medicinal plants',
        central_entities=res
    )

# source context
# entities
# attribute clusters
# attributes

