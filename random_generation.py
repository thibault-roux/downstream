import random
import jiwer

# I have a reference and two corrected hypotheses that are derived from the same hypothesis.
# We know that there is exactly one modification from the hypothesis.

# For example,
# ref: ABCD
# hypA: ABED
# hypB: ABCF
# We can infer the hypothesis:
# hyp_inferred: ABEF

def WE(ref, hyp):
    return jiwer.wer(ref, hyp)*len(ref.split(" "))

def infer_hypothesis1(ref, hypA, hypB):
    # my method is to generate random ancestors until one is correct
    # the condition is that the ancestor must have one error in common with each child, i.e WE(ancestor, child) = 1

    # given a vocabulary set, generate a random sentence
    vocabulary_save = []
    for word in ref.split(" "):
        vocabulary_save.append(word)
    for word in hypA.split(" "):
        vocabulary_save.append(word)
    for word in hypB.split(" "):
        vocabulary_save.append(word)
    lenhypA = len(hypA.split(" "))
    
    
    limit = 0
    # do while
    while limit < 1000000:
        # generate random ancestor
        vocabulary = vocabulary_save.copy()
        ancestor = ""
        change = random.choice([0, 1, -1])
        for i in range(lenhypA + change):
            index = random.randint(0,len(vocabulary)-1)
            word = vocabulary.pop(index)
            ancestor += word + " "
        ancestor = ancestor[:-1]
        # check if it is correct
        ancestor_hypA = WE(ancestor, hypA)
        ancestor_hypB = WE(ancestor, hypB)
        ancestor_ref = WE(ancestor, ref)
        ref_hypA = WE(ref, hypA)
        ref_hypB = WE(ref, hypB)
        if ancestor_hypA == 1 and ancestor_hypB == 1 and ref_hypA + 1 == ancestor_ref and ref_hypB + 1 == ancestor_ref:
            print(limit)
            return ancestor
        limit += 1



def infer_hypothesis2(ref, hypA, hypB):
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
        if position > 0:
            vocab.append(hypBsplit[position-1])
        vocab.append(hypBsplit[position])
        if position < len(hypBsplit)-1:
            vocab.append(hypBsplit[position+1])
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
        hyp_hypA = WE(hyp, hypA)
        hyp_hypB = WE(hyp, hypB)
        hyp_ref = WE(hyp, ref)
        ref_hypA = WE(ref, hypA)
        ref_hypB = WE(ref, hypB)
        if hyp_hypA == 1 and hyp_hypB == 1 and ref_hypA + 1 == hyp_ref and ref_hypB + 1 == hyp_ref:
            print(limit)
            return hyp
        limit += 1


if __name__ == "__main__":
    ref = "salut tu vas bien"
    hypA = "salu tu va bien ouais"
    hypB = "salu tu vas viens ouais"
    
    # ref = "salut tu vas bien car pas moi"
    # hypA = "salu tu vas sien car pa moi"
    # hypB = "salu tu va sien car pas moi"

    # ref = "A B C D"
    # hypA = "A B E D"
    # hypB = "A B C F"
    print(infer_hypothesis2(ref, hypA, hypB))