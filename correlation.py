from translate import Translator


def read_hats():
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open("datasets/hats.txt", "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hypA"] = line[1]
            dictionary["nbrA"] = int(line[2])
            dictionary["hypB"] = line[3]
            dictionary["nbrB"] = int(line[4])
            dataset.append(dictionary)
    return dataset

def translate_hats_and_save(dataset, translator):
    txt = ""
    for dictionary in dataset:
        ref = dictionary["reference"]
        hypA = dictionary["hypA"]
        hypB = dictionary["hypB"]
        tradref = translator.translate(ref)
        tradhypA = translator.translate(hypA)
        tradhypB = translator.translate(hypB)
        txt += ref + "\t" + hypA + "\t" + tradref + "\t" + tradhypA + "\n"
        txt += ref + "\t" + hypB + "\t" + tradref + "\t" + tradhypB + "\n"
        break

    with open("datasets/hats_with_translations.txt", "w", encoding="utf8") as file:
        file.write(txt)

def load translated_hats():
    dataset = []
    with open("datasets/hats_with_translations.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hyp"] = line[1]
            dictionary["tradref"] = line[2]
            dictionary["tradhyp"] = line[3]
            dataset.append(dictionary)
    return dataset

if __name__ == '__main__':

    translator = Translator(from_lang="fr", to_lang="en")
    
    dataset = read_hats()
    translate_hats_and_save(dataset, translator)
    dataset = load_translated_hats()
    print(dataset)