import sys, os, pprint, traceback, time, re
import csv
import sqlite3
import json
import pandas as pd, sqlite3, csv

from time import sleep

from celery import shared_task, current_task
from celery.result import AsyncResult

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import json
from .forms import UploadFileForm
from website_gpt_categorizer.gpt_file_processor import file_processor, single_element_processor

# Create your views here.

csvframe=pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6])
@shared_task(bind=True)
def do_work(self, elements):
    """ Get some rest, asynchronously, and update the state all the time """
    for i in range(len(elements)):
        sleep(0.1)
        element_list=single_element_processor(elements[i])
        csvframe.loc[i,0]=elements[i]
        for x in range(len(element_list)):
            csvframe.loc[i,x+1]=element_list[x]
        current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': len(elements)})


def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state
    return HttpResponse(json.dumps(data), mimetype='application/json')


def csv_process(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csvframe=pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6]) #resets the dataframe
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            elements = df.iloc[:, 0].tolist()
            # print(elements)
            do_work(elements)
            csv_output = csvframe.to_csv(index=False)
            response = HttpResponse(csv_output, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'
            return response
    else:
        form = UploadFileForm()
    return render(request, 'read_file.html', {'form': form})



# def progress_view(request):
#     result = my_task.delay(10)
#     return render(request, 'display_progress.html', context={'task_id': result.task_id})
