#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ncs4200_mpls_backbone_using_ansible_streamlit Console Script.

Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Tahsin Chowdhury"
__email__ = "tchowdhu@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


# Ready for your code.

from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep

from email import base64mime
import streamlit as st
import os, subprocess
from PIL import Image
import pandas as pd
import time
import zipfile
import base64

from utils.hosts_vars_generate import *


#index encoding of the list below
OSPF_AND_SYNCE = 0
ISIS_AND_SYNCE = 1
OSPF_AND_PTP = 2
ISIS_AND_PTP = 3
config_variation = ['MPLS BACKBONE CONFIGURATION WITH OSPF AND SYNCE',
                    'MPLS BACKBONE CONFIGURATION WITH ISIS AND SYNCE',
                    'MPLS BACKBONE CONFIGURATION WITH OSPF AND PTP',
                    'MPLS BACKBONE CONFIGURATION WITH ISIS AND PTP']

def fail_count_check(data):
    error = 0
    for lines in data.split('\n'):
        if 'failed=' in lines:
            line_list = lines.split()
            for stats in line_list:
                if 'failed=' in stats:
                    fail_count = int(stats.split('=')[1].strip())
                    if fail_count > 0:
                        error += 1
                    break
    return error

st.set_page_config(layout="wide")

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield

def export_file(file_name, type, hyperlink_tag):
    with open(file_name, "rb") as f:
                bytes_read = f.read()
                b64 = base64.b64encode(bytes_read).decode()
                href = f'<a href="data:file/{type};base64,{b64}" download=\'{file_name}\'>\
                        {hyperlink_tag}\
                    </a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

