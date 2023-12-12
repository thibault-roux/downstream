from bert_score import BERTScorer
from sentence_transformers import SentenceTransformer
import jiwer
from sklearn.metrics.pairwise import cosine_similarity


def finder():
    with open("corrections_traduction_semdist_bertscore.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line.split("\t")
            ref = line[0]
            hyp = line[1]
            if len(ref.split(" ")) < 7 and len(hyp.split(" ")) < 7 and jiwer.wer(ref, hyp)*len(ref.split(" ")) == 3:
                print(ref)
                print(hyp)
                input()


def bertscore(ref, hyp, memory):
    scorer = memory
    P, R, F1 = scorer.score([hyp], [ref])
    return 1-F1.numpy()[0] # lower is better

def semdist(ref, hyp, memory):
    model = memory
    ref_projection = model.encode(ref).reshape(1, -1)
    hyp_projection = model.encode(hyp).reshape(1, -1)
    score = cosine_similarity(ref_projection, hyp_projection)[0][0]
    return (1-score) # lower is better




if __name__ == "__main__":
    # finder()

    model_translation = BERTScorer(lang="fr")
    model_transcription = SentenceTransformer('dangvantuan/sentence-camembert-large')

    reference_transcription = "à nos résultats"
    reference_translation = "to our results"

    corrected_hyp_transcription = ["un non résultat", "à non résultat", "un nos résultat", "un non résultats"]
    corrected_hyp_translation = ["a no result", "to no result", "a our result", "to no results"]

    print()
    for i in range(len(corrected_hyp_transcription)):
        print("Hypothese:", corrected_hyp_transcription[i])
        print("Corrected Hypothese:", corrected_hyp_translation[i])
        print("SemDist:", semdist(reference_transcription, corrected_hyp_transcription[i], model_transcription))
        print("BERTScore:", bertscore(reference_translation, corrected_hyp_translation[i], model_translation))
        print()
        input()