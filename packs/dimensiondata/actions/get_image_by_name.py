from lib import actions

__all__ = [
    'GetImageByNameAction',
]


class GetImageByNameAction(actions.BaseAction):

    def run(self, region, location, image_name):
        driver = self._get_compute_driver(region)
        location = driver.ex_get_location_by_id(location)
        images = driver.list_images(location=location)
        image = list(filter(lambda x: x.name == image_name,
                            images))[0]
        return self._format_response_obj(image)
