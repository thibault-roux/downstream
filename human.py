import jiwer
import utils.utils as utils

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
        hypB = dictionary["hypB"]
        """
        # first case
        ref = "salut tu vas bien"
        hypA = "salut tu va bien"
        hypB = "salut tu vas viens"
        # second case
        ref = "..."
        hypA = "salut tu vas viens"
        hypB = "salut tu vas biens"
        """

        # what I need : two hypothesis with a common ancestor at one correction each
        # properties :
        #   - a ancestor can only have more errors than his children
        #   - children must have two errors not in common
        if difference_wer(hypA, hypB) == 2 and difference_wer(ref, hypA) == 1 and difference_wer(ref, hypB) == 1:
            filtered_dataset.append(dictionary)
            # we have to create a basis hypothesis which have both errors from hypA and hypB
            hyp = "salut tu va viens"
            # input()
        elif difference_wer(hypA, hypB) == 1: # there is an error made on the same word
            filtered_dataset.append(dictionary)
            print(ref)
            print(hypA)
            print(hypB)
            input()
            # we have to create a basis hypothesis which have 
            # change the ref ??
    with open("datasets/filtered_hats.txt", "w", encoding="utf8") as file:
        file.write("reference\thypA\tnbrA\thypB\tnbrB\n")
        for dictionary in filtered_dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\n")
    print(len(filtered_dataset))


if __name__ == "__main__":
    ref = "salut tu vas bien"
    hyp = "salut tu va bien"
    errors, distance = utils.awer(ref.split(" "), hyp.split(" "))
    base_errors = ''.join(errors)
    print(base_errors)
    exit()

    # save_filtered_hats()