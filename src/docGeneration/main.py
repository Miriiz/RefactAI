from src.utils.function import *

pipeline = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python"),
    tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python",
                                            skip_special_tokens=True))
code = getFunctFromFile(os.path.dirname(__file__))

x = []
code_token = []
for c in code:
    tokenized_code = pythonTokenizer(c)
    code_token.append( tokenized_code)
    x.append(pipeline([tokenized_code]))