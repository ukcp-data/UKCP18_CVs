import json, glob


def test_parsing_all_jsons():

    jsons = glob.glob("*.json")
    if len(jsons) < 5:
        jsons = glob.glob("../*.json")

    for _json in jsons:
        with open(_json) as reader:
            try:
                data = json.load(reader)
            except:
                print("FAILED TO PARSE: {0}".format(_json))


if __name__ == "__main__":

    test_parsing_all_jsons()
