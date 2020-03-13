from django.views.generic.base import TemplateView
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse


import json

from google_api.sheets_api import GoogleAPI

from .utils.cell import Cell
from .utils.const import URL_GOOGLE_DRIVE, EXPECT_HEADER, PROJECT_SHEET, CONFIG_SHEET, SONARQUBE_PAGE
from .forms import SonarForm, SonarFormInput


class SonarPageView(TemplateView):

    template_name = SONARQUBE_PAGE

    def __init__(self):
        self.context = {'title': 'Sonar', 'card_title': 'Sonar Report'}

    def post(self, request):
        """[Function will run when click button search in Sonar Report page]

        Arguments:
            request {[wsgi]}

        Returns:
            [route] -- [Authorize page if user not login or Input Sonar page]
        """
        drive_url = request.POST['url']
        inital_data = {'url': drive_url}

        # check url input
        if not drive_url.startswith('https://docs.google.com/spreadsheets/d/'):
            self.context.update({
                'status': 'Invalid Google Sheet URL.',
                'form': SonarForm(initial=inital_data)
            })
            return render(request, SONARQUBE_PAGE, self.context)

        # update parameters to session
        request.session.update({
            'from_post': True,
            'redirect_url': 'sonar',
            'drive_id': drive_url.split('/')[5],
            'initial': inital_data
        })
        if 'credentials' not in request.session:
            return redirect(reverse('authorize'))
        return redirect(reverse('sonar'))

    def get(self, request):
        """[Function will return filter page]

        Arguments:
            request {[wsgi]}

        Returns:
            [html] -- Sonarqube page
        """
        self.context['form'] = SonarForm()
        filter_sonar = 'False'
        if set(['from_post', 'credentials']).issubset(list(request.session.keys())):
            request.session['from_post'] = False
            if request.session.get('initial', False):
                setattr(self.context['form'], 'initial',
                        request.session['initial'])
            
            google_api = GoogleAPI(request.session['credentials'])
            sheet = google_api.call_the_sheets_api()
            
            # Load data from sheet
            status_code, values = google_api.get_data(
                sheetsrange=PROJECT_SHEET, sheet=sheet, spreadsheetId=request.session['drive_id'])
                
            # render data to input form
            if status_code == 200 and values.get('values', False):
                projects = values.get('values', False)
                cell = Cell(projects)
                # check value columns in google sheets
                mess = cell.check_header_cell(EXPECT_HEADER)
                self.context['status'] = mess
                list_project, mess = cell.get_project_list()
                self.context['status'] = mess
                if list_project:
                    input_form = SonarFormInput(list_project)
                    self.context['input_from'] = input_form
                    filter_sonar = 'True'
            else:
                if status_code != 200:
                    self.context['status'] = values
                    if status_code == 403:
                        self.context['status'] = values + \
                            '. Please click <a href="/authorize">here</a> to change account'
                else:
                    self.context['status'] = 'Not found data Projects in Google Sheets file'

            # get data config
            status_code, values = google_api.get_data(
                sheetsrange=CONFIG_SHEET, sheet=sheet, spreadsheetId=request.session['drive_id'])

            if status_code == 200 and values.get('values', False):
                configs = values.get('values', False)
                cell = Cell(config=configs)
                dict_config, mess_config = cell.get_config()
                if len(mess_config):
                    self.context['status'] = mess_config
                if dict_config and self.context.get('input_from', False):
                    setattr(self.context['input_from'], 'initial', dict_config)
                    filter_sonar = 'True'
            else:
                if status_code != 200:
                    self.context['status'] = values
                    if status_code == 403:
                        self.context['status'] = values + \
                            '. Please click <a href="/authorize">here</a> to change account'
                else:
                    self.context['status'] = 'Not found data config in Google Sheets file'
        self.context['filter_sonar'] = filter_sonar
        return render(request, SONARQUBE_PAGE, self.context)


class SonarFilterPageView(TemplateView):

    template_name = SONARQUBE_PAGE

    def post(self, request):
        print(1111111111111111)
        return JsonResponse({'summary': json.dumps({'message': 'aaaaaa'})})
