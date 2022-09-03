import requests
import unittest
import json
import yaml
import time 

config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
texts = json.load(open("tests/sample_texts.json"))["texts"]
SERVER_IP = f'{config["host"]}:{config["port_api"]}'

class TestEndpoints(unittest.TestCase):

    def test_write_document(self):
        url = f"http://{SERVER_IP}/store"
        payload = json.dumps({"text": texts[0]})
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        self.assertIn("9ea57fb6c560015590f6c1842d35e731", response.text)

    def test_post_4_texts_wait_and_read_summaries(self):
        print("POST 4 large texts")
        for text in texts:
            url = f"http://{SERVER_IP}/store"
            payload = json.dumps({"text": text})
            headers = {
            'Content-Type': 'application/json'
            }
            resp = requests.request("POST", url, headers=headers, data=payload)
            print("POST", resp.text)
        time.sleep(10)
        print("GET all doc ids")
        url = f"http://{SERVER_IP}/get_documentIds"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("GET", response.text)
        ids = json.loads(response.text)["document_ids"]
        self.assertEqual(len(ids), 4)
        print("GET summary directly afterwards (not enough time to process)")
        for id in ids:
            url = f"http://{SERVER_IP}/get_summary?id={id}"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)
        print("WAIT 20sec then GET summary directly afterwards (not enough time to process)")
        time.sleep(20)
        for id in ids:
            url = f"http://{SERVER_IP}/get_summary?id={id}"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)
        return




if __name__ == '__main__':
    unittest.main()