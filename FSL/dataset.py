import templates as TEMPLATES

class BaseDataset:
    def __init__(self, templates):
        self.templates_list = templates

    def build_samples(self, dataset):
        source_text, target_text = [], []
        for data in dataset:
            if data['negative']:
                continue
            if data.get('task-b', False):
                for template in self.templates_list['task-b-prompts']:
                    filled_template = self.fill_task_b_template(data, template)
                    source_text.append(filled_template['text'])
                    target_text.append(filled_template['label'])
            if data.get('task-c', False):
                for template in self.templates_list['task-c-prompts']:
                    filled_template = self.fill_task_c_template(data, template)
                    source_text.append(filled_template['text'])
                    target_text.append(filled_template['label'])
            for template in self.templates_list['completion-prompts']:
                filled_template = self.fill_completion_template(data, template)
                source_text.append(filled_template['text'])
                target_text.append(filled_template['label'])
        return source_text, target_text

    def fill_completion_template(self, data, template) -> dict:
        pass

    def fill_task_b_template(self, data, template) -> dict:
        pass

    def fill_task_c_template(self, data, template) -> dict:
        pass


class WN(BaseDataset):
    def fill_completion_template(self, data, template) -> dict:
        template = template.replace("[A]", data['[A]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        return {"text": template, "label": data['[LABEL]']}

class UMLS(BaseDataset):
    def fill_completion_template(self, data, template) -> dict:
        template = template.replace("[CONCEPT]", data['[CONCEPT]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        return {"text": template, "label": data['[LABEL]'][0].lower()}

    def fill_task_b_template(self, data, template) -> dict:
        template = template.replace("[CONCEPT]", data['[CONCEPT]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        template = template.replace("[LABEL]", data['[LABEL]'][0].lower())
        template = template.replace("[TEXT_A]", data['task-b-items']['text_a'].lower())
        template = template.replace("[TEXT_B]", data['task-b-items']['text_b'].lower())
        label = "yes" if data['task-b-items']['label'] == "correct" else "no"
        return {"text": template, "label": label}

    def fill_task_c_template(self, data, template) -> dict:
        template = template.replace("[CONCEPT]", data['[CONCEPT]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        template = template.replace("[LABEL]", data['[LABEL]'][0].lower())
        template = template.replace("[TAIL]", data['task-c-items']['t'].lower())
        template = template.replace("[HEAD]", data['task-c-items']['h'].lower())
        template = template.replace("[REL]", " ".join(data['task-c-items']['r'].lower().split("_")))
        label = "yes" if data['task-c-items']['label'] == "correct" else "no"
        return {"text": template, "label": label}

class GeoNames(BaseDataset):
    def fill_completion_template(self, data, template) -> dict:
        template = template.replace("[NAME]", data['[NAME]'])
        template = template.replace("[COUNTRY]", data['[COUNTRY]'])
        return {"text": template, "label": data['[LABEL]'].lower()}

    def fill_task_b_template(self, data, template) -> dict:
        template = template.replace("[NAME]", data['[NAME]'])
        template = template.replace("[COUNTRY]", data['[COUNTRY]'])
        template = template.replace("[LABEL]", data['[LABEL]'].lower())
        template = template.replace("[TEXT_A]", data['task-b-items']['text_a'].lower())
        template = template.replace("[TEXT_B]", data['task-b-items']['text_b'].lower())
        label = "yes" if data['task-b-items']['label'] == "correct" else "no"
        return {"text": template, "label": label}

class Schema(BaseDataset):
    def build_samples(self, dataset):
        source_text, target_text = [], []
        for data in dataset:
            for template in self.templates_list['task-b-prompts']:
                filled_template = self.fill_task_b_template(data, template)
                source_text.append(filled_template['text'])
                target_text.append(filled_template['label'])
        return source_text, target_text
    def fill_task_b_template(self, data, template) -> dict:
        template = template.replace("[TEXT_A]", data['text_a'].lower())
        template = template.replace("[TEXT_B]", data['text_b'].lower())
        label = "yes" if data['label'] == "correct" else "no"
        return {"text": template, "label": label}

class DatasetFactory:

    def __new__(self, dataset):
        datasets = {
            "wn18rr": [WN, TEMPLATES.WN18RR],
            "geonames": [GeoNames, TEMPLATES.GEONAMES],
            "umls": [UMLS, TEMPLATES.UMLS],
            "schema": [Schema, TEMPLATES.SCHEMA],
        }
        return datasets[dataset][0](templates=datasets[dataset][1])


