import jiwer

with open("corrections_traduction_semdist_bertscore.txt", "r", encoding="utf8") as file:
    for line in file:
        line = line.split("\t")
        ref = line[0]
        hyp = line[1]
        if len(ref.split(" ")) < 7 and len(hyp.split(" ")) < 7 and jiwer.wer(ref, hyp)*len(ref.split(" ")) == 3:
            print(ref)
            print(hyp)
            input()

