import sqlite3

from lib import g

def sqlite3__terra_plant_name_get(terra_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT t3.powo_name
        FROM terra_plants t1
        JOIN wikidata t2 ON t1.wikidata_id = t2.wikidata_id
        JOIN powo t3 ON t2.powo_id = t3.powo_id
        WHERE t1.terra_id = ?
    """, (terra_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def sqlite3__terra_plant_taxonomy_get(terra_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t3.powo_kingdom,
            t3.powo_phylum,
            t3.powo_class,
            t3.powo_order,
            t3.powo_family,
            t3.powo_genus,
            t3.powo_species
        FROM terra_plants t1
        JOIN wikidata t2 ON t1.wikidata_id = t2.wikidata_id
        JOIN powo t3 ON t2.powo_id = t3.powo_id
        WHERE t1.terra_id = ?
    """, (terra_id,))
    row = cur.fetchone()
    conn.close()
    return row

def sqlite3__wcvp_get(taxon_name):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM wcvp
        WHERE taxon_name = ?
    """, (taxon_name,))
    row = cur.fetchone()
    conn.close()
    return row

