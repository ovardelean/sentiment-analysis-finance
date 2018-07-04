import os, json, sys
import config


def load_json(file_path):
    with open(file_path, 'rb') as f:
        return json.load(f)

def dump_json(data, out):
    f = open(out, 'wb')
    json.dump(data, f)
    f.close()

def dump_nice(dic, out):
    f = open(out, 'wb')
    for key in sorted(dic.keys()):
        f.write(key+":"+dic[key]+"\n")
    f.close()

def load_nice(inn):
    f = open(inn, 'rb').read()
    json_data = {}
    for line in f.split("\n"):
        if not line:
            continue
        json_data[line.split(":")[0].strip()] = line.split(":")[1].strip()
    return json_data

def dump_nice_dict():
    for dic in [config.DICT_NEGATIVE, config.DICT_POSITIVE, config.DICT_DIRECTIONALITY, config.DICT_LAGGING, config.DICT_LAGGING_REV, config.DICT_LEADING]:
        loaded = load_json(dic)
        dump_nice(loaded, os.path.join(os.path.dirname(dic), os.path.basename(dic)+".txt"))

def dump_json_dict():
    for dic in [config.DICT_NEGATIVE, config.DICT_POSITIVE, config.DICT_DIRECTIONALITY, config.DICT_LAGGING, config.DICT_LAGGING_REV, config.DICT_LEADING]:
        loaded = load_nice(dic+".txt")
        dump_json(loaded, dic)

def compare_jsons(path1, path2):
    for dic in [config.DICT_NEGATIVE, config.DICT_POSITIVE, config.DICT_DIRECTIONALITY, config.DICT_LAGGING, config.DICT_LEADING]:
        dic_name = os.path.basename(dic)
        loaded1 = load_json(os.path.join(path1, dic_name))
        loaded2 = load_json(os.path.join(path2, dic_name))
        different_keys = set()
        for key in loaded1:
            if key not in loaded2:
                different_keys.add((key, loaded1[key]))
            elif loaded1[key] != loaded2[key]:
                different_keys.add((key, loaded1[key]))
        print dic
        for dfk in different_keys:
            print dfk[0],
        print "="*50

if __name__ == "__main__":
    if sys.argv[1] == "tojson":
        dump_json_dict()
    elif sys.argv[1] == 'tonice':
        dump_nice_dict()
    elif sys.argv[1] == 'compare':
        compare_jsons(sys.argv[2], sys.argv[3])
