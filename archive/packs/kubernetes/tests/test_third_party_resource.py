from st2tests.base import BaseSensorTestCase

from third_party_resource import ThirdPartyResource


class ThirdPartyResourceTestCase(BaseSensorTestCase):
    sensor_cls = ThirdPartyResource

    def test_k8s_object_to_st2_trigger_bad_object(self):
        k8s_obj = {
            'type': 'kanye',
            'object': {
                'kind': 'president',
                'metadata': {
                    'name': 'west',
                    'namespace': 'westashians'
                    # uid missing
                    # label missing
                }
            }
        }
        sensor = self.get_sensor_instance()
        self.assertRaises(KeyError, sensor._k8s_object_to_st2_trigger, k8s_obj)

    def test_k8s_object_to_st2_trigger(self):
        k8s_obj = {
            'type': 'kanye',
            'object': {
                'kind': 'president',
                'metadata': {
                    'name': 'west',
                    'namespace': 'westashians',
                    'uid': 'coinye',
                    'labels': ['rapper', 'train wrecker']
                }
            }
        }
        sensor = self.get_sensor_instance()
        payload = sensor._k8s_object_to_st2_trigger(k8s_obj)
        self.assertTrue('resource' in payload)
        self.assertEqual(payload['resource'], k8s_obj['type'])
        self.assertTrue('object_kind' in payload)
        self.assertEqual(payload['object_kind'], k8s_obj['object']['kind'])
        self.assertTrue('name' in payload)
        self.assertEqual(payload['name'], k8s_obj['object']['metadata']['name'])
        self.assertTrue('labels' in payload)
        self.assertListEqual(payload['labels'], k8s_obj['object']['metadata']['labels'])
        self.assertTrue('namespace' in payload)
        self.assertEqual(payload['namespace'], k8s_obj['object']['metadata']['namespace'])
        self.assertTrue('uid' in payload)
        self.assertEqual(payload['uid'], k8s_obj['object']['metadata']['uid'])

    def test_get_trigger_payload_from_line(self):
        line = '{"object": {"kind": "president", ' + \
               '"metadata": {"labels": ["rapper", "train wrecker"], ' + \
               '"namespace": "westashians", ' + \
               '"name": "west", "uid": "coinye"}}, "type": "kanye"}'
        sensor = self.get_sensor_instance()
        payload = sensor._get_trigger_payload_from_line(line)
        self.assertTrue(payload is not None)
        self.assertTrue('resource' in payload)
        self.assertTrue('object_kind' in payload)
        self.assertTrue('name' in payload)
        self.assertTrue('labels' in payload)
        self.assertTrue('namespace' in payload)
        self.assertTrue('uid' in payload)
