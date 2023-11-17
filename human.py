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

def alignment(ref, hypA, hypB):
    pass
            

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

        # another option is to generate random ancestors until one is correct

        # what I need: two hypothesis with a common ancestor at one correction each
        # properties:
        #   - an ancestor can only have more errors than his children
        #   - children must have two errors not in common
        #   - when an error is done, the other system must have it correct
        #   - the error in common must be the same, not only the same type (substition must be the same)
        # the hypothesis is generated according to hypotheses A and B and the reference
        
        # alignment
        # ref_align, hypA_align, hypB_align = alignment(ref, hypA, hypB)

        # ref <eps> salut tu vas bien car pas moi
        # hyp euh salu tu NAN NAN car pa <eps>
        # hypA <eps> salu tu vax sien car pa moi
        # hypB euh salu tu va viens car pas <eps>
        
        ref_align = ["<eps>", "salut", "tu", "vas", "bien", "car", "pas", "moi"]
        # hyp_align = ["euh", "salu", "tu", "NAN", "NAN", "car", "pa", "<eps>"]
        hypA_align = ["<eps>", "salu", "tu", "vax", "sien", "car", "pa", "moi"]
        hypB_align = ["euh", "salu", "tu", "va", "viens", "car", "pas", "<eps>"]
        # generate hypothesis
        hyp = ""
        for i in range(len(ref_align)):
            if hypA_align[i] == hypB_align[i]:
                error = hypA_align[i]
            else: # different
                if ref_align[i] == hypA_align[i]:
                    error = hypB_align[i]
                elif ref_align[i] == hypB_align[i]:
                    error = hypA_align[i]
                else:
                    break
            # add error to hypothesis
            # hyp += error + " "
        
    print(counter)
    exit()
    with open("datasets/filtered_hats.txt", "w", encoding="utf8") as file:
        file.write("reference\thypA\tnbrA\thypB\tnbrB\n")
        for dictionary in filtered_dataset:
            file.write(dictionary["ref"] + "\t" + dictionary["hypA"] + "\t" + str(dictionary["nbrA"]) + "\t" + dictionary["hypB"] + "\t" + str(dictionary["nbrB"]) + "\n")
    print(len(filtered_dataset))


if __name__ == "__main__":
    save_filtered_hats()