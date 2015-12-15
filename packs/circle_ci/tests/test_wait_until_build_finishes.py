import responses

from st2tests.base import BaseActionTestCase

from wait_until_build_finishes import WaitUntilBuildFinishes

__all__ = [
    'WaitUntilBuildFinishesActionTestCase'
]


class WaitUntilBuildFinishesActionTestCase(BaseActionTestCase):

    @responses.activate
    def test_bad_build_number(self):
        action = WaitUntilBuildFinishes()
        setattr(action, 'config', {'token': 'dummy'})
        test_build_num = 373
        MOCK_RESPONSE = {'error': 'Build not found'}
        MOCK_URL = ('https://circleci.com/api/v1/project/area51/%s' %
                    str(test_build_num))
        responses.add(
            responses.GET,
            MOCK_URL,
            json=MOCK_RESPONSE,
            status=404)
        self.assertRaises(Exception, action.run,
                          build_number=373, project='area51')

    @responses.activate
    def test_timeout_fails_action(self):
        action = WaitUntilBuildFinishes()
        setattr(action, 'config', {'token': 'dummy'})
        test_build_num = 373
        MOCK_RESPONSE = {'lifecycle': 'Running'}
        MOCK_URL = ('https://circleci.com/api/v1/project/area51/%s' %
                    str(test_build_num))
        responses.add(
            responses.GET,
            MOCK_URL,
            json=MOCK_RESPONSE,
            status=200)
        TEST_TIMEOUT = 0.2
        try:
            action.run(build_number=373, project='area51',
                       wait_timeout=TEST_TIMEOUT)
            self.assertFail('Action should have failed.')
        except Exception as e:
            expected_msg = ('Build did not complete within %s seconds.' %
                            TEST_TIMEOUT)
            self.assertEqual(expected_msg, e.message)

    @responses.activate
    def test_happy_case(self):
        action = WaitUntilBuildFinishes()
        setattr(action, 'config', {'token': 'dummy'})
        test_build_num = 373
        MOCK_RESPONSE = {'lifecycle': 'finished'}
        MOCK_URL = ('https://circleci.com/api/v1/project/area51/%s' %
                    str(test_build_num))
        responses.add(
            responses.GET,
            MOCK_URL,
            json=MOCK_RESPONSE,
            status=200)
        ret = action.run(build_number=373, project='area51',
                         wait_timeout=1)
        self.assertEqual(ret, True)
