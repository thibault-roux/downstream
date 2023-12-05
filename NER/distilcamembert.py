from transformers import pipeline

ner = pipeline(
    task='ner',
    model="cmarkea/distilcamembert-base-ner",
    tokenizer="cmarkea/distilcamembert-base-ner",
    aggregation_strategy="simple"
)

text = "dimanche soir philippe dufreigne était présent à marseille"
ners = ner(text)

# [{'entity_group': 'PER', 'score': 0.9983209, 'word': 'philippe dufreigne', 'start': 13, 'end': 32}, {'entity_group': 'LOC', 'score': 0.9797207, 'word': 'marseille', 'start': 48, 'end': 58}]


# convert a list of NER entities into a list of BIO tags
def convert_to_bio(ners, text):
    bio_tags = ['O'] * len(text.split())

    for ner_entity in ners:
        entity_group = ner_entity['entity_group']
        start_token = ner_entity['start']
        end_token = ner_entity['end']

        # Convert entity start and end indices to token indices
        start_token_index = len(text[:start_token].split())
        end_token_index = len(text[:end_token].split())

        # Assign BIO tags to the tokens
        if start_token_index < len(bio_tags):
            bio_tags[start_token_index] = f'B-{entity_group}'

        for i in range(start_token_index + 1, min(end_token_index + 1, len(bio_tags))):
            bio_tags[i] = f'I-{entity_group}'

    return " ".join(bio_tags)

# Example usage
bio_tags = convert_to_bio(ners, text)
print(bio_tags)
