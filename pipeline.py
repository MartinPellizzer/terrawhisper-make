'''
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
DOING:
complete common names of /herbs/herb pages in hero cards from wikidata?

TODO:
redo tables in observation db, use variable for tables names (because fix copy/paste errors)
!!! title tag in explorer pages
!!! explore page "popular herbs" and "recently added"
add one source name on each table row
add drduke data to pipeline
synonyms
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
    parse_wikidata.run()
    # parse_pubmed.run()
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

if 0:
    import qualify

if 0:
    import derive

if 0:
    import compile_main
    compile_main.run()

if 0:
    import render

if 0:
    import explore
