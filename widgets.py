#!/usr/bin/env python

import yaml
import json


class ethports():

  def __init__(self):
    
    globals().update(yaml.load(open('/home/cisco/apps/nxapi/library/tv-test/ethport.yml').read()))

  def ethport(self,each,intf_name):

    temp = {}
  
    if intf_name.startswith('V'):
      temp['admin_state'] = each['svi_admin_state'] # need to finish this for SVIs at a later date
    else:
      if not intf_name.startswith('m'):
        if not intf_name.startswith('l'):# mgmt interface doesn't show underruns, giants, etc. Focus is on core eth ports now
          print each['interface']
          for k,v in EthPortView.iteritems():
            temp[k] = each[v]

    return temp

  def interface_table(self,subdata):

    interfaces = {}
  
    try:
      for each in subdata:
        intf_name = each['interface']
        interfaces[intf_name] = self.ethport(each,intf_name)
    except TypeError:
      each = subdata
      intf_name = each['interface']
      interfaces[intf_name] = self.ethport(each,intf_name)
  
    return interfaces

################################################################


################################################################

class nxfeatures():

  def __init__(self):
    
    globals().update(yaml.load(open('tv-test/features.yml').read()))
  
  def feat(self,each,feature):

    temp = {}

    for k,v in FeaturesView.iteritems():
      temp[k] = each[v]

    return temp
  
  def feature_table(self,subdata):

    features = {}
  
    try:
      for each in subdata:
        feature = each[FeaturesView['name']]
        if feature in features.keys():
          feature = feature + '_' + each['cfcFeatureCtrlInstanceNum2']
        features[feature] = self.feat(each,feature)
    except TypeError:
      each = subdata
      feature = each[FeaturesView['name']]
      features[feature] = self.feat(each,feature)
  
    return features

################################################################


################################################################
class intf_configs():

  def __init__(self):
    
    globals().update(yaml.load(open('tv-test/intfconfig.yml').read()))

  def ethport(self,each,intf_name):

    temp = {}
    for k,v in IntfConfigView.iteritems():
      if k == 'name':
        temp[k] = each['__XML__PARAM__interface'][v]
      elif k == 'ip_addr':
        try:
          temp[k] = each['__XML__PARAM__interface']['ip']['address']['__XML__PARAM__ip-prefix']['__XML__value']
        except KeyError:
          temp[k] = 'n/a'
    return temp
  
  def interface_table(self,subdata):

    interfaces = {}
  
    try:
      for each in subdata:
        intf_name = each['__XML__PARAM__interface']['__XML__value']
        interfaces[intf_name] = self.ethport(each,intf_name)
    except TypeError:
      each = subdata
      #print json.dumps(each,indent=5)
      intf_name = each['__XML__PARAM__interface']['__XML__value']
      interfaces[intf_name] = self.ethport(each,intf_name)
  
    return interfaces
