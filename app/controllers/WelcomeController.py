"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
import csv
from app.models.Nation import Nation
from app.models.IpRange import IpRange
from app.models.Jobs import Jobs
import json
from masonite.request import Request
from masonite.response import Response

class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        return view.render("welcome")
    '''
    def load_jobs(self, view: View):

        i = 0
        for k in range(0, 60*10):
            Jobs.create({
                'name': 'Job_' + str(k),
                'class_name': 'Job_1',
                'interval': 60,
                'args': json.dumps({'': ''}),
                'start_second': i,
                'run': True 
            })
            if i == 59:
                i = -1
            i += 1
    '''   

    def load_jobs(self, view: View):

        nations = Nation.all()
        i = 0
        count = 0
        max = 600
        for k in range(0, max):
            for nation in nations:

                if count == max:
                    break

                Jobs.create({
                    'name': 'Job_' + nation['key']+"_"+str(k),
                    'class_name': 'Job_ping',
                    'interval': 60,
                    'args': json.dumps({'nation_key': nation['key']}),
                    'start_second': i,
                    'run': True
                })
                print(nation['key'])
                print(nation.ipRange.all())

                count = count + 1

                if i == 59:
                    i = -1
                i += 1



    def load_jobs_old(self, view: View):

        nations = Nation.all()
        i = 0
        i_sub = 0
        for nation in nations:
            Jobs.create({
                'name': 'Job_' + nation['key'],
                'class_name': 'Job_ping',
                'interval': 60,
                'args': json.dumps({'nation_key': nation['key']}),
                'start_second': i,
                'run': True if i < 60 else False
            })
            print(nation['key'])
            print(nation.ipRange.all())

            #if i_sub == 29:
            #if i_sub == 9:
            #    i += 1
            #    i_sub = -1
            #i_sub += 1
            i += 1

        return view.render("welcome")
    
    def load(self, view: View):

        f = open('./resources/csv_file_list.txt', 'r')
        r = csv.reader(f, delimiter=',', quotechar='|')

        for line in r:
            key, file_name = line[0].split('_')
            nation = file_name.split('.')[0]
            print(key, nation)
            Nation.create({
                'key': key,
                'name': nation,
            })
            
            
            nation_file = open('./resources/csv/' + key + '_' + file_name, 'r')
            reader_nation = csv.reader(nation_file, delimiter=',', quotechar='|')
            for addrs in reader_nation:
                print(addrs)
                if addrs:
                    IpRange.create({
                        'key_nation': key,
                        'start': addrs[0],
                        'end': addrs[1]
                    })

        return view.render("welcome")

    def gra(self, request: Request, response: Response):
        print('login')
        print(request)
        return response.json({'prova': 'ciao'})