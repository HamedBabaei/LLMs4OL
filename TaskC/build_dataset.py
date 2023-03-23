from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import torch
from pykeen.sampling.pseudo_type import PseudoTypedNegativeSampler
import numpy as np


def build_umls(config):
    srstre1 = [data.split("|")[:-1] for data in DataReader.load_text(config.raw_sn_re).split("\n")][:-1]
    print("SRSTRE1 size is a:", len(srstre1))

    stydef = [data.split("|")[:5]
              for data in DataReader.load_text(config.raw_sn_re_def).split("\n")
              if data.split("|")[0] == "STY"]

    isas = ['T186']

    rldef = [data.split("|")[:5]
             for data in DataReader.load_text(config.raw_sn_re_def).split("\n")
             if data.split("|")[0] == "RL" and data.split("|")[1] not in isas]

    print("STY def:", len(stydef))
    print("RL  def:", len(rldef))

    stydef_mapp = {sty[1]: index for index, sty in enumerate(stydef)}
    rev_stydef_mapp = {val: key for key, val in stydef_mapp.items()}

    sty2name = {sty[1]: sty[2] for index, sty in enumerate(stydef)}

    rldef_mapp = {rel[1]: index for index, rel in enumerate(rldef)}
    rev_rldef_mapp = {val: key for key, val in rldef_mapp.items()}
    rl2name = {rel[1]: rel[2] for index, rel in enumerate(rldef)}

    print("stydef_mapp:", len(stydef_mapp))
    print("rldef_mapp:", len(rldef_mapp))

    rel_t = list(set([rel[1] for rel in rldef]))
    sty_t = list(set([sty[1] for sty in stydef]))

    triples = []
    for triple in srstre1:
        if triple[0] in sty_t and triple[2] in sty_t and triple[1] in rel_t and triple[1] not in isas:
            triples.append(triple)

    print("TRIPLES size:", len(triples))

    triples_pos = {}
    for triple in triples:
        key = triple[0] + "-" + triple[1]
        if key not in triples_pos:
            triples_pos[key] = []
        triples_pos[key].append(triple[2])

    print("1-M sizes:", len(triples_pos))

    mapped_triples = [[stydef_mapp[triple[0]], rldef_mapp[triple[1]], stydef_mapp[triple[2]]]
                      for triple in triples]

    sampler = PseudoTypedNegativeSampler(mapped_triples=np.array(mapped_triples), num_entities=127, num_relations=53,
                                         filtered=True, filterer='python-set')
    negatives = sampler.sample(torch.tensor(mapped_triples))

    print("Negative examples:", sum(negatives[1].numpy())[0])

    # make positive examples
    dataset = []
    for h, r, t in triples:
        dataset.append({
            "h": sty2name[h],
            "r": rl2name[r],
            "t": sty2name[t],
            "label": "correct",
            "triples": [h, r, t]
        })

    print("Positive Samples:", len(dataset))

    for index in range(len(negatives[0])):
        if negatives[1][index].numpy()[0]:
            h, r, t = rev_stydef_mapp[negatives[0][index][0].numpy()[0]], \
                rev_rldef_mapp[negatives[0][index][0].numpy()[1]], \
                rev_stydef_mapp[negatives[0][index][0].numpy()[2]]
            dataset.append({
                "h": sty2name[h],
                "r": rl2name[r],
                "t": sty2name[t],
                "label": "incorrect",
                "triples": [h, r, t]
            })

    DataWriter.write_json(data=dataset, path=config.processed_sn)
    print("size of processed hierarchy in UMLS is :", len(dataset))

if __name__ == "__main__":
    KB_NAMES = {
        "umls": build_umls
    }
    for kb_name, function in KB_NAMES.items():
        CONFIG = BaseConfig().get_args(kb_name=kb_name)
        function(config=CONFIG)
