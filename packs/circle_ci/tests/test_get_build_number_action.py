import responses

from st2tests.base import BaseActionTestCase

from get_build_number import GetBuildNumberAction

__all__ = [
    'GetBuildNumberActionTestCase'
]


class GetBuildNumberActionTestCase(BaseActionTestCase):

    def test_get_base_headers(self):
        action = GetBuildNumberAction()
        self.assertTrue('Content-Type' in action._get_base_headers())
        self.assertTrue('Accept' in action._get_base_headers())

    def test_get_auth_headers(self):
        action = GetBuildNumberAction()
        setattr(action, 'config', {})
        self.assertRaises(Exception, action._get_auth_headers)
        setattr(action, 'config', {'token': 'dummy'})
        self.assertTrue('circle-token' in action._get_auth_headers())

    @responses.activate
    def test_get_build_num_project_not_found(self):
        action = GetBuildNumberAction()
        setattr(action, 'config', {'token': 'dummy'})
        responses.add(
            responses.GET, 'https://circleci.com/api/v1/project/area51',
            json={'error': 'Project not found'}, status=404
        )
        self.assertRaises(Exception, action.run,
                          vcs_revision='dhjhvjVv635r6735', project='area51')

    @responses.activate
    def test_get_build_num(self):
        action = GetBuildNumberAction()
        setattr(action, 'config', {'token': 'dummy'})
        MOCK_RESPONSE = [
            {'build_num': 373, 'vcs_revision': 'dhjhvjVv635r6735'},
            {'build_num': 372, 'vcs_revision': 'foo'}
        ]
        responses.add(
            responses.GET, 'https://circleci.com/api/v1/project/area51',
            json=MOCK_RESPONSE, status=200
        )
        self.assertEqual(373, action.run(
            vcs_revision='dhjhvjVv635r6735', project='area51')
        )
