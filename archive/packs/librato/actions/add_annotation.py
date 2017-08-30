from lib import action


class AddAnnotation(action.LibratoBaseAction):
    def run(self, stream, title, description=None, start_time=None,
            end_time=None):
        # TODO: Add support for links
        data = {
            'title': title
        }

        if description:
            data['description'] = description

        if start_time:
            data['start_time'] = start_time

        if end_time:
            data['end_time'] = end_time

        return self.librato.post_annotation(name=stream, **data)
