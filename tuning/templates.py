
WN18RR = {
    "completion-prompts":["If \"[SENTENCE]\", then what is the [A] part of speech?",
                          "If \"[SENTENCE]\", so can you tell me the [A] POS ?",
                          "Continue writing the next sentence in this paragraph: \"[SENTENCE]. The word [A] part of speech tag is a \"",
                          "Continue writing the next sentence: \n If \"[SENTENCE]\", it does mean that word '[A]' POS is a ",
                          "Write the next sentence in this paragraph:\nBased on the sentence \"[SENTENCE]\", we can conclude that [A] POS is a ",
                          "How does the next paragraph end?\nPremise: [SENTENCE].\nGiven the premise, can we conclude this hypothesis: [A] part of speech is a",
                          "What most naturally follows?\nLet's say that \"[SENTENCE]\". Now we can say that '[A]' POS is a ",
                          "Write the next sentence in the following story.\n[A] part of speech is a "]
}

UMLS = {
    "completion-prompts":["If \"[SENTENCE]\", then what is the [CONCEPT] in medical care?",
                          "If \"[SENTENCE]\", so can you tell me the [CONCEPT] medically known for?"
                          "What happens next in this paragraph?\n[SENTENCE]. [CONCEPT] is a ",
                          "Continue writing the next sentence: \n[CONCEPT] in health related domain is a \"",
                          "Write the next sentence in this paragraph:\nBased on the sentence \"[SENTENCE]\", we can conclude that [CONCEPT] in healthcare is a ",
                          "How does the next paragraph end?\nPremise: [SENTENCE].\nGiven the premise, can we conclude this hypothesis: [CONCEPT] in medicine is a",
                          "What most naturally follows?\nLet's say that \"[SENTENCE]\". Now we can say that '[CONCEPT]' in medical care is a "],

    "task-b-prompts":[
            # text_b = child, text_a=parent   [text_a, text_b]
            # {"placeholder": "text_a"} is a supertype of {"placeholder": "text_b"}.
            "Based on the sentence \"[SENTENCE]. Also, the [CONCEPT] is a [LABEL] in medicine domain.\", is that sentence \"[TEXT_A] a supertype of [TEXT_B]\" a true sentence?",
            # {"placeholder": "text_b"} is a subtype of {"placeholder": "text_a"}.
            "Premise: [SENTENCE].\nHypothesis: [CONCEPT] biomedically is a '[LABEL]' which we can hypothesis [TEXT_B] as a subtype of [TEXT_A].\nGiven the premise, can we conclude the hypothesis?",
            # {"placeholder": "text_a"} is an ancestor class of {"placeholder": "text_b"}.
            "Does \"[TEXT_A] is an ancestor class of [TEXT_B].\" appear to be an accurate statement based on \"[SENTENCE]. [CONCEPT] in medical domain is a [LABEL].\"?",
            # {"placeholder": "text_b"} is a child class of {"placeholder": "text_a"}.
            "Let's say that \"[SENTENCE]\"\nCan we now say that \"'[CONCEPT]' is kind of [LABEL] in medicine where [TEXT_B] is child class of [TEXT_A]\"?",
            # {"placeholder": "text_b"} is a subclass of {"placeholder": "text_a"}.
            "Sentence 1: \"[SENTENCE]. [CONCEPT] is a [LABEL] in medicine.\"\n Sentence 2: \"[TEXT_B] is a subclass of [TEXT_A].\"\nIs sentence 2 true, based on sentence 1?"],

    "task-c-prompts":[
            # h = LABEL or t=PARENT | t=PARENT or h=LABEL   [head, tail, rel]
            "Based on the sentence \"[SENTENCE]. Also, the [CONCEPT] is a [LABEL] in medicine domain.\", is that sentence \"[HEAD] has a [REL] relation with [TAIL]\" a true sentence?",
            "Premise: [SENTENCE].\nHypothesis: [CONCEPT] biomedically is a '[LABEL]' as well as [TAIL] is [REL] [HEAD].\nGiven the premise, can we conclude the hypothesis?",
            "Does \"[HEAD] is in [REL] type of relation with [TAIL].\" appear to be an accurate statement based on \"[SENTENCE]. [CONCEPT] in medical domain is a [LABEL].\"?",
            "Let's say that \"[SENTENCE]\"\nCan we now say that \"'[CONCEPT]' is kind of [LABEL] in medicine where [TAIL] is [REL] [HEAD]\"?"
    ],
}

