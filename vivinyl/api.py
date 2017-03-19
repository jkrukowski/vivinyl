import falcon
import json
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


class ImageController(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.ses = SignatureES(self.es)

    def on_post(self, req, resp):
        data = req.bounded_stream.read()
        result = self.ses.search_image(data, all_orientations=True, bytestream=True)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)


app = falcon.API()
app.add_route('/find', ImageController())
