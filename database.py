import csv
import os

class LocalDB:
    FILES = [
        "билайн юзеры.csv",
        "государственные услуги p1.csv",
        "государственные услуги p2.csv",
        "государственные услуги p3.csv"
    ]

    @staticmethod
    def search(query):
        query = str(query).lower()
        results = []
        for file in LocalDB.FILES:
            if not os.path.exists(file):
                continue
            try:
                # Авто-определение разделителя
                delim = ';' if 'государственные' in file else ','
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f, delimiter=delim)
                    for row in reader:
                        if query in " ".join(row).lower():
                            results.append(f"📂 {file}: {' | '.join(row)}")
            except Exception as e:
                print(f"Ошибка в {file}: {e}")
        return results
