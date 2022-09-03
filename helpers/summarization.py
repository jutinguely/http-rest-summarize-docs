from transformers import pipeline

class Summary(object):

    def __init__(self, id: int, summary: str):
        self.id = id
        self.summary = summary


class SummarizationTask(object):
    
    def __init__(self, id: int, text: str):
        self.id = id
        self.text = text
    
    def summarize(self, length: int) -> str:
        """here we call our ML pipeline that summarize our text.
            + if the text is too short then we just return it.
            + we used a OS trained model from facebook

        Args:
            length (int): this is the length of the summary from the configuration

        Returns:
            str: this is the output of the pipeline; the summary of the text
        """
        if len(self.text.split(" ")) < 20:
            return self.text
        pipe = pipeline("summarization", model="facebook/bart-large-cnn")
        answer = pipe(self.text, max_length=4*length, min_length=length)
        return answer