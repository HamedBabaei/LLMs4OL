from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
from configs import BaseConfig
import argparse
from datareader import DataReader
from dataset import DatasetFactory
from transformers import DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments


def preprocess_function(sample, padding="max_length"):
    inputs = [item for item in sample["text"]]

    # tokenize inputs
    model_inputs = TOKENIZER(inputs, max_length=CONFIG.max_source_length, padding=padding, truncation=True)

    # tokenize targets
    labels = TOKENIZER(text_target=sample["label"], max_length=CONFIG.max_target_length, padding=padding, truncation=True)

    # If we are padding here, replace all tokenizer.pad_token_id in the
    # labels by -100 when we want to ignore padding in the loss.
    if padding == "max_length":
        labels["input_ids"] = [
            [(l if l != TOKENIZER.pad_token_id else -100) for l in label] for label in labels["input_ids"]
        ]
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb_name", required=True)
    parser.add_argument("--model_to_train", required=True)
    parser.add_argument("--num_train_epochs", type=int, default=15)

    args = parser.parse_args()
    print("args:", args)
    CONFIG = BaseConfig().get_args(kb_name=args.kb_name, model_to_train=args.model_to_train)

    # loading dataset
    dataset_json = DataReader.load_json(path=CONFIG.fsl_train_data)

    source_text, target_text = DatasetFactory(dataset=args.kb_name).build_samples(dataset=dataset_json)
    dataset = DatasetDict({'train': Dataset.from_dict({'label': target_text, 'text': source_text})})

    TOKENIZER = AutoTokenizer.from_pretrained(CONFIG.model_input_path)
    tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=["text", "label"])
    MODEL = AutoModelForSeq2SeqLM.from_pretrained(CONFIG.model_input_path, device_map='auto')

    # we want to ignore tokenizer pad token in the loss
    data_collator = DataCollatorForSeq2Seq(
        TOKENIZER,
        model=MODEL,
        label_pad_token_id=CONFIG.label_pad_token_id,
        pad_to_multiple_of=8
    )

    training_args = Seq2SeqTrainingArguments(
        output_dir=CONFIG.output_log_dir,
        auto_find_batch_size=CONFIG.auto_find_batch_size,
        learning_rate=CONFIG.learning_rate,
        num_train_epochs=args.num_train_epochs,
        logging_dir=f"{CONFIG.output_log_dir}/logs",
        logging_strategy="steps",
        logging_steps=500,
        save_strategy="no",
        report_to="tensorboard"
    )

    # Create Trainer instance
    TRAINER = Seq2SeqTrainer(
        model=MODEL,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_dataset["train"]
    )

    MODEL.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    print(TRAINER.train())

    print("SAVING MODEL ..... ")
    TRAINER.save_model(CONFIG.model_output_path)
    TOKENIZER.save_pretrained(CONFIG.model_output_path)
    print("MODEL trained and saved into:", CONFIG.model_output_path)
