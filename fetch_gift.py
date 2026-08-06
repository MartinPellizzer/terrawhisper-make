'''
def run():
    import os
    import time
    import requests
    import pandas as pd

    API_ENDPOINT = "https://gift.uni-goettingen.de/api/extended/index.php"
    OUTPUT_DIR = "gift_full_database"
    CHUNK_SIZE = 10000
    DELAY_SECONDS = 0.5

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    session = requests.Session()

    def download_simple_endpoint(query_name: str) -> None:
        """Download single-response endpoints."""
        file_path = os.path.join(OUTPUT_DIR, f"{query_name}.csv")
        if os.path.exists(file_path):
            print(f"[SKIP] {query_name} already exists.")
            return

        print(f"[DOWNLOADING] Query: '{query_name}'...")
        try:
            resp = session.get(API_ENDPOINT, params={"query": query_name}, timeout=60)
            resp.raise_for_status()

            # Handle 'versions' plain-text vs JSON endpoints
            if query_name == "versions":
                with open(os.path.join(OUTPUT_DIR, "version.txt"), "w") as f:
                    f.write(resp.text)
                print(f"  -> Saved text version info to {OUTPUT_DIR}/version.txt")
                return

            data = resp.json()
            if data:
                pd.DataFrame(data).to_csv(file_path, index=False)
                print(f"  -> Saved {len(data)} rows to {file_path}")
        except Exception as e:
            print(f"  [ERROR] Failed to fetch {query_name}: {e}")
        time.sleep(DELAY_SECONDS)


    def download_paginated_endpoint(query_name: str, out_filename: str = None) -> None:
        """Paginate through endpoints requiring chunking (species, checklists, etc.)."""
        filename = out_filename or f"{query_name}.csv"
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(file_path):
            print(f"[SKIP] {filename} already exists.")
            return

        print(f"[DOWNLOADING] Paginated Query: '{query_name}'...")
        records, start_at = [], 0

        while True:
            params = {"query": query_name, "startat": start_at, "limit": CHUNK_SIZE}
            try:
                resp = session.get(API_ENDPOINT, params=params, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                if not data:
                    break
                records.extend(data)
                print(f"  Fetched {len(records)} records...")
                if len(data) < CHUNK_SIZE:
                    break
                start_at += CHUNK_SIZE
                time.sleep(DELAY_SECONDS)
            except Exception as e:
                print(f"  [ERROR] Stopped at offset {start_at}: {e}")
                break

        if records:
            pd.DataFrame(records).to_csv(file_path, index=False)
            print(f"  -> Saved {len(records)} total rows to {file_path}")


    def download_all_functional_traits() -> None:
        """Download all ~109 trait files individually into a subfolder."""
        traits_dir = os.path.join(OUTPUT_DIR, "traits")
        os.makedirs(traits_dir, exist_ok=True)

        meta_file = os.path.join(OUTPUT_DIR, "traits_meta.csv")
        if os.path.exists(meta_file):
            traits_meta = pd.read_csv(meta_file).to_dict(orient="records")
        else:
            meta_resp = session.get(API_ENDPOINT, params={"query": "traits_meta"})
            traits_meta = meta_resp.json()
            pd.DataFrame(traits_meta).to_csv(meta_file, index=False)

        trait_ids = [t["Lvl3"] for t in traits_meta if "Lvl3" in t]
        print(f"[TRAITS] Found {len(trait_ids)} trait categories to process.")

        for idx, tid in enumerate(trait_ids, start=1):
            file_path = os.path.join(traits_dir, f"trait_{tid.replace('.', '_')}.csv")
            if os.path.exists(file_path):
                continue

            print(f"  [{idx}/{len(trait_ids)}] Fetching Trait ID: {tid}...")
            records, start_at = [], 0
            while True:
                params = {"query": "traits", "traitid": tid, "startat": start_at, "limit": CHUNK_SIZE}
                resp = session.get(API_ENDPOINT, params=params, timeout=60)
                data = resp.json()
                if not data:
                    break
                records.extend(data)
                start_at += CHUNK_SIZE
                time.sleep(DELAY_SECONDS)

            if records:
                pd.DataFrame(records).to_csv(file_path, index=False)



    print("=== STARTING FULL GIFT DATABASE EXTRACTION ===")

    # 1. Standard Metadata Endpoints (Includes fixed versions handling)
    metadata_endpoints = ["taxonomy", "lists", "regions", "references", "env_misc", "env_raster", "versions"]
    for endpoint in metadata_endpoints:
        download_simple_endpoint(endpoint)

    # 2. Large Paginated Master Tables (Includes species & missing checklists occurrences)
    download_paginated_endpoint("species")
    download_paginated_endpoint("checklists", out_filename="checklists_occurrences.csv")

    # 3. All Functional Traits (109 categories)
    download_all_functional_traits()

    print("\n=== FULL DATABASE EXTRACTION COMPLETE ===")
    print(f"All files saved into: '{OUTPUT_DIR}'")

'''

import os
import time
import requests
import pandas as pd

API_ENDPOINT = "https://gift.uni-goettingen.de/api/extended/index.php"
OUTPUT_DIR = "gift_full_database"
CHECKLIST_DIR = os.path.join(OUTPUT_DIR, "checklists")
DELAY_SECONDS = 0.2

os.makedirs(CHECKLIST_DIR, exist_ok=True)
session = requests.Session()

# Load list IDs from your previously saved lists.csv
lists_file = os.path.join(OUTPUT_DIR, "lists.csv")
if not os.path.exists(lists_file):
    print("Error: lists.csv not found. Please run the metadata download step first.")
    exit(1)

lists_df = pd.read_csv(lists_file)
# GIFT uses 'ID' or 'list_id' as the column name
list_ids = lists_df["ID"].tolist() if "ID" in lists_df.columns else lists_df.iloc[:, 0].tolist()

print(f"Found {len(list_ids)} regional checklists to download.")

for idx, list_id in enumerate(list_ids, start=1):
    file_path = os.path.join(CHECKLIST_DIR, f"checklist_{list_id}.csv")
    if os.path.exists(file_path):
        continue

    try:
        resp = session.get(API_ENDPOINT, params={"query": "checklists", "listid": list_id}, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data:
            pd.DataFrame(data).to_csv(file_path, index=False)
            
        if idx % 100 == 0 or idx == len(list_ids):
            print(f"[{idx}/{len(list_ids)}] Processed list ID {list_id}...")

    except Exception as e:
        print(f"Error downloading list {list_id}: {e}")

    time.sleep(DELAY_SECONDS)

print("\nAll regional checklist occurrences downloaded successfully!")
