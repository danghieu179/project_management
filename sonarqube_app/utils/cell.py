from datetime import datetime
from django.utils import formats

import re
from urllib import parse

input_arr = [
    ('From Date', 'from_date'),
    ('To Date', 'to_date'),
    ('Coverage', 'unit_test'),
    ('Blocker', 'blocker'),
    ('Critical', 'critical'),
    ('Major', 'major'),
    ('Minor', 'minor')
]


class Cell(object):

    def __init__(self, projects=None, config=None):
        self.projects = projects
        self.config = config

    def check_header_cell(self, expect_header):
        mess = ''
        self.projects[0].sort()
        if self.projects[0] != expect_header:
            mess = 'No expected header columns'
        return mess

    def get_project_list(self):
        list_project = []
        mess = ''
        projects = self.projects
        for project in projects[1:len(projects)]:
            if len(project) == 5 and project[0].strip() and project[3].strip() and self.valid_url(project[4].strip()):
                list_project.append((project[0].lower(), project[0]))
        if not list_project:
            mess = 'Not found Project Name or Coverage Field or invalid Sonar URL in Google Sheets file'
        list_project.sort()
        return list_project, mess

    def get_config(self):
        config_dict = {}
        mess = ''
        for config in self.config:
            if len(config) == 2:
                if config[0].strip() == 'From Date':
                    try:
                        datetime.strptime(config[1], "%b %d, %Y").date()
                        config_dict['from_date'] = config[1]
                    except ValueError as e:
                        mess = "From Date %s does not match format 'MMM DD, YYYY'" % (
                            config[1])
                elif config[0].strip() == 'To Date':
                    try:
                        datetime.strptime(config[1], "%b %d, %Y").date()
                        config_dict['to_date'] = config[1]
                    except ValueError as e:
                        mess = "To Date %s does not match format 'MMM DD, YYYY'" % (
                            config[1])
                elif config[0].strip() == 'Coverage':
                    try:
                        config_dict['unit_test'] = int(config[1])
                    except ValueError as e:
                        mess = e
                elif config[0].strip() == 'Blocker':
                    try:
                        config_dict['blocker'] = int(config[1])
                    except ValueError as e:
                        mess = e
                elif config[0].strip() == 'Critical':
                    try:
                        config_dict['critical'] = int(config[1])
                    except ValueError as e:
                        mess = e
                elif config[0].strip() == 'Major':
                    try:
                        config_dict['major'] = int(config[1])
                    except ValueError as e:
                        mess = e
                elif config[0].strip() == 'Minor':
                    try:
                        config_dict['minor'] = int(config[1])
                    except ValueError as e:
                        mess = e
        if config_dict.get('from_date', False) and config_dict.get('to_date', False):
            from_date = datetime.strptime(config_dict.get(
                'from_date', False), "%b %d, %Y").date()
            to_date = datetime.strptime(config_dict.get(
                'to_date', False), "%b %d, %Y").date()
            if from_date > to_date:
                mess = 'From Date less than or equal to To Date'

        for input in input_arr:
            if input[1] not in config_dict.keys():
                mess = input[0] + \
                    ' not found in file or wrong value. Please align formart "Input Name (Col A): Value (Col B)"'
                break
        return config_dict, mess

    def valid_url(self, url):
        """This is function check URL's arguments matching with requirement
        Arguments:
            url {string} -- String URL
        Returns:
            [boolean] -- Return a variable for check
        """
        error = False
        arr_metrics_standard = ['blocker_violations',
                                'critical_violations', 'major_violations',
                                'minor_violations']
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, url) is not None:
            # url_parse = parse.urlparse(url)
            parse_url = parse.parse_qs(parse.urlparse(url).query)
            if parse_url.get('metrics', False) and parse_url.get('component', False):
                arr_metrics = parse_url['metrics'][0].split(',')
                arr_metrics.sort()
                if arr_metrics_standard == arr_metrics:
                    error = True
        return error
