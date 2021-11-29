import torch
from transformers import BertForQuestionAnswering,BertTokenizer

def get_answer(question,answer_text):
    model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
    from transformers import AutoTokenizer,pipeline
    tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
    tokenizer.encode(question,truncation=True,padding=True)
    nlp = pipeline('question-answering',model=model,tokenizer=tokenizer)
    result = nlp(question,answer_text)
    return result

def find_answer(question,answer_text):
    model = TFBertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    from transformers import BertTokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    input_ids = tokenizer.encode(question, answer_text)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)
    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1
    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a
    # Construct the list of 0s and 1s.
    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)
    # Run our example through the model.
    outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                    token_type_ids=torch.tensor([segment_ids]),
                    # The segment IDs to differentiate question from answer_text
                    return_dict=True)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    # Combine the tokens in the answer and print it out.
    answer = ' '.join(tokens[answer_start:answer_end + 1])
    return answer

def search_answer(question,text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = TFBertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


    encoding = tokenizer.encode_plus(question, text)
    input_ids, token_type_ids = encoding["input_ids"], encoding["token_type_ids"]
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))

    all_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer = ' '.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1])
    return answer

