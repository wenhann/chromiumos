#!/usr/bin/python

# Copyright (c) 2009 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Some wrapper code for interacting with the wireless interface

This code should only be used for a quick and dirty control 
panel implementation for Memento.
"""

import os

def GeneratePsk(ssid, passphrase):
  """Generates a WPA key.
  
  Args:
    ssid: The name of the access point.
    passphrase: The user's WPA password.
  
  Returns:
    The encrypted WPA password or None if there was an error.
  """
  binary = "/usr/bin/wpa_passphrase %s %s" % (ssid, passphrase)
  cli_results = os.popen(binary);
  while 1:
    line = cli_results.readline();
    if not line: 
      break;
    if line.strip().find("psk") == 0:
      return line.strip().split('=')[1];
  return None;

def AddNetwork(ssid, passphrase):
  """Uses wpa_cli to configure a new network.

  Adds a new network, connects to it, and runs dhclient to get an IP.
  TODO(rtc): Right now all previously existing networks are disabled, 
  we need a better mechanism for dealing with this.
  """
  existing_networks = GetConfiguredNetworks();
  cli_results = os.popen("/sbin/wpa_cli add_network");
  cli_results.readline();
  network_id = cli_results.readline().split()[0];

  enable_command = "/sbin/wpa_cli enable_network %s" % network_id;
  cli_results = os.popen(enable_command);

  configure_ssid_command = \
      "/sbin/wpa_cli set_network %s ssid \\\"%s\\\"" % (network_id, ssid);
  cli_results = os.popen(configure_ssid_command);
  cli_results.readline();

  if passphrase == "":
    print "Connecting to an open network"
    configure_key_mgmt_command = \
        "/sbin/wpa_cli set_network %s key_mgmt NONE" % network_id;
    cli_results = os.popen(configure_key_mgmt_command);
    cli_results.readline();
  else:
    print "Configuring a WPA network"
    psk = GeneratePsk(ssid, passphrase)
    psk_command = \
        "/sbin/wpa_cli set_network %s psk %s" % (network_id, psk)
    cli_results = os.popen(psk_command);
    print cli_results.readline();

  for key, value in existing_networks.iteritems():
    disable_command = "/sbin/wpa_cli disable_network %s" % value["id"];
    cli_results = os.popen(disable_command);

  cli_results = os.popen("dhclient");

def GetConfiguredNetworks():
  """Gets a list of the currently configured networks.

  Returns:
    A dictionary mapping an ssid to its properties. See the comment 
    for ParseNetworkLine() for more details on the value.
  """
  cli_results = os.popen("/sbin/wpa_cli list_n");
  cli_results.readline();
  cli_results.readline();
  networks = {}
  while 1:
    line = cli_results.readline();
    if not line: 
      break;
    tokens = line.split('\t');
    network = ParseNetworkLine(tokens);
    networks[network["ssid"]] = network;
  return networks;
  
def ParseNetworkLine(tokens):
  """Parses a line of output generated by running 'wpa_cli list_networks'

  Returns:
    A dictionary containing the following keys
      * id - the wpa_supplicant id.
      * ssid - the ssid of the AP.
      * bssid - (the mac address of the AP).
      * flags - additional info, not currently used.
  """
  keys = { 0 : "id",
           1 : "ssid",
           2 : "bssid",
           3 : "flags", 
  };
  network_line_map = {};
  for index, token in enumerate(tokens):
    network_line_map[keys[index]] = token;
  return network_line_map;

def ParseWifiProperties(tokens):
  """Parses a line of output generated by running 'wpa_cli scan_results'

  Returns:
    A dictionary containing the following keys
      * mac - The MAC address of the AP.
      * frequencey - the frequencey of the AP (2.4Ghz for example).
      * signal - The signal strength of the AP.
      * encyrption - The encryption method of the AP.
  """
  ssid_index = len(tokens) - 1;
  keys = { 0 : "mac",
           1 : "frequency",
           2 : "signal",
           3 : "encryption",
           4 : "undocumented-data",
  };
  property_map = {}
  for index, token in enumerate(tokens):
    if index == ssid_index:
      property_map["ssid"] = token.rstrip("\n");
      continue;  
    property_map[keys[index]] = token 
  return property_map;

def Scan():
  """Scans for all nearby APs.
  
  Returns:
    A dictionary that maps an ssid to its properties. 
    See ParseWifiProperties for more details about the values.
  """
  cli_results = os.popen("/sbin/wpa_cli scan_results");
  found_ssid_line = False;
  networks = {}
  while 1:
    line = cli_results.readline();
    if not line: break;
    if not found_ssid_line and line.find("bssid") == 0:
      found_ssid_line = True;
      continue
    if not found_ssid_line: continue;

    tokens = line.split('\t');
    props = ParseWifiProperties(tokens);
    network = props["ssid"]
    if network not in networks:
      networks[network] = props;
    else:
      existing_network_signal = networks[network]["signal"];
      if props["signal"] > existing_network_signal:
        networks[network] = props;
  return networks;

def CurrentNetwork():
  """Returns the name of the network that the wifi interface is connected to.

  Returns:
    The AP name or None if the wifi card isn't connected to anything.
  """
  networks = GetConfiguredNetworks()
  for ssid, props in networks.iteritems():
    if props.has_key('flags') and props['flags'].find("CURRENT") >= 0:
      return ssid
  return None

if __name__ == "__main__":
  print CurrentNetwork()