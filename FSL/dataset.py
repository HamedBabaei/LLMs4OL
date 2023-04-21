import templates as TEMPLATES

class BaseDataset:
    def __int__(self, templates):
        self.templates_list = templates
    def build_samples(self, dataset):
        source_text, target_text = [], []
        for data in dataset:
            for template in self.templates_list:
                if "[LABEL]" in template and data['negative']:
                    filled_template = self.fill_template(data, template)
                    source_text.append(filled_template['text'])
                    target_text.append(filled_template['label'])
                if not data['negative']:
                    filled_template = self.fill_template(data, template)
                    source_text.append(filled_template['text'])
                    target_text.append(filled_template['label'])
        return source_text, target_text

class WN(BaseDataset):
    def fill_template(self, data, template):
        template = template.replace("[A]", data['[A]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        if '[LABEL]' in template:
            template = template.replace("[LABEL]", data['[LABEL]'])
            return {"text": template, "label": data['yes-no-label']}
        return {"text": template, "label": data['[LABEL]']}

class UMLS(BaseDataset):
    def fill_template(self, data, template):
        template = template.replace("[CONCEPT]", data['[CONCEPT]'])
        template = template.replace("[SENTENCE]", data['[SENTENCE]'])
        if '[LABEL]' in template:
            template = template.replace("[LABEL]", data['[LABEL]'][0].lower())
            return {"text": template, "label": data['yes-no-label']}
        return {"text": template, "label": data['[LABEL]'][0].lower()}

class GeoNames(BaseDataset):
    def fill_template(self, data, template):
        template = template.replace("[NAME]", data['[NAME]'])
        template = template.replace("[COUNTRY]", data['[COUNTRY]'])
        if '[LABEL]' in template:
            template = template.replace("[LABEL]", data['[LABEL]'].lower())
            return {"text": template, "label": data['yes-no-label']}
        return {"text": template, "label": data['[LABEL]'].lower()}


class DatasetFactory:

    def __new__(self, dataset):
        datasets = {
            "wn18rr": [WN, TEMPLATES.WN18RR],
            "geonames": [GeoNames, TEMPLATES.GEONAMES],
            "umls": [UMLS, TEMPLATES.UMLS]
        }
        return datasets[dataset][0](templates=datasets[dataset][1])


