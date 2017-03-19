import logging
import logging.config
import falcon
import json
import traceback
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES


logging.config.fileConfig('./vivinyl/logging.conf')
logger = logging.getLogger('vivinyl')

class ImageController(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.ses = SignatureES(self.es)

    def on_post(self, req, resp):
        if not req.content_length:
            raise falcon.HTTPBadRequest('Missing content', 'Please provide jpg image is POST request body')
        data = req.bounded_stream.read()
        try:
            result = self.ses.search_image(data, all_orientations=True, bytestream=True)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result)
        except Exception as e:
            logging.error(traceback.format_exc())
            raise falcon.HTTPBadRequest('Error', 'Your request cannot be processed')


app = falcon.API()
app.add_route('/find', ImageController())
