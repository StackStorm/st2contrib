import sys, os, time, json, logging
import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceType
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.address import Address

interval = 20

class EC2(object):

    __access_key_id = None
    __secret_access_key = None
    __region = None
    __conn = None
    __debug = False

    def __init__(self,conf):

      try:
        config_file = os.path.join(os.path.dirname(__file__), conf)
        fh = open(config_file)
        config = json.load(fh)
        fh.close()
      except Exception, e:
        print "Error reading config file %s: %s" % (conf,e)

      self.__access_key_id = config['access_key_id']
      self.__secret_access_key = config['secret_access_key']
      self.__region = config['region']
      self.connect(self.__region)

    def setup(self,debug):
      self.__debug = debug

    def connect(self,region):
        try:
          self.__conn = boto.ec2.connect_to_region(region,
           aws_access_key_id=self.__access_key_id,
           aws_secret_access_key=self.__secret_access_key)
        except Exception, e:
          print "Error connecting to EC2 region: %s" % region

    def getInstanceDetails(self,instance_id=None):
        if self.__debug == True: print instance_id
        payload = {}
        try:
          instances = self.__conn.get_only_instances()
          for i in instances:
            instance_payload = {}
            instance_payload['instance_type'] = i.instance_type
            instance_payload['launch_time'] = i.launch_time
            instance_payload['tags'] = i.tags
            instance_payload['image_id'] = i.image_id
            instance_payload['ip_address'] = i.ip_address
            instance_payload['state'] = i.state
            instance_payload['state_code'] = i.state_code
            if instance_id is None or instance_id == i.id:
              payload[i.id] = instance_payload
          if self.__debug == True: print payload
        except Exception, e:
           print "Exception %s" % e
        return payload

    def getVolumeDetails(self,vol_id):
        payload = {}
        try:
          volumes = self.__conn.get_all_volumes()
          for v in volumes:
            v_payload = {}
            v_payload['create_time'] = v.create_time
            v_payload['region'] = v.region.name
            v_payload['size'] = v.size
            v_payload['status'] = v.status
            v_payload['tags'] = v.tags
            v_payload['type'] = v.type
            v_payload['attach_time'] = v.attach_data.attach_time
            v_payload['device_map'] = v.attach_data.device
            v_payload['instance_id'] = v.attach_data.instance_id
            if vol_id is None or vol_id == v.id:
              payload[v.id] = v_payload
          if self.__debug == True: print payload
        except Exception, e:
          print "Exception %s" %e
          sys.exit(2)
        return payload

    def getAMI(self,ami=None,owner=None):
      image_list = {}
      try:
        images = self.__conn.get_all_images(owners=strToList(owner))
        for i in images:
          image_data = {}
          image_data['name'] = i.name
          image_data['state'] = i.state
          image_data['architecture'] = i.architecture
          image_data['root_device_type'] = i.root_device_type
          if ami is None or ami == i.id:
            image_list[i.id] = image_data
      except Exception, e:
        print "Exception %s" % e
        sys.exit(2)
      return image_list

    def deregisterAMI(self,ami):
      result_ids = []
      output = {}
      try:
        image = self.__conn.get_all_images(image_ids=strToList(ami))
        result = image[0].deregister()
        result_ids.append(ami)
        output[result] = result_ids
      except Exception, e:
        print e
      return output

    def createVM(self,ami,instance_type):
      i = {}
      output = []
      reservation = self.__conn.run_instances(ami, instance_type=instance_type)
      instance = reservation.instances[0]
      time.sleep(2)
      status = instance.update()
      while status == 'pending':
        time.sleep(10)
        status = instance.update()
      if status == 'running':
        i[instance.id] = {}
        i[instance.id]['public_dns'] = instance.public_dns_name
        i[instance.id]['private_dns'] = instance.private_dns_name
        i[instance.id]['status'] = status
        output.append(i)
        
      return output

    def changeVmState(self,state,instance_id):
      results = []
      result_ids = []
      output = {}
      instances = strToList(instance_id)
      if self.__debug == True: print instances
      if state == 'start':
        results = self.__conn.start_instances(instances)
      elif state == 'stop':
        results = self.__conn.stop_instances(instances)
      elif state == 'destroy' or state == 'terminate':
        state = 'terminate'
        results = self.__conn.terminate_instances(instances)
      for i in results:
        result_ids.append(i.id)
      output[state] = result_ids
      return output

    def _createVolume(self,size):
      output['id'] = self.__conn.create_volume(size,self._region)
      return json.dumps(output)

    def attachNewVolume(self,size,instance_id,dev):
      volume = json.loads(self_createVolume(size))
      output['status'] = self.__conn.attach_volume(volume['id'],instance_id, dev)
      return json.dumps(output)

    def deleteVolume(self,vol_id):
      output = {}
      results = self.__conn.delete_volume(vol_id)
      if results is True:
        status = 'deleted'
      else:
        status = 'failed'
      output[status] = vol_id
      return json.dumps(output)

    def attachEIP(self,ip=None):
      print "asdfasdf"

    def createImage(self,instance_id):
      print "Not implemented yet"

def strToList(data):
  new_list = []
  if not isinstance(data, list):
    new_list.append(data)
  else:
    new_list = data
  return new_list
