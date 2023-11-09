from deep_translator import GoogleTranslator as Translator
import progressbar

from utils.utils import corrector

# from sklearn.metrics.pairwise import cosine_similarity


def read_hats():
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open("datasets/hats.txt", "r", encoding="utf8") as file:
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

def translate_hats_and_save(dataset, verbose=True):
    translator = Translator(source='fr', target='en')
    txt = ""
    # progressbar
    if verbose:
        bar = progressbar.ProgressBar(maxval=len(dataset))
        bar.start()
        i = 0
    for dictionary in dataset:
        ref = dictionary["ref"]
        hypA = dictionary["hypA"]
        hypB = dictionary["hypB"]
        tradref = translator.translate(ref)
        tradhypA = translator.translate(hypA)
        tradhypB = translator.translate(hypB)
        txt += ref + "\t" + hypA + "\t" + tradref + "\t" + tradhypA + "\n"
        txt += ref + "\t" + hypB + "\t" + tradref + "\t" + tradhypB + "\n"

        if verbose:
            bar.update(i)
            i += 1

    with open("datasets/hats_with_translations.txt", "w", encoding="utf8") as file:
        file.write(txt)

def load_translated_hats():
    dataset = []
    with open("datasets/hats_with_translations.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["ref"] = line[0]
            dictionary["hyp"] = line[1]
            dictionary["tradref"] = line[2]
            dictionary["tradhyp"] = line[3]
            dataset.append(dictionary)
    return dataset


def semdist(ref, hyp, memory):
    model = memory
    ref_projection = model.encode(ref).reshape(1, -1)
    hyp_projection = model.encode(hyp).reshape(1, -1)
    score = cosine_similarity(ref_projection, hyp_projection)[0][0]
    return (1-score)*100 # lower is better

def bertscore(ref, hyp, memory):
    scorer = memory
    P, R, F1 = scorer.score([hyp], [ref])
    return 100-F1.numpy()[0]*100 # lower is better

def save_semdist_bertscore(verbose=True):
    # hats must have been translated

    # SemDist Sentence Camembert-large
    from sentence_transformers import SentenceTransformer
    semdist_model = SentenceTransformer('dangvantuan/sentence-camembert-large')

    # BERTScore
    from bert_score import BERTScorer
    bertscore_model = BERTScorer(lang="en")

    dataset = load_translated_hats()
    txt = ""

    if verbose:
        # progressbar
        bar = progressbar.ProgressBar(maxval=len(dataset))
        bar.start()
        i = 0
    for dictionary in dataset:
        ref = dictionary["ref"]
        hyp = dictionary["hyp"]
        tradref = dictionary["tradref"]
        tradhyp = dictionary["tradhyp"]
        semdist_score = semdist(ref, hyp, semdist_model)
        bertscore_score = bertscore(tradref, tradhyp, bertscore_model)
        txt += ref + "\t" + hyp + "\t" + tradref + "\t" + tradhyp + "\t" + str(semdist_score) + "\t" + str(bertscore_score) + "\n"

        if verbose:
            bar.update(i)
            i += 1
    
    # save data set
    with open("datasets/hats_with_semdist_bertscore.txt", "w", encoding="utf8") as file:
        file.write(txt)

def load_semdist_bertscore():
    dataset = []
    with open("datasets/hats_with_semdist_bertscore.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hyp"] = line[1]
            dictionary["tradref"] = line[2]
            dictionary["tradhyp"] = line[3]
            dictionary["semdist"] = line[4]
            dictionary["bertscore"] = line[5]
            dataset.append(dictionary)
    return dataset

def compute_correlation():
    dataset = load_semdist_bertscore()
    semdist = []
    bertscore = []
    for dictionary in dataset:
        semdist.append(float(dictionary["semdist"]))
        bertscore.append(float(dictionary["bertscore"]))
    from scipy.stats import pearsonr
    print("pearson:", pearsonr(semdist, bertscore))
    from scipy.stats import spearmanr
    print("spearman:", spearmanr(semdist, bertscore))


def correct_and_save():
    # correct word error in the hypothesis and compute the improvements
    dataset = load_semdist_bertscore()
    txt = ""
    for dictionary in dataset:
        ref = dictionary["reference"]
        hyp = dictionary["hyp"]
        tradref = dictionary["tradref"]
        tradhyp = dictionary["tradhyp"]
        semdist = float(dictionary["semdist"])
        bertscore = float(dictionary["bertscore"])
        corrections = corrector(ref, hyp) # list of possible word corrections
        txt += ref + "\t" + hyp + "\t" + tradref + "\t" + tradhyp + "\t" + str(semdist) + "\t" + str(bertscore)
        for correction in corrections:
            semdist_correction = semdist(ref, correction, semdist_model)
            bertscore_correction = bertscore(tradref, tradhyp, bertscore_model)
            txt += "\t" + correction + "," + str(semdist_correction) + "," + str(bertscore_correction)
        txt += "\n"
    with open("datasets/hats_with_corrections.txt", "w", encoding="utf8") as file:
        file.write(txt)

if __name__ == '__main__':
    
    # dataset = read_hats()
    # translate_hats_and_save(dataset)
    # save_semdist_bertscore(verbose=False)
    
    # compute_correlation()

    # correct_and_save()

    for correction in corrector("salut tu vas bien", "salut tue va vien"):
        print(correction)