GEONAMES = {
    "completion-prompts":["If \"[NAME] is a place in [COUNTRY].\", so can you tell me the [NAME] geographically known for ?",
                          "Continue writing the next sentence: \n[NAME] in [COUNTRY] is a geographical name for \"",
                          "How does the next paragraph end?\nPremise: [NAME] is a place in [COUNTRY].\nGiven the premise, can we conclude this hypothesis: [NAME] in geography is a ",
                          "What most naturally follows?\nLet's say that \"[NAME] is based in [COUNTRY]\". Now we can say that '[NAME]' geographic name is a "],


    "task-b-prompts":[
        # text_b = child, text_a=parent   [text_a, text_b]
        # {"placeholder": "text_a"} is a supertype of {"placeholder": "text_b"}.
        "Based on the sentence \"[NAME] is located in [COUNTRY]. Also, the [NAME] is a [LABEL] in geography.\", is that sentence \"[TEXT_A] a supertype of [TEXT_B]\" a true sentence?",
        # {"placeholder": "text_b"} is a subtype of {"placeholder": "text_a"}.
        "Premise: [NAME] is based in [COUNTRY].\nHypothesis: [NAME] is a '[LABEL]' which we can hypothesis [TEXT_B] as a subtype of [TEXT_A].\nGiven the premise, can we conclude the hypothesis?",
        # {"placeholder": "text_a"} is an ancestor class of {"placeholder": "text_b"}.
        "Does \"[TEXT_A] is an ancestor class of [TEXT_B].\" appear to be an accurate statement based on \"[NAME] is a place in [COUNTRY]. [NAME] is known as a [LABEL].\"?",
        # {"placeholder": "text_b"} is a child class of {"placeholder": "text_a"}.
        "Let's say that \"[NAME] can be found in the [COUNTRY].\"\nCan we now say that \"'[NAME]' is a [LABEL] as well as [TEXT_B] is a child class of [TEXT_A] in geography\"?",
        # {"placeholder": "text_b"} is a subclass of {"placeholder": "text_a"}.
        "Sentence 1: \"The [NAME] is a place in [COUNTRY] and [NAME] is a [LABEL].\"\n Sentence 2: \"[TEXT_B] is a subclass of [TEXT_A].\"\nIs sentence 2 true, based on sentence 1?"]
}

SCHEMA = {
    "task-b-prompts":[
                # text_b = child, text_a=parent   [text_a, text_b]
                # {"placeholder": "text_a"} is a supertype of {"placeholder": "text_b"}.
                "Is that sentence \"[TEXT_A] a supertype of [TEXT_B]\" a true sentence?",
                # {"placeholder": "text_b"} is a subtype of {"placeholder": "text_a"}.
                "Premise: [TEXT_B] has all the properties of [TEXT_A] .\nHypothesis: we can hypothesis [TEXT_B] as a subtype of [TEXT_A].\nGiven the premise, can we conclude the hypothesis?",
                # {"placeholder": "text_a"} is an ancestor class of {"placeholder": "text_b"}.
                "Does \"[TEXT_A] is an ancestor class of [TEXT_B].\" appear to be an accurate statement?",
                # {"placeholder": "text_b"} is a child class of {"placeholder": "text_a"}.
                "Can we say that \"[TEXT_B] is child class of [TEXT_A]\"?",
                # {"placeholder": "text_b"} is a subclass of {"placeholder": "text_a"}.
                "Sentence 1: \"[TEXT_B] contain all features of [TEXT_A].\"\n Sentence 2: \"[TEXT_B] is a subclass of [TEXT_A].\"\nIs sentence 2 true, based on sentence 1?"],

}