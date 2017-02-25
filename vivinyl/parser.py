import logging

logger = logging.getLogger('vivinyl')

class DataParser(object):
    def get_image_uri(self, data, num):
        images = data.get('images')
        if not images:
            logger.info('{0}: No images for release'.format(num))
            return None
        image = self.get_image(images=images, image_type='primary')
        if image is None:
            image = self.get_image(images=images, image_type='secondary')
        if image is None:
            image = images[0]
        return image.get('uri')

    def get_image(self, images, image_type):
        result = [i for i in images if i.get('type') == image_type]
        if len(result) > 0:
            return result[0]
        return None