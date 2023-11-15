import jiwer

def read_hats(path="datasets/hats.txt"):
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open(path, "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["ref"] = line[0]
            dictionary["hypA"] = line[1]
            dictionary["nbrA"] = int(line[2])
            dictionary["hypB"] = line[3]
            dictionary["nbrB"] = int(line[4])
            dataset.append(dictionary)
    return dataset

def difference_wer(ref, hyp):
    return jiwer.wer(ref, hyp)*len(ref.split(" "))


def save_filtered_hats(): # filter data to keep only hypothesis where there is a only two different words
    dataset = read_hats()
    filtered_dataset = []
    for dictionary in dataset:
        ref = dictionary["ref"]
        hypA = dictionary["hypA"] 
        hypB = dictionary["nbrB"]
        if difference_wer(hypA, hypB) == 2 and difference_wer(ref, hypA) == 1 and difference_wer(ref, hypB) == 1:
            filtered_dataset.append(dictionary)
    with open("datasets/filtered_hats.txt", "w", encoding="utf8") as file:
        file.write("reference\thypA\tnbrA\thypB\tnbrB\n")
        for dictionary in filtered_dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\n")
    print(len(filtered_dataset))


if __name__ == "__main__":
    save_filtered_hats()