def CDP():
    st.info('Running Config: CDP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_1_cdp.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        

def LLDP():
    st.info('Running Config: LLDP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_1_lldp.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
    #print(subprocess.run(['./start.sh', 'mpls_back_bone_creation_with_ospf_synce_lldp.yml'], capture_output=True, text=True))

def INTF_IP():
    st.info('Running Config: INTERFACE IP ADDRESS...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_2_ip_address.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
 
def OSPF():       
    st.info('Running Config: OSPF...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_3_ospf.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        
def ISIS():       
    st.info('Running Config: ISIS...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_3_isis.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)

def MPLS_TE_OSPF():
    st.info('Running Config: MPLS TE...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_4_mpls_te_ospf.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        
def MPLS_TE_ISIS():
    st.info('Running Config: MPLS TE...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_4_mpls_te_isis.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)

def MPLS_LDP_OSPF():       
    st.info('Running Config: MPLS LDP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_5_mpls_ldp_ospf.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        
def MPLS_LDP_ISIS():       
    st.info('Running Config: MPLS LDP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_5_mpls_ldp_isis.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)

def RSVP():
    st.info('Running Config: RSVP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_6_rsvp.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)

def NETWORK_CLOCK_SYNCE():      
    st.info('Running Config: NETWORK CLOCK SYNCE...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_7_network_clock_synce.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        
def NETWORK_CLOCK_PTP():      
    st.info('Running Config: NETWORK CLOCK PTP...')
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_7_network_clock_ptp.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)

def SAVE():
    st.info('Running: SAVE Config...')   
    output = st.empty()
    config_output_ansible = ''
    with st_capture(output.code):
        config_output_ansible = os.popen('./start.sh config_8_save.yml').read()
        print(config_output_ansible)
    return fail_count_check(config_output_ansible)
        
def APPLY_CONFIGS(config_item, config_precent, config_var_select):
    
    if config_item == 'CDP':
        fail_count = CDP()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'LLDP':
        fail_count = LLDP()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'INTF_IP':
        fail_count = INTF_IP()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'OSPF':
        fail_count = OSPF()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'ISIS':
        fail_count = ISIS()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'MPLS_TE':
        fail_count = 0
        if (config_var_select == config_variation[OSPF_AND_SYNCE]) or (config_var_select == config_variation[OSPF_AND_PTP]):
            fail_count = MPLS_TE_OSPF()
        elif (config_var_select == config_variation[ISIS_AND_SYNCE]) or (config_var_select == config_variation[ISIS_AND_PTP]):
            fail_count = MPLS_TE_ISIS()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'MPLS_LDP':
        fail_count = 0
        if (config_var_select == config_variation[OSPF_AND_SYNCE]) or (config_var_select == config_variation[OSPF_AND_PTP]):
            fail_count = MPLS_LDP_OSPF()
        elif (config_var_select == config_variation[ISIS_AND_SYNCE]) or (config_var_select == config_variation[ISIS_AND_PTP]):
            fail_count = MPLS_LDP_ISIS()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'RSVP':
        fail_count = RSVP()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'NETWORK_CLOCK_SYNCE':
        fail_count = NETWORK_CLOCK_SYNCE()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'NETWORK_CLOCK_PTP':
        fail_count = NETWORK_CLOCK_PTP()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    elif config_item == 'SAVE':
        fail_count = SAVE()
        if fail_count > 0:
            st.error('Error Occured..')
            return 0
        else:
            return config_precent
    
    else:
        st.error(config_item+': Invalid Selection')
        return 0
    

img = Image.open('Cisco-Logo.png')
st.sidebar.image(img)

st.markdown('# NCS4200 MPLS BACKBONE CONFIGURATION')
st.markdown('source code avilable at: https://github.com/tchowdhu/ncs4200_mpls_backbone_using_ansible_streamlit.git')

config_variety_select = st.selectbox('Select Config Variation:', config_variation)

st.sidebar.info("Upload Data Excel File:")
if (config_variety_select == config_variation[OSPF_AND_SYNCE]):
    export_file('excel_data_template/ncs4200_init_conf_data_input_template_ospf_synce.xlsx', 'xlsx', '(Download data input template)')
elif (config_variety_select == config_variation[OSPF_AND_PTP]):
    export_file('excel_data_template/ncs4200_init_conf_data_input_template_ospf_ptp.xlsx', 'xlsx', '(Download data input template)')
elif (config_variety_select == config_variation[ISIS_AND_SYNCE]):
    export_file('excel_data_template/ncs4200_init_conf_data_input_template_isis_synce.xlsx', 'xlsx', '(Download data input template)')
elif (config_variety_select == config_variation[ISIS_AND_PTP]):
    export_file('excel_data_template/ncs4200_init_conf_data_input_template_isis_ptp.xlsx', 'xlsx', '(Download data input template)')

file = st.sidebar.file_uploader("Choose an excel file", type="xlsx")

#import time
#with st.spinner("Waiting .."):
#     time.sleep(5)
#     st.success("Finished!")

#my_bar = st.progress(0)
#for p in range(100):
#    sleep(0.1)
#    my_bar.progress(p + 1)

if file:
    df = pd.read_excel(file, engine='openpyxl')
    expected_columns = list()
    if (config_variety_select == config_variation[OSPF_AND_SYNCE]):
        expected_columns = ['hostname', 
                        'mgmt_ip', 
                        'loopback_ip', 
                        'interfaces', 
                        'interface_ips',
                        'interface_subnet',
                        'ospf_process_id',
                        'ospf_area',
                        'rsvp_bw_percentage', 
                        'network_clock_synce_interfaces',
                        'network_clock_synce_intfs_priorities']
    elif (config_variety_select == config_variation[OSPF_AND_PTP]):
        expected_columns = ['hostname', 
                        'mgmt_ip', 
                        'loopback_ip', 
                        'interfaces', 
                        'interface_ips',
                        'interface_subnet',
                        'ospf_process_id',
                        'ospf_area',
                        'rsvp_bw_percentage', 
                        'network_clock_ptp_role',
                        'ptp_source_clock_ip',
                        'network_clock_souce_type',
                        'network_clock_souce_priority']
    elif (config_variety_select == config_variation[ISIS_AND_SYNCE]):
        expected_columns = ['hostname', 
                        'mgmt_ip', 
                        'loopback_ip', 
                        'interfaces', 
                        'interface_ips',
                        'interface_subnet',
                        'isis_area_tag',
                        'isis_net_id',
                        'router_is_type',
                        'mpls_te_is_type',
                        'rsvp_bw_percentage', 
                        'network_clock_synce_interfaces',
                        'network_clock_synce_intfs_priorities']
    elif (config_variety_select == config_variation[ISIS_AND_PTP]):
        expected_columns = ['hostname', 
                        'mgmt_ip', 
                        'loopback_ip', 
                        'interfaces', 
                        'interface_ips',
                        'interface_subnet',
                        'isis_area_tag',
                        'isis_net_id',
                        'router_is_type',
                        'mpls_te_is_type',
                        'rsvp_bw_percentage', 
                        'network_clock_ptp_role',
                        'ptp_source_clock_ip',
                        'network_clock_souce_type',
                        'network_clock_souce_priority']
    
    uploaded_columns = df.columns
    
    expected = set(expected_columns)
    uploaded = set(uploaded_columns)
    if expected == uploaded:
        os.system('rm -rf ./inventory/*')
        os.system('rm -rf ./host_vars/*')
        st.dataframe(df)
        
        st.info('Generating inventory host file:')
        inventory_file=host_file_generate(df)
        with open(inventory_file, 'r') as filename:
            output = st.empty()
            with st_capture(output.code):
                print(filename.read())
        
        st.info('Generating interface variable file:')
        var_interface_file=var_interface_generate(df)
        with open(var_interface_file, 'r') as filename:
            output = st.empty()
            with st_capture(output.code):
                print(filename.read())
        
        if (config_variety_select == config_variation[OSPF_AND_SYNCE]) or (config_variety_select == config_variation[OSPF_AND_PTP]):
            st.info('Generating ospf variable file:')
            var_ospf_file = var_ospf_file_generate(df)
            with open(var_ospf_file, 'r') as filename:
                output = st.empty()
                with st_capture(output.code):
                    print(filename.read())
        
        if (config_variety_select == config_variation[OSPF_AND_SYNCE]) or (config_variety_select == config_variation[ISIS_AND_SYNCE]):
            st.info('Generating network-clock variable file:')
            var_network_clock_intfs_file=var_network_clock_intfs_generate_synce(df)
            with open(var_network_clock_intfs_file, 'r') as filename:
                output = st.empty()
                with st_capture(output.code):
                    print(filename.read())
        elif (config_variety_select == config_variation[OSPF_AND_PTP]) or (config_variety_select == config_variation[ISIS_AND_PTP]):
            st.info('Generating network-clock-ptp variable file:')
            var_network_clock_intfs_file=var_network_clock_ptp_source_generate(df)
            with open(var_network_clock_intfs_file, 'r') as filename:
                output = st.empty()
                with st_capture(output.code):
                    print(filename.read())
            st.info('Generating ptp-role variable file:')
            ptp_role_file=var_network_clock_ptp_role(df)
            with open(ptp_role_file, 'r') as filename:
                output = st.empty()
                with st_capture(output.code):
                    print(filename.read())
        
        if (config_variety_select == config_variation[ISIS_AND_SYNCE]) or (config_variety_select == config_variation[ISIS_AND_PTP]):
            var_isis_file = var_isis_generate(df)
            st.info('Generating isis variable file: {}'.format(var_isis_file))
            with open(var_isis_file, 'r') as filename:
                output = st.empty()
                with st_capture(output.code):
                    print(filename.read())
        
        select_config_items = ''
        if (config_variety_select == config_variation[OSPF_AND_SYNCE]) :
            select_config_items = st.multiselect("Select Config Items: ",("CDP",
                                                                    "LLDP",
                                                                    "INTF_IP",
                                                                    "OSPF",
                                                                    "MPLS_TE",
                                                                    "MPLS_LDP",
                                                                    "RSVP",
                                                                    "NETWORK_CLOCK_SYNCE",
                                                                    "SAVE"))

        elif (config_variety_select == config_variation[ISIS_AND_SYNCE]) :
            select_config_items = st.multiselect("Select Config Items: ",("CDP",
                                                                    "LLDP",
                                                                    "INTF_IP",
                                                                    "ISIS",
                                                                    "MPLS_TE",
                                                                    "MPLS_LDP",
                                                                    "RSVP",
                                                                    "NETWORK_CLOCK_SYNCE",
                                                                    "SAVE"))
        elif (config_variety_select == config_variation[OSPF_AND_PTP]) :
            select_config_items = st.multiselect("Select Config Items: ",("CDP",
                                                                    "LLDP",
                                                                    "INTF_IP",
                                                                    "OSPF",
                                                                    "MPLS_TE",
                                                                    "MPLS_LDP",
                                                                    "RSVP",
                                                                    "NETWORK_CLOCK_PTP",
                                                                    "SAVE"))

        elif (config_variety_select == config_variation[ISIS_AND_PTP]) :
            select_config_items = st.multiselect("Select Config Items: ",("CDP",
                                                                    "LLDP",
                                                                    "INTF_IP",
                                                                    "ISIS",
                                                                    "MPLS_TE",
                                                                    "MPLS_LDP",
                                                                    "RSVP",
                                                                    "NETWORK_CLOCK_PTP",
                                                                    "SAVE"))

        st.write("You selected",len(select_config_items),"config items:", select_config_items)

        action_applied = False
        if st.button('Apply Configs'):
            #print(os.system('source ./.env'))
            os.system('rm -rf ./config_generated_from_template/*')
            os.system('rm -rf ./*.zip')
            p = 0
            status_bar = st.sidebar.info('Config progress status: {}%'.format(p))
            my_bar = st.sidebar.progress(p)
            len_int = int(100/len(select_config_items))
            for item in select_config_items:
                p += APPLY_CONFIGS(item, len_int, config_variety_select)
                if p == int(len_int*len(select_config_items)):
                    p = 100
                #APPLY_CONFIGS(item)
                my_bar.progress(p)
                status_bar.info('Config progress status: {}%'.format(p))
            if p == 100:
                st.sidebar.success('Finished!')
                st.success('Completed!')
                action_applied = True
            elif p == 0:
                st.sidebar.error('Failed!')
                st.error('Failed!, Check environment and config data')
                action_applied = True
            else:
                st.sidebar.warning('Partially Failed!')
                st.warning('Partially Failed: See errors above')
                action_applied = False

        if action_applied:
            file_name = 'config_generated_and_applied_{}.zip'.format(time.strftime("%Y%m%d-%H%M%S"))
            file_name_zip = zipfile.ZipFile(file_name, 'w')
            
            for folder, subfolders, files in os.walk('config_generated_from_template'):
                for file in files:
                    file_name_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'config_generated_from_template'), compress_type = zipfile.ZIP_DEFLATED)
            file_name_zip.close()
            
            
            # send to webapp to make downloadable link
            export_file(file_name, 'zip', 'Export Applied Configs')
            

    else:
        st.error('Excel uploaded with invalid data columns')
        st.info('Expected Columns:')
        st.write(expected_columns)

