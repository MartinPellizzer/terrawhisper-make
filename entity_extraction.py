
import spacy

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_md")

text = "Lavender is prepared via steam distillation to extract essential oils like linalool."

ner_labels = nlp.get_pipe('ner').labels
print(ner_labels)

