database_download_link = 'https://www.catalogueoflife.org/data/download'

def fetch_sqlite_table_name_usage():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/col/datasets'
    output_folderpath = f'{g.DATA_FOLDERPATH}/fetch/col/'
    io.folders_recursive_gen(output_folderpath)
    with open(f"{input_folderpath}/NameUsage.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            # print(f'{i}')
            print('NameUsage.tsv')
            print(json.dumps(row, indent=4))
            break

def fetch_sqlite_table_vernacular_name():
    pass

def run():
    print(f'''HERBS >> FETCH >> col''')

    start = time.perf_counter()
    fetch_sqlite_table_name_usage()
    print(f'fetch sqlite_name_usage() - execution time: ', time.perf_counter() - start)

