import pip
import pandas as pd

def import_or_install():
    package_list = ['pandas', 'pandasql','openpyxl']
    for i in package_list:
        name = i
        try:
            __import__(i)
            print("Packagage requirement for {package} satisfied; {package} imported".format(package = name))
        except ImportError:
            print("{package} not installed".format(package = name))
            pip.main(['install', i])      

import_or_install()

def attribution_join(member, provider):
    memb = pd.read_csv(memb_select, encoding = 'latin', on_bad_lines="skip")
    prov = pd.read_csv(prov_select, encoding = 'latin', on_bad_lines="skip")
    merged = memb.merge(prov, how = "inner", left_on ="PCP_Prv_NPI", right_on = 'Prv_NPI')
    return merged

def some_join_function(memb_select, prov_select):
    memb = pd.read_csv(memb_select, encoding = 'latin', on_bad_lines="skip")
    prov = pd.read_csv(prov_select, encoding = 'latin', on_bad_lines="skip")
    merged = memb.merge(prov, how = "inner", left_on ="PCP_Prv_NPI", right_on = 'Prv_NPI')
    return merged

def client_constructor(file):
    mapping = dict(zip(file.stellar_value,file.external_column))
    return mapping

def memb_prov_join(memb_select, prov_select,mapping):
    """Join configuration that takes a member demographic file and a provider roster"""
    memb = pd.read_csv(memb_select, sep ="|", encoding = 'latin', on_bad_lines="skip")
    #change it back for provider ,"encoding = 'latin, on_bad_lines="skip"'""
    prov = pd.read_excel(prov_select)
    merged = memb.merge(prov, how = "inner", right_on = 'AttributedNPI', left_on= "NPI Number")
    #merged = memb.merge(prov, how = "inner", left_on =memb_select[mapping["member.patient.npi"]], right_on = prov_select[mapping["provider.npi"])
    return merged

#Assumes that there is a one to one relationship between the file extensions and the delimiter types
def file_ingest(file):
    if str(file.split(".")[-1]) ==  "xlsx":
        df = pd.read_excel(file)
    elif str(file.split(".")[-1]) ==  "txt":
        df = pd.read_csv(file, sep = r'[,|;\t"]+(?=\S)')
    elif str(file.split(".")[-1]) ==  "csv": 
        df = pd.read_csv(file)
    return(df)

