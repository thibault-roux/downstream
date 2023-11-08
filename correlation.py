from deep_translator import GoogleTranslator as Translator
import progressbar


def read_hats():
    # dataset = [{"reference": ref, "hypA": hypA, "nbrA": nbrA, "hypB": hypB, "nbrB": nbrB}, ...]
    dataset = []
    with open("datasets/hats.txt", "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line[:-1].split("\t")
            dictionary = dict()
            dictionary["reference"] = line[0]
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
        ref = dictionary["reference"]
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
            dictionary["reference"] = line[0]
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
    return 100-F1*100

def save_semdist_bertscore(verbose=True):
    # hats must have been translated

    # SemDist Sentence Camembert-large
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
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

if __name__ == '__main__':
    
    # dataset = read_hats()
    # translate_hats_and_save(dataset)
    
    dataset = load_translated_hats()
    for e in dataset:
        print(e)

    