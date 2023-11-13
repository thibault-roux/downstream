from deep_translator import GoogleTranslator as Translator
import progressbar

from utils.utils import corrector

from sklearn.metrics.pairwise import cosine_similarity


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

def compute_correlation_intrinsic_extrinsic():
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


def correct_and_save(verbose=False):
    # correct word error in the hypothesis and compute the improvements
    dataset = load_semdist_bertscore()

    # SemDist Sentence Camembert-large
    from sentence_transformers import SentenceTransformer
    semdist_model = SentenceTransformer('dangvantuan/sentence-camembert-large')

    # BERTScore
    from bert_score import BERTScorer
    bertscore_model = BERTScorer(lang="en")
    
    translator = Translator(source='fr', target='en')

    txt = ""
    if verbose:
        # progressbar
        bar = progressbar.ProgressBar(maxval=len(dataset))
        bar.start()
        i = 0
    for dictionary in dataset:
        ref = dictionary["reference"]
        hyp = dictionary["hyp"]
        tradref = dictionary["tradref"]
        tradhyp = dictionary["tradhyp"]
        semdist_score = float(dictionary["semdist"])
        bertscore_score = float(dictionary["bertscore"])
        corrections = corrector(ref, hyp) # list of possible word corrections
        txt += ref + "\t" + hyp + "\t" + tradref + "\t" + tradhyp + "\t" + str(semdist_score) + "\t" + str(bertscore_score)
        for correction in corrections:
            semdist_correction = semdist(ref, correction, semdist_model)
            tradcorrection = translator.translate(correction)
            bertscore_correction = bertscore(tradref, tradcorrection, bertscore_model)
            txt += "\t" + correction + "," + tradcorrection + "," + str(semdist_correction) + "," + str(bertscore_correction)
        txt += "\n"
        if verbose:
            bar.update(i)
            i += 1
    with open("datasets/hats_with_corrections.txt", "w", encoding="utf8") as file:
        file.write(txt)
    print("Function worked properly.")


def load_corrected_hats():
    dataset = []
    with open("datasets/hats_with_corrections.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
            dictionary["hyp"] = line[1]
            dictionary["tradref"] = line[2]
            dictionary["tradhyp"] = line[3]
            dictionary["semdist"] = line[4]
            dictionary["bertscore"] = line[5]
            dictionary["corrections"] = []
            for i in range(6, len(line)):
                dictionary["corrections"].append(line[i].split(","))
            dataset.append(dictionary)
    print(dataset[0])
    return dataset

def repair_corrected_dataset(): # does not work because it is not easy to find where the comma are really
    # load the dataset and repair it by selecting only float numbers
    with open("datasets/hats_with_corrections.txt", "r", encoding="utf8") as file:
        txt = ""
        nbrError = 0
        commaInref = 0
        commaInhyp = 0
        for line in file:
            linesplit = line[:-1].split("\t")
            ref = linesplit[0]
            hyp = linesplit[1]
            if "," in ref:
                commaInref += 1
            if "," in hyp:
                commaInhyp += 1
            corrections = linesplit[6:]
            for quadruple in corrections:
                if len(quadruple.split(",")) != 4:
                    print(line)
                    input()
                    print(quadruple)
                    nbrError += 1
        print("nbrError:", nbrError)
        print("commaInref:", commaInref)
        print("commaInhyp:", commaInhyp)
        # should check if there is a comma in references
        # I can keep the first as a real comma and the one preceding numbers?
        # also check if there are numbers in the references or hypotheses?

def load_only_improvements():
    improvements_intrinsic = []
    improvements_extrinsic = []
    dataset = load_corrected_hats()
    for dictionary in dataset:
        semdist_score = float(dictionary["semdist"])
        bertscore_score = float(dictionary["bertscore"])
        for correction in dictionary["corrections"]:
            semdist_correction = float(correction[-2])
            bertscore_correction = float(correction[-1])
            improvements_intrinsic.append(semdist_score-semdist_correction)
            improvements_extrinsic.append(bertscore_score-bertscore_correction)
    return improvements_intrinsic, improvements_extrinsic


def compute_correlation_minED_extrinsic():
    # compute correlation between the minimum edit distance and the extrinsic metric
    improvements_intrinsic, improvements_extrinsic = load_only_improvements()
    from scipy.stats import pearsonr
    print("pearson:", pearsonr(improvements_intrinsic, improvements_extrinsic))
    from scipy.stats import spearmanr
    print("spearman:", spearmanr(improvements_intrinsic, improvements_extrinsic))


if __name__ == '__main__':
    
    # dataset = read_hats()
    # translate_hats_and_save(dataset)
    # save_semdist_bertscore(verbose=False)
    # compute_correlation_intrinsic_extrinsic()
    # correct_and_save()
    # dataset = load_corrected_hats()
    # load_only_improvements()
    # compute_correlation_minED_extrinsic()