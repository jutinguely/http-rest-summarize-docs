from helpers.summarization import SummarizationTask, Summary
import redis 
import hashlib
import multiprocessing
import logging

class DocumentManager(object):

    def __init__(self, host: str, port: int, config: dict):
        """use one store for the text and another store for the summary
            + if persist=True then use Redis, TODO: still need to be thouroughly tested! otherwise use pyt dict
            + use two queues to pass the tasks and results such that summarize tasks are non-blocking 
            + use 4 processes in order to parallelize summarization work

        Args:
            host (str): db_hostname
            port (int): db_port
            config (dict): global configuration
        """
        self.persist = config["persist_data"]
        self.len_summary = config["length_summary"]
        if self.persist:
            self.db = redis.Redis(host=host, port=port, db=0)
            self.db_summary = redis.Redis(host=host, port=port, db=1)
        else:
            self.db = {}
            self.db_summary = {}
        self.task_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        for p in range(4):
            p = multiprocessing.Process(target=self._summarise_text, args=())
            p.start()
            print(p, "started")
    
    def _summarise_text(self):
        """we take a task from self.task_queue and call the summarize() function
            + once the summary is produced then it put the object Summary into the result queue
            + this function is parellized with 4 processes
        """
        while True:
            task = self.task_queue.get()
            summary = task.summarize(self.len_summary)
            self.result_queue.put(Summary(task.id, summary))
            print(summary, task.id)

    def _process_results(self):
        """pull result (summarized texts) from self.result_queue and store them into the self.db_summary store
        """
        while not self.result_queue.empty():
            outcome = self.result_queue.get()
            self.db_summary[outcome.id] = outcome.summary
        return

    def write_document(self, text: str) -> dict:
        """store the document in self.db KV store with hashed doc key
            + pass the text to subprocess self.task_queue in order to summarize the text (non-blocking)

        Args:
            text (str): the large text itself

        Returns:
            dict: document_id 
        """
        key = hashlib.md5(text.encode()).hexdigest()
        if key in self.db.keys():
            return {"document_id": key}
        if self.persist:
            self.db.set(key, text) 
        else:
            self.db[key] = text
        self.task_queue.put(SummarizationTask(key, text))
        return {"document_id": key}

    def load_document(self, id: str) -> dict:
        """load the document from self.db store
            + self._process_results() is called to pull into self.dev_summary the document that were summarized

        Args:
            id (str): key mapping to document text

        Returns:
            dict: text, doc_id if doc_id exists
        """
        self._process_results()
        if id not in self.db.keys():
            return {"message": "no such document"}
        return {"text": self.db[id], "id": id}

    def load_document_summary(self, id: str) -> dict:
        """load the summary from self.db_summary store

        Args:
            id (str): key mapping to document text

        Returns:
            dict: summary, doc_id if doc_id exists and summary was already produced
        """
        self._process_results()
        if id not in self.db_summary.keys():
            return {"message": "no such document or summary not produced yet"}
        return {"summary": self.db_summary[id], "id": id}

    def load_documentIds(self) -> dict:
        """load all documents ids

        Returns:
            dict: docs_ids
        """
        self._process_results()
        return {"document_ids": [k for k, v in self.db.items()]}