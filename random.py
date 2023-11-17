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

    # do while
    while True:
        # generate random ancestor
        ancestor = "A B C D"
        # check if it is correct
        if WE(ref, ancestor) == 0:
            break

if __name__ == "__main__":
    ref = "A B C D"
    hypA = "A B E D"
    hypB = "A B C F"
    print(infer_hypothesis(ref, hypA, hypB))