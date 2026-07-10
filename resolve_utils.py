import sqlite3

from lib import g

def sqlite3__wcvp_get(taxon_name):
    DB_PATH = f'{g.SSOT_FOLDERPATH}/datasets/powo/wcvp/wcvp.db'
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM wcvp
        WHERE LOWER(taxon_name) = LOWER(?)
    """, (taxon_name,))
    row = cur.fetchone()
    conn.close()
    return row

def resolve_chemical(normalized_name):
    conn = sqlite3.connect(f"{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/pubchem/pubchem_cid_synonyms.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cid, alias, normalized_alias
        FROM compound_alias
        WHERE normalized_alias = ?
        LIMIT 1
    """, (normalized_name,))
    result = cursor.fetchone()
    conn.close()
    return result if result else None

