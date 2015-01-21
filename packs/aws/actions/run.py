from lib import action


class ActionManager(action.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        module_path = kwargs['module_path']
        del kwargs['module_path']
        if action == 'run_instances':
            kwargs['user_data'] = self.st2_user_data()
        if action == 'create_tags':
            kwargs['tags'] = self.split_tags(kwargs['tags'])
        if 'cls' in kwargs.keys():
            cls = kwargs['cls']
            del kwargs['cls']
            return self.do_method(module_path, cls, action, **kwargs)
        else:
            return self.do_function(module_path, action, **kwargs)
