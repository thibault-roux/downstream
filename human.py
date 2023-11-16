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


def get_base_errors(ref, hyp):
    errors, distance = utils.awer(ref.split(" "), hyp.split(" "))
    base_errors = ''.join(errors)
    return base_errors



def check(ref, hypA, hypB):
    # je pourrais avoir les erreurs de base et les comparer
    # ref, hypA = seees
    # ref, hypB = seese
    # hypA, hypB = eeess
    # check if the errors are the same

    refhypA = get_base_errors(ref, hypA)
    refhypB = get_base_errors(ref, hypB)
    hypAhypB = get_base_errors(hypA, hypB)
    # count the number of difference between hypA and hypB
    differences = 0
    for i in range(len(hypAhypB)):
        if hypAhypB[i] != "e":
            differences += 1
    if diffences != 2:
        return False
    

def check_base_errors(ref, hypA, hypB, base_errors_A, base_errors_B):
    # if difference_wer(hypA, hypB) == 2:
    
    if jiwer.cer(base_errors_A, base_errors_B)*len(base_errors_A) == 2:
        for i in range(len(base_errors_A)):
            if base_errors_A[i] != base_errors_B[i]:
                return True

def generate_hyp(ref, hypA, hypB, base_errors_A, base_errors_B): # TRY TO THINK ABOUT ALIGNMENT
    # I HAVE TROUBLE BECAUSE I WANT THE SAME ERROR, NOT JUST THE SAME KIND
    #
    # base_errors = base_errors_A + base_errors_B
    if len(base_errors_A) != len(base_errors_B):
        print(ref)
        print(hypA)
        print(hypB)
        print(base_errors_A)
        print(base_errors_B)
        print("different length")
        input()
    return "TEMP"
            

def save_filtered_hats(): # filter data to keep only hypothesis where there is a only two different words
    dataset = read_hats()
    filtered_dataset = []
    counter = 0
    for dictionary in dataset:
        ref = dictionary["ref"]
        hypA = dictionary["hypA"] 
        hypB = dictionary["hypB"]
        
        # first case
        ref = "salut tu vas bien"
        hypA = "salut va vienss"
        hypB = "salut vass vienxs"
        """
        # second case
        ref = "..."
        hypA = "salut tu vas viens"
        hypB = "salut tu vas biens"
        """

        # what I need: two hypothesis with a common ancestor at one correction each
        # properties:
        #   - an ancestor can only have more errors than his children
        #   - children must have two errors not in common
        #   - when an error is done, the other system must have it correct
        #   - the error in common must be the same, not only the same type (substition must be the same)
        # the hypothesis is generated according to hypotheses A and B and the reference
        
        if difference_wer(hypA, hypB) == 2:
            counter += 1
            print(hypA)
            print(hypB)
            input()
        """
        # ref = "salut tu vas bien"
        # hypA = "salut tu va bien"
        # hypB = "salut tu vas viens"
        base_errors_A = get_base_errors(ref, hypA)
        base_errors_B = get_base_errors(ref, hypB)
        if check_base_errors(ref, hypA, hypB, base_errors_A, base_errors_B):
            # print(base_errors_A, base_errors_B)
            # print(ref)
            # print(hypA)
            # print(hypB)
            hyp = generate_hyp(ref, hypA, hypB, base_errors_A, base_errors_B)
            # print(hyp)
            # input()
        # elif difference_wer(hypA, hypB) == 1: # there is an error made on the same word
        #     filtered_dataset.append(dictionary)
        #     print(ref)
        #     print(hypA)
        #     print(hypB)
        #     input()
        #     # we have to create a basis hypothesis which have 
        #     # change the ref ??
        """
    print(counter)
    exit()
    with open("datasets/filtered_hats.txt", "w", encoding="utf8") as file:
        file.write("reference\thypA\tnbrA\thypB\tnbrB\n")
        for dictionary in filtered_dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\n")
    print(len(filtered_dataset))


if __name__ == "__main__":
    save_filtered_hats()