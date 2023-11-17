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

def infer_hypothesis(ref, hypA, hypB):
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

if __name__ == "__main__":
    ref = "salut tu vas bien"
    hypA = "salu tu va bien ouais"
    hypB = "salu tu vas viens ouais"
    print(infer_hypothesis(ref, hypA, hypB))