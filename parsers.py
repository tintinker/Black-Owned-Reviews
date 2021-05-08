'''
-------------------------------Seattle Methods----------------------------------
'''

def Seattle_Addr(row):
    return f'{row["Street Address"]}, {row["City"]} {row["State"]} {row["Zip"]}'

def Seattle_Name(row):
    return row["Trade Name"]

def Seattle_Filter(df):
    return  (df["NAICS Description"] == "Full-Service Restaurants") | (df["NAICS Description"] == "Limited-Service Restaurants")


'''
-------------------------------Los Angeles Methods----------------------------------
'''

def LA_Addr(row):
    return f'{row["STREET ADDRESS"]}, {row["CITY"]} CA {row["ZIP CODE"]}'

def LA_Name(row):
    return row["DBA NAME"]

def LA_Filter(df):
    return  (df["PRIMARY NAICS DESCRIPTION"] == "Full-service restaurants") | (df["PRIMARY NAICS DESCRIPTION"] == "Limited-service eating places")


'''
-------------------------------San Francisco Methods----------------------------------
'''
def SF_Addr(row):
    return f'{row["Mail Address"]}, {row["Mail City"]} {row["Mail State"]} {row["Mail Zipcode"]}'

def SF_Name(row):
    return row["DBA Name"]

def SF_Filter(df):
    return  (df["NAICS Code Description"] == "Food Services")

'''
-------------------------------Chicago Methods----------------------------------
'''

def Chicago_Addr(row):
    return f'{row["ADDRESS"]}, {row["CITY"]} {row["STATE"]} {row["ZIP CODE"]}'

def Chicago_Name(row):
    return row["DOING BUSINESS AS NAME"]

def Chicago_Filter(df):
    return  df["LICENSE DESCRIPTION"] == "Retail Food Establishment"


'''
-------------------------------Add More Here----------------------------------
'''
