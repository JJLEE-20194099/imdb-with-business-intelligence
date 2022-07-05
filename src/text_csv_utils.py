import csv
def write_csv_file(data, path, mode):
    with open(path, mode, encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if data:
            for row in data:
                if row:
                    writer.writerow(row)


def read_text_file(path, mode):
    return open(path, mode).readlines()
    
