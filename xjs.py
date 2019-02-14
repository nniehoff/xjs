#!/usr/bin/python3

import sys
import getopt
import yaml
import re
from datetime import datetime
from datetime import timedelta
from prettytable import PrettyTable


COLOR_GREEN = '\033[32m'
COLOR_ORANGE = '\u001b[31;1m'
COLOR_RED = '\033[31m'
COLOR_RESET = '\u001b[0m'
COLOR_YELLOW = '\033[33m'
UPDATE_THRESHOLD = 300

juju_status = {}
juju_date = datetime.now()


def load_yaml(inputfile):
    global juju_status

    filecontents = open(inputfile, 'r')
    juju_status = yaml.load(filecontents)


def find_dates(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():
        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = find_dates(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = find_dates(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


def get_max_date(date_list):
    max_date = datetime.now() - timedelta(days=36500)

    for date in date_list:
        testdate = datetime.strptime(date, '%d %b %Y %H:%M:%SZ')
        if testdate > max_date:
            max_date = testdate

    return max_date


def process_status():
    global juju_date
    all_dates = []

    all_dates = find_dates(juju_status, 'since')
    max_date = get_max_date(all_dates)

    print(COLOR_YELLOW + 'WARNING: Guessing time of run to be ' +
          str(max_date) + COLOR_RESET)
    if ('controller' in juju_status and
            'timestamp' in juju_status['controller']):
        juju_date = datetime.strptime(max_date.strftime('%d %b %Y') + ' ' +
                                      juju_status['controller']['timestamp'],
                                      '%d %b %Y %H:%M:%SZ')
    else:
        juju_date = max_date


def color_model_info():
    global juju_status

    # Juju Version
    if re.match('^2', juju_status['model']['version']):
        color = COLOR_GREEN
    elif re.match('^1', juju_status['model']['version']):
        color = COLOR_YELLOW
    else:
        color = COLOR_RED
    juju_status['model']['version_color'] = color

    # Model Status
    if juju_status['model']['model-status']['current'] == 'available':
        color = COLOR_GREEN
    else:
        color = COLOR_RED
    juju_status['model']['model-status']['current_color'] = color

    # Model Color
    if 'meter-status' in juju_status['model']:
        if juju_status['model']['meter-status']['color'] == 'green':
            color = COLOR_GREEN
        elif juju_status['model']['meter-status']['color'] == 'red':
            color = COLOR_RED
        elif juju_status['model']['meter-status']['color'] == 'amber':
            color = COLOR_ORANGE
        juju_status['model']['meter-status']['color_color'] = color


def color_application_info():
    global juju_status

    for appname, appinfo in juju_status['applications'].items():
        # last_update = datetime.strptime(
        #     appinfo['application-status']['since'], '%d %b %Y %H:%M:%SZ')
        # timediff = juju_date - last_update
        # if timediff.seconds > UPDATE_THRESHOLD:
        #     appinfo['row_color'] = COLOR_ORANGE
        #     appinfo['notes'].append('Last status update ' +
        #                             str(timediff.seconds) + ' ago')

        # Application Status
        if appinfo['application-status']['current'] == 'active':
            color = COLOR_GREEN
        elif appinfo['application-status']['current'] in ('error', 'blocked'):
            color = COLOR_RED
        elif appinfo['application-status']['current'] == 'waiting':
            color = COLOR_RESET
        elif appinfo['application-status']['current'] == 'maintenance':
            color = COLOR_ORANGE
        else:
            color = COLOR_YELLOW
        appinfo['application-status']['current_color'] = color

        # Scale
        if appinfo['scale'] == 0:
            appinfo['scale_color'] = COLOR_RED

        # Charm Revision
        if 'can-upgrade-to' in appinfo:
            match = re.match('\D+(\d+)$', appinfo['can-upgrade-to'])
            currentversion = match.group(1)
            if match:
                if currentversion == appinfo['version']:
                    color = COLOR_GREEN
                elif currentversion < appinfo['version']:
                    color = COLOR_YELLOW
                    appinfo['notes'].append('Charm Revision ' +
                                            currentversion +
                                            ' is available')
                appinfo['charm-rev_color'] = color

        # Juju Store
        if appinfo['charm-origin'] != 'jujucharms':
            appinfo['charm-origin_color'] = COLOR_YELLOW


def process_application_info():
    global juju_status
    for appname in juju_status['applications']:
        notes = []
        scale = 0
        version = ""

        if juju_status['applications'][appname]['exposed']:
            notes.append('exposed')
        if 'units' in juju_status['applications'][appname]:
            scale = len(juju_status['applications'][appname]['units'].keys())
        if 'version' in juju_status['applications'][appname]:
            version = juju_status['applications'][appname]['version']

        juju_status['applications'][appname]['notes'] = notes
        juju_status['applications'][appname]['scale'] = scale
        juju_status['applications'][appname]['version'] = version


def print_model_info():
    row = []
    table = PrettyTable()
    table.set_style(12)
    table.field_names = ["Model", "Controller", "Cloud/Region", "Version",
                         "SLA", "Timestamp", "Model-Status", "Meter-Status",
                         "Message"]
    for column in ['name', 'controller', 'cloud', 'version', 'sla']:
        if column + '_color' in juju_status['model']:
            row.append(juju_status['model'][column + '_color'] +
                       juju_status['model'][column] + COLOR_RESET)
        else:
            row.append(juju_status['model'][column])
    if ('controller' in juju_status and
            'timestamp' in juju_status['controller']):
        row.append(juju_status['controller']['timestamp'])
    else:
        print(COLOR_YELLOW + 'WARNING: Guessing at the controller timestamp' +
              COLOR_RESET)
        row.append(juju_status['model']['model-status']['since'])
    if 'current_color' in juju_status['model']['model-status']:
        row.append(juju_status['model']['model-status']['current_color'] +
                   juju_status['model']['model-status']['current'] +
                   COLOR_RESET)
    else:
        row.append(juju_status['model']['model-status']['current'])
    if 'meter-status' in juju_status['model']:
        if 'color_color' in juju_status['model']['meter-status']:
            row.append(juju_status['model']['meter-status']['color_color'] +
                       juju_status['model']['meter-status']['color'] +
                       COLOR_RESET)
        else:
            row.append(juju_status['model']['meter-status']['color'])
        row.append(juju_status['model']['meter-status']['message'])
    else:
        row.append("")
        row.append("")
    table.add_row(row)
    table.align = "l"
    print(table)


def process_unit_info():
    global juju_status

    for appname, appinfo in juju_status['applications'].items():
        if 'units' in appinfo:
            for unitname, unitinfo in appinfo['units'].items():
                unitinfo['notes'] = []
                if 'subordinates' in unitinfo:
                    subordinates = unitinfo['subordinates']
                    for subunitname, subunitinfo in subordinates.items():
                        subunitinfo['notes'] = []


def color_unit_info():
    global juju_status

    for appname, appinfo in juju_status['applications'].items():
        if 'units' in appinfo:
            for unitname, unitinfo in appinfo['units'].items():
                workload_status = unitinfo['workload-status']
                unitjuju_status = unitinfo['juju-status']
                # last_update = get_max_date([workload_status['since'],
                #                             unitjuju_status['since']])
                # timediff = juju_date - last_update
                # if timediff.seconds > UPDATE_THRESHOLD:
                #     unitinfo['row_color'] = COLOR_ORANGE
                #     unitinfo['notes'].append('Last status update ' +
                #                              str(timediff.seconds) + ' ago')

                # Workload Status
                if workload_status['current'] == 'active':
                    workload_status['current_color'] = COLOR_GREEN
                elif workload_status['current'] in ('error', 'blocked'):
                    workload_status['current_color'] = COLOR_RED
                elif workload_status['current'] == 'waiting':
                    workload_status['current_color'] = COLOR_RESET
                elif workload_status['current'] == 'maintenance':
                    workload_status['current_color'] = COLOR_ORANGE
                else:
                    workload_status['current_color'] = COLOR_YELLOW

                # Juju Status
                if unitjuju_status['current'] in ('idle', 'executing'):
                    unitjuju_status['current_color'] = COLOR_GREEN
                elif unitjuju_status['current'] == 'error':
                    unitjuju_status['current_color'] = COLOR_RED
                else:
                    unitjuju_status['current_color'] = COLOR_YELLOW

                # Subordinates
                if 'subordinates' in unitinfo:
                    subordinates = unitinfo['subordinates']
                    for subunitname, subunitinfo in subordinates.items():
                        workload_status = subunitinfo['workload-status']
                        subjuju_status = subunitinfo['juju-status']
                        # last_update = get_max_date([workload_status['since'],
                        #                             subjuju_status['since']])
                        # timediff = juju_date - last_update
                        # if timediff.seconds > UPDATE_THRESHOLD:
                        #     subunitinfo['row_color'] = COLOR_ORANGE
                        #     subunitinfo['notes'].append('Last status update ' +
                        #                                 str(timediff.seconds) +
                        #                                 ' ago')

                        # Workload Status
                        if workload_status['current'] == 'active':
                            workload_status['current_color'] = COLOR_GREEN
                        elif (workload_status['current'] in
                              ('error', 'blocked')):
                            workload_status['current_color'] = COLOR_RED
                        elif workload_status['current'] == 'waiting':
                            workload_status['current_color'] = COLOR_RESET
                        elif workload_status['current'] == 'maintenance':
                            workload_status['current_color'] = COLOR_ORANGE
                        else:
                            workload_status['current_color'] = COLOR_YELLOW

                        # Juju Status
                        if subjuju_status['current'] in ('idle', 'executing'):
                            subjuju_status['current_color'] = COLOR_GREEN
                        elif subjuju_status['current'] == 'error':
                            subjuju_status['current_color'] = COLOR_RED
                        else:
                            subjuju_status['current_color'] = COLOR_YELLOW


def print_unit_info(hide_subondinate_units=False):
    table = PrettyTable()
    table.set_style(12)
    table.field_names = ["Unit", "Workload", "Agent", "Machine",
                         "Public address", "Ports", "Message", "Notes"]
    for appname, appinfo in juju_status['applications'].items():
        if 'units' in appinfo:
            for unitname, unitinfo in appinfo['units'].items():
                row = []
                default_color = COLOR_RESET
                if 'row_color' in unitinfo:
                    default_color = unitinfo['row_color']
                if 'leader' in unitinfo and unitinfo['leader']:
                    row.append(default_color + unitname + '*')
                else:
                    row.append(default_color + unitname)
                row.append(unitinfo['workload-status']['current_color'] +
                           unitinfo['workload-status']['current'] +
                           default_color)
                row.append(unitinfo['juju-status']['current_color'] +
                           unitinfo['juju-status']['current'] +
                           default_color)
                row.append(unitinfo['machine'])
                row.append(unitinfo['public-address'])
                if 'open-ports' in unitinfo:
                    row.append(','.join(unitinfo['open-ports']))
                else:
                    row.append('')
                if 'message' in unitinfo['workload-status']:
                    row.append(unitinfo['workload-status']['message'])
                else:
                    row.append('')
                if 'row_color' in unitinfo:
                    row.append(', '.join(unitinfo['notes']) + COLOR_RESET)
                else:
                    row.append(', '.join(unitinfo['notes']))
                table.add_row(row)
                if 'subordinates' in unitinfo and not hide_subondinate_units:
                    subordinates = unitinfo['subordinates']
                    for subunitname, subunitinfo in subordinates.items():
                        row = []
                        default_color = COLOR_RESET
                        if 'row_color' in subunitinfo:
                            default_color = subunitinfo['row_color']
                        workload_status = subunitinfo['workload-status']
                        subjuju_status = subunitinfo['juju-status']
                        if 'leader' in subunitinfo and subunitinfo['leader']:
                            row.append('  ' + default_color + subunitname +
                                       '*')
                        else:
                            row.append('  ' + default_color + subunitname)
                        row.append(workload_status['current_color'] +
                                   workload_status['current'] +
                                   default_color)
                        row.append(subjuju_status['current_color'] +
                                   subjuju_status['current'] +
                                   default_color)
                        row.append('')
                        row.append(unitinfo['public-address'])
                        row.append('')
                        row.append(workload_status['message'])
                        if 'row_color' in subunitinfo:
                            row.append(', '.join(subunitinfo['notes']) +
                                       COLOR_RESET)
                        else:
                            row.append(', '.join(subunitinfo['notes']))
                        table.add_row(row)
    table.align = "l"
    print(table)


def print_application_info(hide_scale_zero=False):
    table = PrettyTable()
    table.set_style(12)
    table.field_names = ["App", "Version", "Status", "Scale", "Charm", "Store",
                         "Rev", "OS", "Series", "Notes"]
    for appname, appinfo in juju_status['applications'].items():
        if not (hide_scale_zero and int(appinfo['scale']) == 0):
            row = []
            default_color = COLOR_RESET
            if 'row_color' in appinfo:
                default_color = appinfo['row_color']
                row.append(default_color + appname)
            else:
                row.append(appname)
            row.append(appinfo['version'])
            if 'current_color' in appinfo['application-status']:
                row.append(appinfo['application-status']['current_color'] +
                           appinfo['application-status']['current'] +
                           default_color)
            else:
                row.append(appinfo['application-status']['current'])
            for column in ['scale', 'charm', 'charm-origin', 'charm-rev',
                           'os', 'series']:
                if column + '_color' in appinfo:
                    row.append(appinfo[column + '_color'] +
                               str(appinfo[column]) + default_color)
                else:
                    row.append(appinfo[column])
            if 'row_color' in appinfo:
                row.append(', '.join(appinfo['notes']) + COLOR_RESET)
            else:
                row.append(', '.join(appinfo['notes']))
            table.add_row(row)
    table.align = "l"
    print(table)


def process_machine_info():
    global juju_status

    for machname, machinfo in juju_status['machines'].items():
        for hardwarepair in machinfo['hardware'].split(' '):
            key, value = hardwarepair.split('=')
            machinfo[key] = value


def color_machine_info():
    global juju_status

    for machname, machinfo in juju_status['machines'].items():
        if machinfo['juju-status']['current'] == 'started':
            machinfo['juju-status']['current_color'] = COLOR_GREEN
        elif (machinfo['juju-status']['current'] in
              ('error', down)):
            machinfo['juju-status']['current_color'] = COLOR_RED
        elif machinfo['juju-status']['current'] == 'pending':
            machinfo['juju-status']['current_color'] = COLOR_ORANGE
        else:
            machinfo['juju-status']['current_color'] = COLOR_YELLOW


def print_machine_info():
    table = PrettyTable()
    table.set_style(12)
    table.field_names = ["Machine", "State", "DNS", "Inst id", "Series", "AZ",
                         "Arch", "Cores", "Memory", "Message"]
    for machname, machinfo in juju_status['machines'].items():
        row = []
        row.append(machname)
        row.append(machinfo['juju-status']['current_color'] +
                   machinfo['juju-status']['current'] + COLOR_RESET)
        row.append(machinfo['dns-name'])
        row.append(machinfo['instance-id'])
        row.append(machinfo['series'])
        if 'availability-zone' in machinfo:
            row.append(machinfo['availability-zone'])
        else:
            row.append("")
        if 'arch' in machinfo:
            row.append(machinfo['arch'])
        else:
            row.append("")
        if 'cores' in machinfo:
            row.append(machinfo['cores'])
        else:
            row.append("")
        if 'mem' in machinfo:
            row.append(machinfo['mem'])
        else:
            row.append("")
        row.append(machinfo['machine-status']['message'])
        table.add_row(row)
    table.align = "l"
    print(table)


def process_network_info():
    global juju_status


def color_network_info():
    global juju_status


def print_network_info():
    table = PrettyTable()
    table.set_style(12)
    table.field_names = ["Machine", "State", "DNS", "Inst id", "Series", "AZ",
                         "Arch", "Cores", "Memory", "Message"]
    table.align = "l"
    print(table)


def main(argv):
    inputfile = ''
    hide_scale_zero = False
    hide_subondinate_units = False
    show_model_info = True
    show_app_info = True
    show_unit_info = True
    show_machine_info = True
    show_network_info = True
    try:
        opts, args = getopt.getopt(argv, "namuszhi:", ["ifile=", "model"])
    except getopt.GetoptError:
        print('xjs.py [-z] [-s] -i <inputfile.yaml>')
        print('')
        print('-z Hide Applications with 0 units')
        print('-s Hide Subordinate Units')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('xjs.py -i <inputfile.yaml>')
            sys.exit()
        elif opt == '-z':
            hide_scale_zero = True
        elif opt == '-s':
            hide_subondinate_units = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-a", "-m", "-u", "--model", "-n"):
            if (show_app_info and
                    show_machine_info and
                    show_model_info and
                    show_unit_info and
                    show_network_info):
                show_model_info = False
                show_app_info = False
                show_unit_info = False
                show_machine_info = False
                show_network_info = False
            if opt == '-a':
                show_app_info = True
            elif opt == '-m':
                show_machine_info = True
            elif opt == '-u':
                show_unit_info = True
            elif opt == '--model':
                show_model_info = True
            elif opt == '-n':
                show_network_info = True
    load_yaml(inputfile)
    process_status()
    if show_model_info:
        color_model_info()
        print_model_info()
        print("")
    if show_app_info:
        process_application_info()
        color_application_info()
        print_application_info(hide_scale_zero)
        print("")
    if show_unit_info:
        process_unit_info()
        color_unit_info()
        print_unit_info(hide_subondinate_units)
        print("")
    if show_machine_info:
        process_machine_info()
        color_machine_info()
        print_machine_info()
        print("")
    if show_network_info:
        process_network_info()
        color_network_info()
        print_network_info()
        print("")


if __name__ == "__main__":
    main(sys.argv[1:])
