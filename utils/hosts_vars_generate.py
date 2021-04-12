import pandas as pd
import re
from utils.Loopback_NETID import generate_net_id_from_loopback0

intfs_list_start_space = '\n' + ' ' * 12 + '- '
intfs_list_cont_space = '\n' + ' ' * 12 + '  '

four_spaces = '\n' + ' ' * 4
eigth_spaces = '\n' + ' ' * 8

def seperate_interface_type_and_port(interface_name_str):
    egec = re.compile('(^.*?(?=[0-9]))([0-9].*)')
    reply = egec.search(interface_name_str)
    type = reply.group(1)
    port = reply.group(2)
    if type.upper().startswith('TE'):
        type = 'TenGigabitEthernet'
    elif type.upper().startswith('GI'):
        type = 'GigabitEthernet'
    elif type.upper().startswith('R'):
        type = 'R'
    else:
        print('Invalid port type, exiting the program')
        exit(-1)
    return type, port

def host_file_generate(df):
    records = df.shape[0]
    host_file = "[all:vars]\n" \
                "ansible_connection=network_cli\n" \
                "ansible_network_os=ios\n\n" \
                "[ncs4200]"

    for i in range(records):
        host_file += '\n' + df['hostname'][i] + ' ansible_ssh_host={}'.format(df['mgmt_ip'][i])

    #print(host_file)

    with open("inventory/hosts", 'w') as f:
        f.write(host_file)
        
    return 'inventory/hosts'
        
def var_interface_generate(df):
    records = df.shape[0]
    interfaces_file = 'nodes:'
    for i in range(records):
        interfaces_file += '\n' + ' ' * 4 + df['hostname'][i] + ':' + '\n' + ' ' * 8 + 'interfaces:'

        ints_list = df['interfaces'][i].split(',')
        intf_ips_list = df['interface_ips'][i].split(',')

        len_int = len(ints_list)
        len_int_ip = len(intf_ips_list)

        if len_int != len_int_ip:
            assert ('Interface/IP information missing')
        else:
            for j in range(len_int):
                name, port = seperate_interface_type_and_port(ints_list[j].strip())
                interfaces_file += intfs_list_start_space + 'interface_name: ' + name
                interfaces_file += intfs_list_cont_space + 'interface_port: ' + port
                interfaces_file += intfs_list_cont_space + 'interface_type: ethernetCsmacd'
                interfaces_file += intfs_list_cont_space + 'ip_address: ' + intf_ips_list[j].strip()
                interfaces_file += intfs_list_cont_space + 'mask: ' + df['interface_subnet'][i]
                if name.upper().startswith('TE') or name.upper().startswith('GI'):
                    interfaces_file += intfs_list_cont_space + 'rsvp_bandwidth_percent: {}'.format(df['rsvp_bw_percentage'][i])

        interfaces_file += intfs_list_start_space + 'interface_name: ' + 'Loopback'
        interfaces_file += intfs_list_cont_space + 'interface_port: ' + '0'
        interfaces_file += intfs_list_cont_space + 'interface_type: softwareLoopback'
        interfaces_file += intfs_list_cont_space + 'ip_address: ' + df['loopback_ip'][i]
        interfaces_file += intfs_list_cont_space + 'mask: ' + '255.255.255.255'

    with open("host_vars/interfaces.yml", 'w') as f:
        f.write(interfaces_file)

    return 'host_vars/interfaces.yml'

def var_ospf_file_generate(df):
    records = df.shape[0]
    ospf_file = 'ospf:'
    for i in range(records):
        ospf_file += four_spaces + df['hostname'][i] + ':'
        ospf_file += eigth_spaces + 'ospf_id: {}'.format(df['ospf_process_id'][i])
        ospf_file += eigth_spaces + 'ospf_area: {}'.format(df['ospf_area'][i])
    
    with open("host_vars/ospf.yml", 'w') as f:
        f.write(ospf_file)

    return 'host_vars/ospf.yml'

