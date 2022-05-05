from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
pipeline = SummarizationPipeline(
    model=AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python"),
    tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python", skip_special_tokens=True),
    device=0
)
code = '''with open("file.txt", "r") as in_file:\n    buf = in_file.readlines()\n\nwith open("file.txt", "w") as out_file:\n    for line in buf:\n        if line == "; Include this text\n":\n            line = line + "Include below\n"\n        out_file.write(line)''' #@param {type:"raw"}

import tokenize
import io


def pythonTokenizer(line):
    result = []
    line = io.StringIO(line)

    for toktype, tok, start, end, line in tokenize.generate_tokens(line.readline):
        if (not toktype == tokenize.COMMENT):
            if toktype == tokenize.STRING:
                result.append("CODE_STRING")
            elif toktype == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not tok == "\n") and (not tok == "    "):
                result.append(str(tok))
    return ' '.join(result)


tokenized_code = pythonTokenizer(code)
print("code after tokenization " + tokenized_code)
pipeline([tokenized_code])

