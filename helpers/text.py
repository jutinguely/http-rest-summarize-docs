from transformers import pipeline

class Outcome(object):

    def __init__(self, id, summary):
        self.id = id
        self.summary = summary


class Task(object):
    
    def __init__(self, id, text):
        self.id = id
        self.text = text
    
    def summarize(self):
        if len(self.text.split(" ")) < 20:
            return self.text
        pipe = pipeline("summarization", model="facebook/bart-large-cnn")
        answer = pipe(self.text, max_length=20, min_length=20)
        print(answer)
        return answer

def summarise_text(q, q_result) -> str:
    task = q.get()
    summary = task.summarize()
    print(summary, task.id)
    q_result.put(Outcome(task.id, summary))
    return 