def var_network_clock_intfs_generate_synce(df):
    records = df.shape[0]
    network_clock_synce_file = 'hold_off_time_msec: 50\n' \
                            'wait_to_restore_time_sec: 10\n' \
                            'input_sources:'


    for i in range(records):
        network_clock_synce_file += '\n' + ' ' * 4 + df['hostname'][i] + ':' + '\n' + ' ' * 8 + 'sources:'
        list_network_clock_synce_intfs = df['network_clock_synce_interfaces'][i].split(',')
        list_network_clock_synce_intfs_priorites = df['network_clock_synce_intfs_priorities'][i].split(',')

        len_network_clock_synce_intfs = len(list_network_clock_synce_intfs)
        len_network_clock_synce_intfs_priorites = len(list_network_clock_synce_intfs_priorites)

        if len_network_clock_synce_intfs != len_network_clock_synce_intfs_priorites:
            assert ('SyncE Interface/Priority information missing')
        else:
            for j in range(len_network_clock_synce_intfs):
                name, port = seperate_interface_type_and_port(list_network_clock_synce_intfs[j].strip())
                type = ''
                if name.upper().startswith('TE') or name.upper().startswith('GI'):
                    type = 'Interface'
                elif name.upper().startswith('R'):
                    type = 'External'
                else:
                    assert('Not implemented yet')

                network_clock_synce_file += intfs_list_start_space + 'source_type: ' + type
                if type == 'Interface':
                    network_clock_synce_file += intfs_list_cont_space + 'source_name: ' + name
                    network_clock_synce_file += intfs_list_cont_space + 'source_port: ' + port
                elif type == 'External':
                    network_clock_synce_file += intfs_list_cont_space + 'source_name: ' + name + port
                else:
                    assert('No inout given for this type since invalid or not implemented yet')

                network_clock_synce_file += intfs_list_cont_space + 'priority: ' + list_network_clock_synce_intfs_priorites[j].strip()

    with open("host_vars/network-clock-synce.yml", 'w') as f:
        f.write(network_clock_synce_file)

    return 'host_vars/network-clock-synce.yml'

def var_isis_generate(df):
    records = df.shape[0]

    isis_file = 'isis_auth_mode: md5\n' \
                'isis_key_name: ISIS_Auth_MD5\n' \
                'isis_key_id: 20\n' \
                'isis_key_encription_level: 7\n' \
                'isis_key_string: 1234abcd\n' \
                'isis_node_settings:'
    
    for i in range(records):
        #isis_file += '\n' + ' ' * 4 + df['hostname'][i] + ': 49.0001.{}.00'.format(generate_net_id_from_loopback0(df['loopback_ip'][i]))
        isis_file += four_spaces + df['hostname'][i] + ':'
        isis_file += eigth_spaces + 'isis_area_tag: ' + df['isis_area_tag'][i]
        isis_file += eigth_spaces + 'net_id: ' + df['isis_net_id'][i]
        isis_file += eigth_spaces + 'isis_level: ' + df['router_is_type'][i]
        isis_file += eigth_spaces + 'isis_level_mpls_te: ' + df['mpls_te_is_type'][i]

    with open("host_vars/isis.yml", 'w') as f:
        f.write(isis_file)

    return 'host_vars/isis.yml'

