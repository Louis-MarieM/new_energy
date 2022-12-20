from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response

from scraping.forms import LoginForm
from scraping.services.fournisseurs.totalenergies import FournisseurTotalEnergies as totalEnergies
from scraping.services.constantes.constantes import Constantes as const
from scraping.models import User

def launcher(request):
    if request.method == 'POST':
        global wait, browser, Link
        form = LoginForm(request.POST)
        
        if form.is_valid():
            print("Les logs sont : " + form.cleaned_data['website'], form.cleaned_data['identifier'], form.cleaned_data['password'])
            totalEnergies.energy_login("https://clientsgc.totalenergies.fr/connexion-clients-collectivites/", form.cleaned_data['identifier'], form.cleaned_data['password'])
            totalEnergies.access_factures()
            totalEnergies.download_factures()
            return render(request, 'scraping/succes.html')
    else :
        form = LoginForm()
    return render(request, 'scraping/launcher.html', {'form': form})


class UserView(APIView) :

    def get(self, *args, **kwargs) :
        success = False
        message = ""
        processId = ""
        filenames = []
        user = User("", "")
        try:
            processId = self.request.GET.get("processId")
            folderPath = user.getDownloadFolder(processId)
            print(folderPath)
            if os.path.exists(folderPath):
                filenames = os.listdir(folderPath)
        except Exception as e :
            message = str(e)
        return Response({
            "success" : success,
            "message" : message,
            "provider" : self.request.GET.get("provider"),
            "processId" : processId,
            "jobId" : self.request.GET.get("jobId"),
            "filenames" : filenames
        })

    def put(self, *args, **kwargs) :
        success = False
        provider = ""
        processId = ""
        jobId = ""
        user = User("", "")
        try:
            provider = const.FOURNISSEURS[self.request.GET.get("provider")]
            processId = self.request.GET.get("processId")
            user.setUsername(self.request.GET.get("username"))
            user.setPassword(self.request.GET.get("password"))
            success = totalEnergies.energy_login(provider, user, processId)
            return Response({
                    "success" : success,
                    "provider" : self.request.GET.get("provider"),
                    "processId" : processId,
                    "jobId" : self.request.GET.get("jobId"),
                    "username" : user.getUsername(),
                    "password" : user.getPassword()
                })
        except Exception as e :
            return Response({'error' : str(e)})

class FactureView(APIView) : 

    def get(self, *args, **kwargs) :
        success = False
        message = ""
        provider = ""
        processId = ""
        jobId = ""
        user = User("", "")
        filenames = ""
        try :
            provider = self.request.GET.get("provider")
            providerWebsite = const.FOURNISSEURS[provider]
            processId = self.request.GET.get("processId")
            jobId = self.request.GET.get("jobId")
            user.setUsername(self.request.GET.get("username"))
            user.setPassword(self.request.GET.get("password"))
            totalEnergies.energy_login(providerWebsite, user, processId)
            totalEnergies.access_factures()
            success = totalEnergies.download_factures()
        except Exception as e :
            message = str(e)
        if success:
            folderName = user.getDownloadFolder(processId)
            filenames = os.listdir(folderName)
        return Response({
                "success" : success,
                "message" : message,
                "filenames" : filenames,
                "provider" : provider,
                "processId" : processId,
                "jobId" : jobId,
                "username" : user.getUsername(),
                "password" : user.getPassword()
            })
            
    def put(self, *args, **kwargs) :
        success = False
        message = ""
        provider = ""
        processId = ""
        jobId = ""
        user = User("", "")
        filenames = ""
        try:
            provider = self.request.GET.get("provider")
            processId = self.request.GET.get("processId")
            jobId = self.request.GET.get("jobId")
            success = totalEnergies.decoupage(user, processId)
        except Exception as e :
            message = str(e)
        if success:
            folderName = user.getDecoupageFolder(processId)
            filenames = os.listdir(folderName)
        return Response({
            "success" : success,
            "message" : message,
            "filenames" : filenames,
            "provider" : provider,
            "processId" : processId,
            "jobId" : jobId
        })