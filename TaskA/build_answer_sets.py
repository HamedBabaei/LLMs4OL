import time

from configuration import BaseConfig
from datahandler import DataReader, DataWriter
from src import AnswerSetGenerator
import openai_key_setter
from tqdm import tqdm
import time
def preprocessor(label_mapper, kb_name):
    chatgpt_label_mapper = {}
    if kb_name == 'wn18rr':
        for type, name in label_mapper.items():
            chatgpt_label_mapper[name.lower()] = [name.lower()]
    elif kb_name == 'geonames':
        for type, name in label_mapper.items():
            if len(type) != 1:
                chatgpt_label_mapper[name['name'].lower()] = [name['name'].lower()]
    elif kb_name == 'umls':
        for type, name in label_mapper.items():
            chatgpt_label_mapper[name[0].lower()] = [name[0].lower()]
    return chatgpt_label_mapper

if __name__ == "__main__":

    answer_set_generator = AnswerSetGenerator(model='chat-gpt')

    kb_names = ['umls', 'geonames']

    # answer_sets = answer_set_generator.generate(label="sign or symptom",
    #                                             domain="medicine",
    #                                             answer_set_no=10)
    # print(answer_sets)
    # answer_sets = eval(answer_sets)
    # processed_answer_set = []
    # for answer_set, answer_set_syns in answer_sets.items():
    #     processed_answer_set += [answer_set] + answer_set_syns
    # # exit(0)
    # 'wn18rr',
    for kb_name in kb_names:
        config = BaseConfig(version=3).get_args(kb_name=kb_name)
        label_mapper = DataReader.load_json(config.label_mapper)
        chatgpt_label_mapper = preprocessor(label_mapper=label_mapper, kb_name=kb_name)
        for label in tqdm(list(chatgpt_label_mapper.keys())):
            try:
                answer_sets = answer_set_generator.generate(label=label,
                                                            domain=config.answer_set_generator_domains,
                                                            answer_set_no=config.answer_set_generator_n)
            except:
                print("going to sleep for 40 seconds")
                time.sleep(40)
                answer_sets = answer_set_generator.generate(label=label,
                                                            domain=config.answer_set_generator_domains,
                                                            answer_set_no=config.answer_set_generator_n)

            answer_sets = eval(answer_sets)
            processed_answer_set = []
            for answer_set, answer_set_syns in answer_sets.items():
                processed_answer_set += [answer_set] + answer_set_syns

            chatgpt_label_mapper[label] += processed_answer_set
            chatgpt_label_mapper[label] = list(set(chatgpt_label_mapper[label]))

        DataWriter.write_json(data=chatgpt_label_mapper, path=config.chatgpt_label_mapper)
