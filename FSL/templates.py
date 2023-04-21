
WN18RR = [
    # none-yes/no prompt
    "If \"[SENTENCE]\", then what is the [A] part of speech?",
    "If \"[SENTENCE]\", so can you tell me the [A] POS ?",
    # "What happens next in this paragraph?\n[SENTENCE]. [A] part of speech tag is a ",
    # "Continue writing the next sentence: \n[A] part of speech tag is a \"",
    "Continue writing the next sentence in this paragraph: \"[SENTENCE]. The word [A] part of speech tag is a \"",
    "Continue writing the next sentence: \n If \"[SENTENCE]\", it does mean that word '[A]' POS is a ",
    # "Complete the next sentence:\nIn the sentence \"[SENTENCE]\". [A] part of speech tag is a ",
    "Write the next sentence in this paragraph:\nBased on the sentence \"[SENTENCE]\", we can conclude that [A] POS is a ",
    "How does the next paragraph end?\nPremise: [SENTENCE].\nGiven the premise, can we conclude this hypothesis: [A] part of speech is a",
    "What most naturally follows?\nLet's say that \"[SENTENCE]\". Now we can say that '[A]' POS is a ",
    # "What happens next?\nSentence 1: \"[SENTENCE].\"\n Sentence 2: \"[A] POS is a \"",
    # "What happens next?\nSentence 1: \"[SENTENCE].\"\n Sentence 2: \"[A] part of speech is a \"",
    # "Write the next sentence in the following story.\n[A] POS is a ",
    "Write the next sentence in the following story.\n[A] part of speech is a ",

    # yes/no question prompts
    "If \"[SENTENCE]\", does this mean that \"[A] POS is a [LABEL]\"?",
    "Based on the sentence \"[SENTENCE]\", is that sentence  \"[A] POS is a [LABEL]\" a true sentence?",
    "Premise: [SENTENCE].\nHypothesis: [A] part of speech is a '[LABEL]'.\nGiven the premise, can we conclude the hypothesis?",
    "Let's say that \"[SENTENCE]\"\nCan we now say that \"'[A]' part of speech is a [LABEL]\"?",
    "Does \"[A] POS is a [LABEL].\" appear to be an accurate statement based on \"[SENTENCE]. [A] POS is a [LABEL]\"?",
    "Sentence 1: \"[SENTENCE].\"\n Sentence 2: \"[A] part of speech is a [LABEL].\"\nIs sentence 2 true, based on sentence 1?"
]

UMLS = [
    # none-yes/no prompt
    "If \"[SENTENCE]\", then what is the [CONCEPT] in medical care?",
    "If \"[SENTENCE]\", so can you tell me the [CONCEPT] medically known for?"
    "What happens next in this paragraph?\n[SENTENCE]. [CONCEPT] is a ",
    "Continue writing the next sentence: \n[CONCEPT] in health related domain is a \"",
    "Write the next sentence in this paragraph:\nBased on the sentence \"[SENTENCE]\", we can conclude that [CONCEPT] in healthcare is a ",
    "How does the next paragraph end?\nPremise: [SENTENCE].\nGiven the premise, can we conclude this hypothesis: [CONCEPT] in medicine is a",
    "What most naturally follows?\nLet's say that \"[SENTENCE]\". Now we can say that '[CONCEPT]' in medical care is a ",

    # yes/no question prompts
    "Based on the sentence \"[SENTENCE]\", is that sentence  \"[CONCEPT] in medicine is a [LABEL]\" a true sentence?",
    "Premise: [SENTENCE].\nHypothesis: [CONCEPT] biomedically is a '[LABEL]'.\nGiven the premise, can we conclude the hypothesis?",
    "Let's say that \"[SENTENCE]\"\nCan we now say that \"'[CONCEPT]' is kind of [LABEL] in medicine\"?",
    "Does \"[CONCEPT] in medical domain is a [LABEL].\" appear to be an accurate statement based on \"[SENTENCE].\"?",
    "Sentence 1: \"[SENTENCE].\"\n Sentence 2: \"[CONCEPT] is a [LABEL] in medicine.\"\nIs sentence 2 true, based on sentence 1?"
]

GEONAMES = [
    # none-yes/no prompt
    "If \"[NAME] is localed in [COUNTRY].\", then what is the [NAME]?",
    "If \"[NAME] is a place in [COUNTRY].\", so can you tell me the [NAME] geographically known for ?",
    "What happens next in this paragraph?\n[NAME] is situated in [COUNTRY]. The [NAME] place is a ",
    "Continue writing the next sentence: \n[NAME] in [COUNTRY] is a geographical name for \"",
    "Write the next sentence in this paragraph:\nBased on the sentence \"[NAME] is a place in [COUNTRY].\", we can conclude that [NAME] is a ",
    "How does the next paragraph end?\nPremise: [NAME] is a place in [COUNTRY].\nGiven the premise, can we conclude this hypothesis: [NAME] in geography is a ",
    "What most naturally follows?\nLet's say that \"[NAME] is based in [COUNTRY]\". Now we can say that '[NAME]' geographic name is a ",

    # yes/no question prompts
    "Premise: [NAME] is based in [COUNTRY].\nHypothesis: [NAME] is a '[LABEL]'.\nGiven the premise, can we conclude the hypothesis?",
    "Let's say that \"[NAME] can be found in the [COUNTRY].\"\nCan we now say that \"'[NAME]' is a [LABEL] in geography\"?",
    "Does \"The [NAME] is known as a [LABEL].\" appear to be an accurate statement based on \"[NAME] is a place in [COUNTRY]. [NAME] is known as a [LABEL]\"?",
    "Sentence 1: \"The [NAME] is a place in [COUNTRY].\"\n Sentence 2: \"[NAME] is a [LABEL].\"\nIs sentence 2 true, based on sentence 1?"
]
