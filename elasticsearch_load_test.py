import json
from locust import HttpUser, task, between
from functools import lru_cache
from query_generator import QueryGenerator
from pprint import pprint

class ElasticsearchUser(HttpUser):
    wait_time = between(1, 2)
    host = 'http://localhost:9201/'

    BASE_QUERY_FILE = 'doi_es_query.json'
    DATA_QUERIES_FILE = 'research_data_queries.csv'
    # Load the doi_es_query.json file
    @lru_cache(maxsize=1)
    def base_query(self):
        with open(self.BASE_QUERY_FILE, 'r') as f:
            return json.load(f)

    # initialize the values of BASE_QUERY with the on_start method
    def on_start(self):
        self.query_generator = QueryGenerator(self.DATA_QUERIES_FILE)


    def get_randomized_query_params(self):
        query = self.query_generator.get_random_query()
        # pprint(query["Query"])
        return self.search_for(query["Query"])

    def search_for(self, query_string):
        query_params = self.base_query().copy()
        query_params["query"]["bool"]["must"][0]["query_string"]["query"] = query_string
        return query_params

    @task
    def send_elasticsearch_query(self):
        query_params = self.get_randomized_query_params()
        self.client.post('dois/_search', json=query_params)
