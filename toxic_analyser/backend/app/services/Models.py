import os
from transformers import pipeline


def qa_model(context):
    _base_path = os.path.dirname(__file__)
    qa1 = pipeline("question-answering", os.path.join(_base_path, "..",'models/trained_model_ep_1'))
    qa2 = pipeline("question-answering", os.path.join(_base_path, "..",'models/trained_model_ep_2'))
    qa3 = pipeline("question-answering", os.path.join(_base_path, "..",'models/trained_model_ep_3'))

    question = "What toxic sentence is used in this paragraph?"
    votes = {}

    m1 = qa1(context=context, question=question)

    votes[m1["answer"]] = 1

    m2 = qa2(context=context, question=question)

    if votes.get(m2["answer"]):
        votes[m2["answer"]] =+ 1
    else:
        votes[m2["answer"]] = 1

    m3 = qa3(context=context, question=question)

    print(m1, m2, m3)

    if votes.get(m3["answer"]):
        votes[m3["answer"]] =+ 1
    else:
        votes[m3["answer"]] = 1

    if len(votes.keys()) == 1:
        return list(votes.keys())[0], confirm(m1, context)
    elif m1["score"] > m2["score"]:
        
        return m1["answer"], confirm(m1, context)
    elif m2["score"] > m3["score"]:
        
        return m2["answer"], confirm(m2, context)
    else:
        
        return m3["answer"], confirm(m3, context)
    

def confirm(answer, context):
    print(len(context))
    if len(context)-1 == answer["end"]:
        if answer["score"] < 0.95:
            return False
        else: return True
    return True
                

def get_reason(context):
    _base_path = os.path.dirname(__file__)
    gpt2 = pipeline("text-generation", os.path.join(_base_path, "..",'models/gpt_model'))
    answer, score = qa_model(context)
    if score:
        return gpt2(answer, max_length=200)
    else: "No toxic statement"

if __name__ == "__main__":
    get_reason()
    qa_model()
    confirm()