ptp_domain=10
def var_network_clock_ptp_source_generate(df):
    records = df.shape[0]
    network_clock_ptp_source_file = 'hold_off_time_msec: 50\n' \
                            'wait_to_restore_time_sec: 10\n' \
                            'input_sources:'


    for i in range(records):
        network_clock_ptp_source_file += '\n' + ' ' * 4 + df['hostname'][i] + ':' + '\n' + ' ' * 8 + 'sources:'
        list_network_clock_ptp_source = df['network_clock_souce_type'][i].split(',')
        list_network_clock_ptp_source_priorites = df['network_clock_souce_priority'][i].split(',')

        len_network_clock_ptp_source = len(list_network_clock_ptp_source)
        len_network_clock_ptp_source_priorites = len(list_network_clock_ptp_source_priorites)

        if len_network_clock_ptp_source != len_network_clock_ptp_source_priorites:
            assert ('PTP Source/Priority information missing')
        else:
            for j in range(len_network_clock_ptp_source):
                ptp_source = list_network_clock_ptp_source[j].strip()
                if ptp_source.upper() == 'PTP':
                    network_clock_ptp_source_file += intfs_list_start_space + 'source_type: ' + 'ptp'
                    network_clock_ptp_source_file += intfs_list_cont_space + 'priority: ' + list_network_clock_ptp_source_priorites[j].strip()
                    network_clock_ptp_source_file += intfs_list_cont_space + 'domain: {}'.format(ptp_domain)
                elif ptp_source.upper().startswith('R'):
                    network_clock_ptp_source_file += intfs_list_start_space + 'source_type: ' + 'External'
                    network_clock_ptp_source_file += intfs_list_cont_space + 'source_name: ' + list_network_clock_ptp_source[j].strip()
                    network_clock_ptp_source_file += intfs_list_cont_space + 'priority: ' + list_network_clock_ptp_source_priorites[j].strip()
                elif ptp_source.upper() == 'TOD':
                    network_clock_ptp_source_file += intfs_list_start_space + 'source_type: ' + 'TOD-CLOCK'
                    network_clock_ptp_source_file += intfs_list_cont_space + 'source_name: ' + 'internal'
                    network_clock_ptp_source_file += intfs_list_cont_space + 'priority: ' + list_network_clock_ptp_source_priorites[j].strip()
                else:
                    assert('No input given for this type since invalid or not implemented yet')

    with open("host_vars/network-clock-ptp-source.yml", 'w') as f:
        f.write(network_clock_ptp_source_file)

    return 'host_vars/network-clock-ptp-source.yml'


def var_network_clock_ptp_role(df):
    records = df.shape[0]
    network_clock_ptp_role = 'ptp_transport_interface:'
    network_clock_ptp_role += four_spaces + 'name: ' + 'Loopback'
    network_clock_ptp_role += four_spaces + 'port_number: {}'.format(0)
    network_clock_ptp_role += '\n' + 'ptp_domain_num: {}'.format(ptp_domain)
    network_clock_ptp_role += '\n' + 'ptp_profile: ' + 'g8265.1'
    network_clock_ptp_role += '\n' + 'ptp_role:'
    
    for i in range(records):
        network_clock_ptp_role += four_spaces + df['hostname'][i] + ':'
        role = df['network_clock_ptp_role'][i]
        if role.upper() == 'SLAVE':
            network_clock_ptp_role += eigth_spaces + 'role: ' + role.lower()
            network_clock_ptp_role += eigth_spaces + 'ptp_clock_port_name: ' + 'SLAVE'
            network_clock_ptp_role += eigth_spaces + 'priority1: {}'.format(200)
            network_clock_ptp_role += eigth_spaces + 'priority2: {}'.format(200)
            network_clock_ptp_role += eigth_spaces + 'ptp_source_clock_ip: ' + df['ptp_source_clock_ip'][i]
        elif role.upper() == "MASTER":
            network_clock_ptp_role += eigth_spaces + 'role: ' + role.lower()
            network_clock_ptp_role += eigth_spaces + 'ptp_clock_port_name: ' + 'MASTERCLOCK'
            network_clock_ptp_role += eigth_spaces + 'priority1: {}'.format(100)
            network_clock_ptp_role += eigth_spaces + 'priority2: {}'.format(100)
        else:
            assert('No input given for this type since invalid or not implemented yet')
            
    with open("host_vars/ptp-role.yml", 'w') as f:
        f.write(network_clock_ptp_role)

    return 'host_vars/ptp-role.yml'

