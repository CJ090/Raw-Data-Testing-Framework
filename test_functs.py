#from winreg import QueryInfoKey
from pandasql import sqldf
import pandas as pd

pysqldf = lambda q: sqldf(q, globals())

#this function should be the first step and be the prerequisite for the mapping_dict builder
#retool this
def column_check(any_file, mapping_dict):
    name = str(file.split('/')[-1])
    in_file = pd.read_csv(any_file, sep = '|')
    mapping = pd.read_excel(mapping_dict)
    result =  all(elem in mapping_dict["external_value"] for elem in in_file.columns)
    if result:
        print("All columns are according to our specs")
        req_cols['August'] = "Check"
        req_cols.to_excel("test_metrics_file.xlsx")
    else :
     print("columns are missing")

#This is a report
#QID 1
def ct_memb_rows (pysqldf,memb ,mapping_dict):
    query ="""Select "{member_number}", count(*) as 'Count of Member Numbers' from memb group by "{member_number}" """.format(
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output

# QID 2 
def ct_memb_membnum_unique(pysqldf,memb,mapping_dict):
    # pysqldf,mapping_dict = lambda q: sqldf(q, globals())
    #to make this dynamic, we would have to have the BE has the second parameter that would be pulled via the patient struct
    query ="""SELECT Count(distinct "{member_number}") as '# Unique member_numbers in member file'
    From memb
    where "{member_number}" is not null and length(trim("{member_number}")) > 1;""".format(
    member_number = mapping_dict['member.patient.member_number'])
    query_output = pysqldf(query)
    return query_output

# QID 3
def ct_memb_membnum_empty(pysqldf,memb ,mapping_dict):
    query  = """SELECT Count(*) as '#total number of null member_numbers as well trim values with spaces' from memb 
    where "{member_number}" is NULL or
    length(trim("{member_number}")) < 1;""".format(
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output

# QID 4
def ct_memb_membnum_nonunique(pysqldf,memb ,mapping_dict):
    query  = """select count(*) as '# Uniquely identifies a single member'
    from memb where "{member_number}" in(
    Select "{member_number}"
    From memb 
    Group by "{member_number}"
    Having count(distinct("{first_name}")) > 1
    or count(distinct("{last_name}")) > 1
    or count(distinct("{dob}")) > 1
    or count(distinct("{gender}")) > 1)""".format(
    member_number = mapping_dict["member.patient.member_number"],
    first_name = mapping_dict['member.patient.first_name'],
    last_name =mapping_dict['member.patient.first_name'],
    dob = mapping_dict['member.patient.date_of_birth'],
    gender = mapping_dict['member.patient.gender'])
    query_output = pysqldf(query)
    return query_output


#QID 5 REPLACE
def member_number_length_check(pysqldf,memb,mapping_dict):
    query  = """SELECT "{member_number}", length("{member_number}") AS member_number_length, 
    (case 
    when length("{member_number}") <= '200' then 'True' 
    when length("{member_number}") > '200' then 'False' 
    else '' end) AS Print 
    from memb
    GROUP BY 1;""".format(
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output


# QID 6
# Row 22 Data Predictability Test List
def ct_memb_fname_empty(pysqldf,memb,mapping_dict):
    query = """SELECT Count(*) as 'member_first_name: # records missing value in member file'
    from memb
    where "{PatientFirstName}" is null or
    length(trim ("{PatientFirstName}")) < 1;""". format(
    PatientFirstName=mapping_dict['member.patient.first_name'])
    query_output = pysqldf(query)
    return query_output


# QID 7
# Row 23 Data Predictability Test List
def ct_memb_fname_length(pysqldf,memb,mapping_dict):
    query = """SELECT count(Length("{PatientFirstName}")) as 'member_first_name: # records value too long in member file'
    from memb
    where Length("{PatientFirstName}") > 200;""". format(
    PatientFirstName=mapping_dict['member.patient.first_name'])
    query_output = pysqldf(query)
    return query_output   

# QID 8
# Row 24 Data Predictability Test List
def ct_memb_lname_empty(pysqldf,memb,mapping_dict):
    query = """SELECT Count(*) as 'member_last_name: # records missing value in member file' from memb
    where "{PatientLastName}" is null or
    length(trim("{PatientLastName}")) < 1;""". format(
    PatientLastName=mapping_dict["member.patient.last_name"])
    query_output = pysqldf(query)
    return query_output


# QID 9
# Row 25 Data Predictability Test List
def ct_memb_lname_length(pysqldf,memb,mapping_dict):
    query = """SELECT count(Length("{PatientLastName}")) as 'member_last_name: # records value too long in member file'
    from memb
    where Length("{PatientLastName}") > 200;""". format(
    PatientLastName=mapping_dict["member.patient.last_name"])
    query_output = pysqldf(query)
    return query_output

#This is not a agg count this is a detailed report
# QID 10
def rpt_memb_demographics(pysqldf,memb, mapping_dict):
    query = """Select "{member_number}", "{last_name}", "{first_name}", "{dob}", "{sex}", count("{member_number}") as count 
    from memb""".format(
    member_number = mapping_dict['member.patient.member_number'], 
    last_name = mapping_dict['member.patient.last_name'],
    first_name = mapping_dict['member.patient.first_name'], 
    dob = mapping_dict['member.patient.date_of_birth'],
    sex = mapping_dict['member.patient.gender'])
    query_output = pysqldf(query)
    return query_output

# QID 11
def ct_memb_dob_empty(pysqldf,memb,mapping_dict):
    query = """SELECT count(*) as '# records missing DOB'
    from memb
    where "{member_date_of_birth}" is null or
    length(trim("{member_date_of_birth}")) < 1;""".format(
    member_date_of_birth = mapping_dict['member.patient.date_of_birth'])
    query_output = pysqldf(query)
    return query_output

# QID 12
def rpt_memb_sex_valuelist(pysqldf, memb, mapping_dict):
    query  = """Select distinct "{gender}" from memb""".format(
    gender = mapping_dict["member.patient.gender"])
    query_output = pysqldf(query)
    return query_output



# QID 15
#Row 38 in Data Predictability Test List
def ct_memb_attr_npi_invalid(pysqldf,memb, mapping_dict):
    query = """Select count(*) from memb
    where length("{member_file_npi}") <> '10' and left("{member_file_npi}", 1) in('1', '2')""".format(
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output

# QID 20 
def ct_memb_tin_empty(pysqldf,memb, mapping_dict):
    query = """SELECT count(*) as 'Count of NULL TINs'
    from memb
    where "{member_file_tin}" is null or
    length(trim("{member_file_tin}")) < 1;""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output



# QID 16
def ct_memb_attr_npi_lookup(pysqldf,memb,prov, mapping_dict):
    query="""Select count(*) as 'Member NPI not in provider file (# records)',
    count(distinct "{member_number}") as 'Member NPI not in provider file (# members)', 
    count(distinct "{member_file_npi}") as 'Member NPI not in provider file (# NPIs)'
    from memb
    where "{member_file_npi}" not in (Select "{provider_npi}" From prov);  """.format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_npi = mapping_dict["provider.npi"],
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output  

#!
# QID 18 
def ct_memb_prov_attr_npi_multi_tins (pysqldf,memb,prov,mapping_dict):
    query = """Select count(*) as '# count of npis with their multi tins'
    from (
    Select "{member_file_npi}", count(distinct "{provider_file_tin}")
    from memb
    Join prov
    on "{provider_file_npi}" = "{member_file_npi}"
    group by 1
    having count(distinct "{provider_file_tin}") >1 ) as B;""" .format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_file_npi = mapping_dict["provider.npi"],
    provider_file_tin = mapping_dict["provider.medical_group_tin"])
    query_output = pysqldf(query)
    return query_output





def not_null_members(pysqldf,memb,mapping_dict):
    #Need to replace dynamic
    query = """Select "{member_number}", count(*) as Count_null, (case when "{member_number}" is null
    then 'False'
    else 'True'
    end) as Print
    from memb
    GROUP BY 1;""".format(
    member_number = mapping_dict['member.patient.member_number'])
    query_output = pysqldf(query)
    return query_output
    
##WIP if we have to dynamically call the number of columns relevant in this query how would we get that number.
#def duplicate_member(pysqldf,mapping_dict):
#query = """Select "{member_number}", "{last_name}", "{first_name}", "{dob}", "{sex}","{dod}", count("{member_number}") as count from file1 group by 6 having count(1)>1 order by "{first_name}", "{last_name}""""
#query_output = pysqldf(query)
#return query_output


# QID 21
def ct_memb_prov_tin_unique(pysqldf,memb, prov, mapping_dict):
    query="""Select count(distinct "{member_file_tin}" ) as # of unique TINs in the member file that are not in the provider file
    from memb
    where "{member_file_tin}" not in (select "{provider_file_tin}"
                                          from Customer".Provider_File );""".format(
    member_file_tin = mapping_dict["member.patient.tin"],
    provider_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output


# QID 22
def patient_attr_npi_not_in_prov(pysqldf,memb,prov, mapping_dict):
    query="""Select count(distinct "{member_number}") as 'Patients whos attributed provider not in provider file'
    from memb 
    Join prov 
    On memb."{member_file_npi}" = prov."{provider_npi}"
    where memb."{member_file_npi}" not in (Select prov."{provider_npi}"
    from prov);""".format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_npi = mapping_dict["provider.npi"],
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output  

# QID 26
def ct_prov_npi_empty(pysqldf,prov,mapping_dict):
    query = """Select count(*) as 'Missing NPI in provider file (# records)'
    From prov
    where "{provider_file_npi}" is null
    or length(trim("{provider_file_npi}")) < 1
    and length("{provider_file_npi}") <> '10';""".format(
    provider_file_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output

# QID 28
def ct_prov_npi_valid (pysqldf,prov,mapping_dict):
    query = """Select count(*) as 'Valid NPI in provider file (# records)'
    from prov
    where length("{provider_file_npi}") = '10'
    and left("{provider_file_npi}", 1) in('1', '2');""".format(
    provider_file_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output


#Might Depreciate
def date_of_death_format_check(pysqldf,memb, mapping_dict):
    query = """Select "{dod}", (case when "{dod}" like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    then 'True'
    else 'False'
    end) as Print
    from memb""".format(
    dod=mapping_dict['member.date_of_death'] )
    query_output = pysqldf(query)
    return query_output


# row 64??
def npi_attribution_check(pysqldf,memb, prov,mapping_dict):
    #memb_file  =pd.read_csv(memb, sep='|', encoding='latin')
    #prov_file = pd.read_excel(prov)
    query = """Select count (distinct"{member_file_npi}")
    from memb 
    Join prov
    on memb."{member_file_npi}" = prov."{provider_npi}" """.format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output


#def patient_attr_tin_not_in_prov(pysqldf,memb,prov,mapping_dict):
#    query="""Select count(distinct "{member_number}") 
#    from memb
#    Join prov
#    On memb."{member_file_tin}" = prov."{proviver_tin}"
#    where memb."{member_file_tin}" not in (Select prov."{proviver_tin}"
#    from prov);""".format(
#    member_number = mapping_dict["member.patient.member_number"],
##    member_file_tin = mapping_dict[],
#  ß provider_tin = mapping_dict[])
  #  query_output = pysqldf(query)
  #  return query_output  

def npi_reverse_check(pysqldf,memb, prov,mapping_dict):
    query  = """Select count(distinct memb."{member_file_npi}") 
    from memb
    Join prov
    on memb."{member_file_npi}" = prov."{provider_npi}"
    where memb."{member_file_npi}" not in (Select prov."{provider_npi}"
    from prov);""".format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output


#needs a name
def member_number_something(pysqldf,memb,mapping_dict):
    query  = """SELECT "{member_number}", count("{member_number}") as count_rows, 
    (case 
    when count("{member_number}") = 1
    then 'True'
    else 'False'
    end )
    from memb
    GROUP BY 1;""".format(
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output

 #Demographics tests   
#def demographic_error_count(pysqldf,memb,mapping_dict):
#    query  = """SELECT memb, "{last_name}", "{first_name}", "{dob}", "{gender}",
#       (case
#           when bene_1st_name is null then 'Error'
#           when bene_last_name is null then 'Error'
#           when bene_sex_cd is null then 'Error'
#           when bene_brth_dt is null then 'Error'
#           else 'Good'
#           end) as Print
#    from memb;
#""".format(
#     = mapping_dict_field[mapping_dict_column]
#    )
#    query_output = pysqldf(query)
#    return query_output




#@Here
def date_of_birth_format_check(pysqldf,memb, mapping_dict):
    query = """Select "{dob}", (case when "{dob}" like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
    then 'True'
    else 'False'
    end) as Print
    from memb""".format(
    dob = mapping_dict['member.patient.date_of_birth'])
    query_output = pysqldf(query)
    return query_output

#Assumes there is a provider field in the member file
def not_null_attributed_provider_npi(pysqldf,memb, mapping_dict):
    query = """Select count(*)
    from memb
    where "{member_file_npi}" is not null""".format(
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output

def null_attributed_provider_npi(pysqldf,memb, mapping_dict):
    query = """Select count(*)
    from memb
    where "{member_file_npi}" is null;""".format(
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output


def attr_prov_tin_null_trim(pysqldf,memb, mapping_dict):
    query = """SELECT count(*)
    from memb
    where "{member_file_tin}" is null
    "{member_file_tin}" in (select Trim("{member_file_tin}") from memb );""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output

def providers_without_validNPI(pysqldf,prov, mapping_dict):
    query = """Select count(*) as 'Providers without valid NPIs'
    From prov
    where "{provider_file_npi}" is not null 
    and "{provider_file_npi}" in(Select Trim("{provider_file_npi}") From prov) 
    and length("{provider_file_npi}") = '10';""".format(
    provider_file_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output

def patients_null_tin_attr(pysqldf,memb, mapping_dict):
    query="""Select count(distinct "{member_number}") as 'Patients attributed to null TINs'
    from memb 
    where "{member_file_tin}" is null;""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"],
    member_number = mapping_dict["member.patient.member_number"])
    query_output = pysqldf(query)
    return query_output  

def lengthcase_attributed_provider_tin(pysqldf,memb, mapping_dict):
    query = """SELECT count("{member_file_tin}"), length("{member_file_tin}") AS Length_tin
    from memb
    where Length_tin = '9'
    and Length_tin < '9';""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output

# QID 14
def ct_memb_attr_npi_unique(pysqldf,memb, mapping_dict):
    query="""Select count(distinct "{member_file_npi}") as 'Unique NPIs in Member file'
    from memb ;""".format(
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output  

def unique_attr_prov_tin(pysqldf,memb, mapping_dict):
    query="""Select count(distinct "{member_file_tin}") as 'Unique TINs in Member File'
    from memb ;""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output  

def unique_tin_in_membershipfile(pysqldf,memb, prov, mapping_dict):
    query="""Select distinct "{member_file_npi}"
    from memb
    Join prov
    On memb."{member_file_tin}" = prov."{provider_file_tin}" """.format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_file_tin = mapping_dict["member.medicalgroup.tin"])
    query_output = pysqldf(query)
    return query_output  

#confused on the purpose of this function
def unique_npi_in_membershipfile(pysqldf,memb,prov, mapping_dict):
    query="""Select distinct "{member_file_npi}"
    from memb
    Join prov
    On memb."{member_file_npi}" = prov."{provider_file_npi}" 
    where memb."{member_file_npi}" not in (Select "{provider_file_npi}" From prov);""".format(
    member_file_npi = mapping_dict["member.patient.npi"],
    provider_file_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output  

# QID 23
# No mapping for SLHP 
def ct_memb_dod_empty (pysqldf,memb,mapping_dict):
    query = """Select count("{member_file_dod}")
    from memb
    where "{member_file_dod}" is null
    or length(trim("{member_file_dod}"));""".format(
    member_file_dod = mapping_dict["member.patient.dod"])
    query_output = pysqldf(query)
    return query_output


# QID 24
def unique_prov_file_npi(pysqldf,prov, mapping_dict):
    query = """Select count(distinct "{provider_file_npi}") 
    from prov;""".format(
    provider_file_npi = mapping_dict["provider.npi"])
    query_output = pysqldf(query)
    return query_output  

# QID 25
def ct_prov_tin_unique(pysqldf,prov, mapping_dict):
    query = """Select count(distinct "{provider_file_tin}") as 'Unique TINs in the Provider File' 
    from prov;""".format(
    provider_file_tin = mapping_dict["provider.medical_group_tin"])
    query_output = pysqldf(query)
    return query_output  

# Row 74 in Data Predictability Test List
def providers_with_NoTIN(pysqldf,prov, mapping_dict):
    query = """Select "{provider_file_npi}", count("{provider_file_npi}")
    From prov
    where "{provider_file_tin}" is null;""".format(
    provider_file_tin = mapping_dict["provider.tin"])
    query_output = pysqldf(query)
    return query_output
#QID 27 Updated Query
def ct_prov_tin_empty(pysqldf,prov,mapping_dict):
    query = """Select count(*) as 'Missing TIN in provider file (# records)', 
    count(distinct "{provider_file_npi}") as 'Missing TIN in provider file (# providers)',
    count(distinct "{medical_group_name}") as 'Missing TIN in provider file (# MGs)'
    From prov
    where TIN is null
    or length(trim(tin)) < 1;""".format(
    medical_group_name = mapping.file["provider.medical.group.name"],
    provider_file_tin = mapping_dict["provider.tin"])
    query_output = pysqldf(query)
    return query_output


def membership_count_MultiTINs_perNPI(pysqldf,memb, mapping_dict):
    query ="""SELECT distinct "{member_file_npi}", count(distinct "{member_file_tin}")
    FROM memb
    GROUP BY "{member_file_npi}"
    Having count(distinct "{member_file_tin}") > 1
    Order by 1""".format(
    member_file_npi = mapping_dict["member.patient.npi"] )
    query_output = pysqldf(query)
    return query_output

# QID 29 THis 
#Row 72 in Data Predictability Test List
def ct_prov_npi_multi_tins(pysqldf,prov, mapping_dict):
    query = """ Select count(*) as List of TINs per NPI in the Provider file
    SELECT distinct "{provider_file_npi}", count(distinct "{providerfile_tin}")
    FROM prov
    GROUP BY "{provider_file_npi}"
    Having count(distinct "{provider_file_tin}") > 1
    Order by 1""".format(
    provider_file_npi = mapping_dict["provider.npi"],
    provider_file_tin = mapping_dict["provider.tin"])
    query_output = pysqldf(query)
    return query_output
    

# QID 31
#Row 72 in Data Predictability Test List
def rpt_prov_npi_multi_tins(pysqldf,prov, mapping_dict):
    query = """SELECT distinct "{provider_file_npi}", count(distinct "{member_file_tin}")
    FROM prov
    GROUP BY "{provider_file_npi}"
    Having count(distinct "{provider_file_tin}") > 1
    Order by 1""".format(
    provider_file_npi = mapping_dict["provider.npi"],
    provider_file_tin = mapping_dict["provider.tin"])
    query_output = pysqldf(query)
    return query_output

# QID 32
def rpt_prov_tin_rollup (pysqldf,memb,prov,mapping_dict):
    query = """select "{provider_file_tin}", count(distinct "{provider_file_npi}") as '# NPIs', count(distinct member_number) as '# Patients'
    from prov
    join memb
    on "{provider_file_npi}" = "{member_file_npi}"
    group by 1
    order by 1;""".format(
    member_file_npi = mapping_dict["member.patient.npi"],
    member_number = mapping_dict["member.patient.member_number"],
    provider_file_npi = mapping_dict["provider.npi"],
    provider_file_tin = mapping_dict["provider.tin"])
    query_output = pysqldf(query)
    return query_output    

#Might be replaced above??
def membership_list_MultiTINs_perNPI(pysqldf,memb, mapping_dict):
    query ="""Select "{member_file_npi}", "{member_file_tin}"
    from memb
    where "{member_file_npi}" in (
    SELECT distinct "{member_file_npi}"
    FROM memb
    GROUP BY "{member_file_npi}"
    Having count(distinct "{member_file_tin}") > 1)
    Group by 1,2
    Order by 1;""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"],
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output
    
#Row 72 in Data Predictability Test List
def provider_list_MultiTINs_perNPI(pysqldf,prov, mapping_dict):
    query = """SELECT distinct "{member_file_npi}", count(distinct "{member_file_tin}")
    FROM prov
    GROUP BY "{member_file_npi}"
    Having count(distinct "{member_file_tin}") > 1
    Order by 1""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"],
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output

#Row 72 in Data Predictability Test List
def providers_list_MultiTINs_perNPI(pysqldf,memb,prov,mapping_dict):
    query ="""Select "{member_file_npi}", "{member_file_tin}"
    from prov
    where "{member_file_npi}" in (
    SELECT distinct "{member_file_npi}"
    FROM memb
    GROUP BY "{member_file_npi}"
    Having count(distinct "{member_file_tin}") > 1)
    Group by 1,2
    Order by 1;""".format(
    member_file_tin = mapping_dict["member.medicalgroup.tin"],
    member_file_npi = mapping_dict["member.patient.npi"])
    query_output = pysqldf(query)
    return query_output
