'''
################################################################################
# GUIDE
################################################################################

FETCH:
You start by fetching resources (datasets/studies). Some resources are used to extract plants info, others to create reference table (for fast lookup)

PARSE:
You take the fetched resources, parse them, and output json files with defined schemas. Each type of info must be formatted with the same schema across different sources. Use "parse_utils" to create coherent output functions.

NORMALIZE:
You take the parsed jsons, and add the appropriate normalized fields. For example "plant_name_scientific_raw_norm". The normalized fields are used for entity resolution.

RESOLVE:
### TODO: document "resolve"

OBSERVE:
### TODO: document "observe"

MASTERIZE:
### TODO: update masterize tables with "activities" (plants and plants_activities tables?)

### TODO: complete rest of pipeline with "activities"

'''

'''
################################################################################
# STEPS
################################################################################
fetch
parse
normalize
resolve
observe
qualify
derive
compile
render
'''

'''
fetch   > reference
resolve > masterize
'''

'''
explore
'''

'''
TODO:
add drduke data to pipeline
get chemicals classes from chemical and pubchem
'''

if 0:
    import parse_wcvp
    import parse_ipni
    import parse_powo
    import parse_wikidata
    import parse_pubmed
    import parse_drduke

    # parse_wcvp.run()
    # parse_ipni.run()
    # parse_powo.run()
    # parse_wikidata.run()
    parse_pubmed.run()
    # parse_drduke.run()

if 0:
    import normalize_wcvp
    import normalize_powo
    import normalize_wikidata
    import normalize_pubmed
    import normalize_drduke

    # normalize_wcvp.run()
    # normalize_powo.run()
    # normalize_wikidata.run()
    normalize_pubmed.run()
    # normalize_drduke.run()

if 0:
    import resolve_wcvp
    import resolve_powo
    import resolve_wikidata
    import resolve_pubmed
    import resolve_drduke

    # resolve_wcvp.run()
    # resolve_powo.run()
    # resolve_wikidata.run()
    resolve_pubmed.run()
    # resolve_drduke.run()

if 0:
    import masterize_init
    import masterize_pubmed
    import masterize_drduke
    masterize_init.run()
    masterize_pubmed.run()
    # masterize_drduke.run()

if 0:
    import observe_init
    import observe_powo
    import observe_wikidata
    import observe_pubmed
    import observe_drduke

    observe_init.run()
    # observe_powo.run()
    # observe_wikidata.run()
    observe_pubmed.run()
    # observe_drduke.run()

if 1:
    import qualify

if 1:
    import derive

if 1:
    import compile_main
    compile_main.run()

if 1:
    import render

if 0:
    import explore
