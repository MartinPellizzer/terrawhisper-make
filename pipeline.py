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

Complete Diseases and Preparations sections wiht references in monographs

GIFT: 
    complete database with other tables
    model the tables and relationships in the pygame program

check USDA PLANTS database for morphological characteristics
check gemini for other traits datasources

parse pubmed for "compounds"
fetch/parse powo
RENDER: mention sources on a section level where appropriate 
get chemicals classes from chemical and pubchem
TRY DATASET (identification layer)
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
    import resolve_main

    # resolve_wcvp.run()
    # resolve_powo.run()
    # resolve_wikidata.run()
    # resolve_pubmed.run()
    # resolve_drduke.run()
    resolve_main.run()

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
    import observe_main

    observe_init.run()
    # observe_powo.run()
    # observe_wikidata.run()
    # observe_pubmed.run()
    # observe_drduke.run()
    observe_main.run()

if 0:
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
