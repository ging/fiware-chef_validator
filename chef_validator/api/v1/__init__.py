import routes

from chef_validator.api.v1 import actions
from chef_validator.common import wsgi


class API(wsgi.Router):
    """
    WSGI router for chef_validator v1 ReST API requests.
    """

    def __init__(self, conf, **local_conf):
        self.conf = conf
        mapper = routes.Mapper()
        actions_resource = actions.create_resource()
        mapper.connect('/recipes', controller=actions_resource, action='validate', conditions={'method': ['POST']})
        super(API, self).__init__(mapper)
