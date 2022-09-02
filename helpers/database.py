from helpers.text import summarise_text, Task
import redis 
import hashlib
import multiprocessing

class Database():

    def __init__(self, host, port, db, persist=False):
        self.persist = persist
        if self.persist:
            self.db = redis.Redis(host='localhost', port=port, db=db)
            self.db_summary = {}
        else:
            self.db = {}
            self.db_summary = {}
        self.queue = multiprocessing.Queue()
        self.summary_queue = multiprocessing.Queue()
        self.p = multiprocessing.Process(target=summarise_text, args=(self.queue, self.summary_queue))
        self.p.start()

    def write_document(self, text: str) -> dict:
        key = hashlib.md5(text.encode()).hexdigest()
        if self.persist:
            self.db.set(key, text) 
        else:
            self.db[key] = text
        self.queue.put(Task(key, text))
        return {"document_id": key}

    def load_document(self, id: str) -> dict:
        if id not in self.db.keys():
            return {"message": "no such document"}
        return {"text": self.db[id], "id": id}

    def load_document_summary(self, id: str) -> dict:
        while not self.summary_queue.empty():
            outcome = self.summary_queue.get()
            self.db_summary[outcome.id] = outcome.summary
        if id not in self.db.keys():
            return {"message": "no such document"}
        return {"summary": self.db_summary[id], "id": id}

    def load_documentIds(self) -> dict:
        return {"document_ids": [k for k, v in self.db]}