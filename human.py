import jiwer
import random
import utils.utils as utils
import progressbar

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


def WE(ref, hyp):
    return jiwer.wer(ref, hyp)*len(ref.split(" "))

def infer_hypothesis(ref, hypA, hypB):
    # instead of fully generate the hypothesis, I could start from hypothesis A and B and generate a random ancestor

    vocabulary_save = []
    for word in ref.split(" "):
        vocabulary_save.append(word)
    for word in hypA.split(" "):
        vocabulary_save.append(word)
    for word in hypB.split(" "):
        vocabulary_save.append(word)

    hypAsplit = hypA.split(" ")
    hypBsplit = hypB.split(" ")

    limit = 0
    while limit < 10000:
        hyp = hypAsplit.copy()
        # randomly delete a word, insert a word from vocabulary or substitute a word from vocabulary
        # randomly choose an operation
        operation = random.choice(["delete", "insert", "substitute"])
        # randomly choose a position
        position = random.randint(0, len(hyp)-1)
        # instead of choosing a word from vocabulary, I could choose a word in the hypothesis which is close
        # create a vocab with words from hypB[position-1], hypB[position], hypB[position+1]
        vocab = []
        try:
            if position > 0:
                vocab.append(hypBsplit[position-1])
            if position < len(hypBsplit):
                vocab.append(hypBsplit[position])
            if position < len(hypBsplit)-1:
                vocab.append(hypBsplit[position+1])
        except IndexError:
            return None
        # choose a word from vocab
        word = random.choice(vocab)
        # apply operation
        if operation == "delete":
            hyp.pop(position)
        elif operation == "insert":
            hyp.insert(position, word)
        elif operation == "substitute":
            hyp[position] = word
        hyp = " ".join(hyp)
        # check if it is correct
        try:
            hyp_hypA = WE(hyp, hypA)
            hyp_hypB = WE(hyp, hypB)
            hyp_ref = WE(hyp, ref)
            ref_hypA = WE(ref, hypA)
            ref_hypB = WE(ref, hypB)
        except ValueError:
            return None
        if hyp_hypA == 1 and hyp_hypB == 1 and ref_hypA + 1 == hyp_ref and ref_hypB + 1 == hyp_ref:
            # print(limit)
            return hyp
        limit += 1
            

def save_filtered_hats(): # filter data to keep only hypothesis where there is a only two different words
    dataset = read_hats()
    filtered_dataset = []
    counter = 0
    # progressbar
    bar = progressbar.ProgressBar(maxval=len(dataset))
    bar.start()
    i = 0
    for dictionary in dataset:
        bar.update(i)
        i += 1
        ref = dictionary["ref"]
        hypA = dictionary["hypA"]
        hypB = dictionary["hypB"]
        
        if WE(hypA, hypB) == 2:
            hyp = infer_hypothesis(ref, hypA, hypB)
            if hyp is not None:
                counter += 1
                filtered_dataset.append({"ref": ref, "hyp": hyp, "hypA": hypA, "nbrA": dictionary["nbrA"], "hypB": hypB, "nbrB": dictionary["nbrB"]})

    print(counter)
    with open("datasets/filtered_hats.txt", "w", encoding="utf8") as file:
        file.write("reference\thyp\thypA\tnbrA\thypB\tnbrB\n")
        for dictionary in filtered_dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hyp"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\n")
    print(len(filtered_dataset))


def read_filtered_hats(path="datasets/filtered_hats.txt"):
    # dataset = [{"reference": ref, "hyp": hyp, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open(path, "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["ref"] = line[0]
            dictionary["hyp"] = line[1]
            dictionary["hypA"] = line[2]
            dictionary["nbrA"] = int(line[3])
            dictionary["hypB"] = line[4]
            dictionary["nbrB"] = int(line[5])
            dataset.append(dictionary)
    return dataset


def semdist(ref, hyp, memory):
    model = memory
    ref_projection = model.encode(ref).reshape(1, -1)
    hyp_projection = model.encode(hyp).reshape(1, -1)
    score = cosine_similarity(ref_projection, hyp_projection)[0][0]
    return (1-score)*100 # lower is better

def save_improvements():
    # compute the semdist improvements of hypothesis A and B which are corrections of the hypothesis
    dataset = read_filtered_hats()
    for dictionary in dataset:
        ref = dictionary["ref"]
        hyp = dictionary["hyp"]
        hypA = dictionary["hypA"]
        hypB = dictionary["hypB"]
        nbrA = dictionary["nbrA"]
        nbrB = dictionary["nbrB"]
        dictionary["refhyp"] = semdist(ref, hyp)
        dictionary["refhypA"] = semdist(ref, hypA)
        dictionary["refhypB"] = semdist(ref, hypB)
    # save dataset
    with open("datasets/filtered_hats_improvements.txt", "w", encoding="utf8") as file:
        file.write("reference\thyp\thypA\tnbrA\thypB\tnbrB\trefhyp\trefhypA\trefhypB\n")
        for dictionary in dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hyp"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\t" + str(dictionary["refhyp"]) + "\t" + str(dictionary["refhypA"]) + "\t" + str(dictionary["refhypB"]) + "\n")

def correlation():
    pass    

if __name__ == "__main__":
    save_filtered_hats()