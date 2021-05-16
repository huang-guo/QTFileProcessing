import json
import os


def load_commodity_data(file_name):
    if not file_name:
        return
    commodity = {}
    with open(file_name)as file:
        for line in file.readlines()[3:]:
            line = line.replace('\n', '')
            line = line.replace('否', '0').replace('是', '1')
            a = line.split(',')
            a[-6] += ('0' * (19 - len(a[-6])))

            commodity[a[1]] = [a[4], a[-1], a[-6], eval(a[-5])]
    dump_json_to_file('./src/tax.json', commodity)


def dump_json_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def fix_wins_file_bug(content):
    if content.startswith(u'\ufeff'):
        content = content.encode('utf8')[3:].decode('utf8')
    return content


def load_json_from_file(file_name):
    if os.access(file_name, os.F_OK):
        file = open(file_name, encoding='utf-8')
        data = json.loads(fix_wins_file_bug(file.read()))
        file.close()
        if data:
            return data
        else:
            return {}
    else:
        return {}
