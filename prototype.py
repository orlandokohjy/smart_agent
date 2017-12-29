import requests
from bs4 import BeautifulSoup
import xmltodict

url = 'http://comparefirst.sg/wap/searchProductsEvent.action'

headers = {}
headers['content-type'] = 'application/x-www-form-urlencoded'
headers['origin'] = 'http://comparefirst.sg'
headers['Referer'] = 'http://comparefirst.sg/wap/homeEvent.action'

payload = "productGroup=invst&searchproduct=&prodGroup=bips&pageAction=search" \
+ "&breadCrumb=null&viewProdsId=null&ProdsCompIDs=null&ProdsVisibleIDs=null" \
+ "&subCatSeleJson=null&subCatCountJson=null&sortOrderSelected=null" \
+ "&reportProdsCompIDs=null&searchResInitCount=10&searchResIncCount=5" \
+ "&gaSearchSummary=null&prodStringXML=&prodSummaryTxt=&premiumTypeOther=Annual&premiumTypeDCIPs=Annual" \
+ "&coverageTermTLNonDCIP=select&coverageTermTLAllList=select&coverageTermEndow=select" \
+ "&premiumTermAll=select&premiumTermNonDcips=select&PremAnnualGroup=select"\
+ "&PremSingleGroup=select&SATLAll=select&SAWLAll=select&SATLNonDCIPS=select&SAWLNonDCIPS=select" \
+ "&sortNonWLGroup=1&sortWLGroup=1&sortEndoGroup=select" \
+ "&selCategory={0}" \
+ "&selGender={1}" \
+ "&selSmokStatus={2}" \
+ "&dob={3}" \
+ "&selCIRider={4}" \
+ "&coverageTermTLDCIPs={5}" \
+ "&SATLDCIPS={6}" \
+ "&premiumTermDcips={7}" \
+ "&SAWLDCIPS={8}" 

# premiumTypeOther = "Annual", premiumTypeDCIPs = "Annual"
# Category : term-life, whole-life
selCategory = ["term-life", "whole-life"]
# Gender : M, F
selGender = ["M", "F"]
# Smoke Status : Y, N
selSmokStatus = ["Y", "N"]
# Date of Birth : dd%2Fmm%2Fyyyy
dob = ["10%2F10%2F{0}".format(i) for i in range(1970,2018)]
# Critical Illness Benefits : Y, N
selCIRider = ["Y", "N"]

# ---------------------- Term Life ----------------------
# Coverage Term : 5+Years, 20+Years, To+Age+65
coverageTermTLDCIPs = ["5+Years", "20+Years", "To+Age+65"]
# Sum Assured : 50000, 100000, 200000, 300000, 400000
SATLDCIPS = ["50000", "100000", "200000", "300000", "400000"]
# Sort Result By : 1, 2, 3, 4 (doesn't matter ATM)
# sortNonWLGroup = ""

# ---------------------- Whole Life ----------------------
# Coverage Term : To+age+70, To+age+85
premiumTermDcips = ["To+age+70", "To+age+85"]
# Sum Assured : 50000, 100000, 200000
SAWLDCIPS = ["50000", "100000", "200000"]
# Sort Result By : 1, 2, 3, 4, 5, 6 (doesn't matter ATM)
# sortWLGroup = ""

# ---------------------- payload ----------------------
# payload.format(selCategory,selGender,selSmokStatus,dob,selCIRider,\
# 	coverageTermTLDCIPs,SATLDCIPS,premiumTermDcips,SAWLDCIPS))

#def createcsv(filename, dict):
#	dict['ProdList']['Product'][i].keys()
#		['id', 'InsurerId', 'InsurerName', 'InsurerIcon', 
#		 'ProductId', 'ProductName', 'ProductIcon', 'ProductGroup',
#		 'ProductSubCategory', 'ProductSubCategoryID', 'SumAssured', 
#		 'CoverageTerm', 'AnnualPremium', 'TotalPremium', 'AnnualPremiumNum', 
#		 'TotalPremiumNum', 'PremiumPaymentMode', 'PremiumPayPeriod', 
#		 'upondeathGuaranteedAmount5Year', 'upondeathGuaranteedAmount10Year', 
#		 'upondeathGuaranteedAmount20Year', 'upondeathGuaranteedAmount30Year', 
#		 'DistributedCost', 'CreditRating', 'ProductFeatures1', 'ProductFeatures2', 
#		 'ProductFeatures3', 'ProductFeatures4', 'ProductFeatures5', 'ProductFeatures6', 
#		 'ProductFeatures7', 'ProductFeatures8', 'ProductFeatures9', 'ProductFeatures10', 
#		 'CiRideApp', 'TpdRideapp', 'OptlRide1', 'OptlRide2', 'OptlRide3', 'OptlRide4', 
#		 'OptlRide5', 'CompulRide1', 'CompulRide2', 'CompulRide3', 'CompulRide4', 
#		 'CompulRide5', 'ProductSummary2', 'ProductSummary3', 'ProductSummary4', 
#		 'ProductSummary5', 'exclusionsURL', 'brochureURL', 'InsurerInfoURL', 
#		 'ContactInsurer', 'LastUpdatedOn', 'Subtitle']
#	file = open(filename, 'w')
#	for i in range(len(dict['ProdList']['Product'])):
#		for key in dict['ProdList']['Product'][i]:
#			if dict['ProdList']['Product'][i][key] is not None:
#				file.write(dict['ProdList']['Product'][i][key])
#		file.write('\n')
#	file.close()

# Testing 1
# get (1970 - 2017)

file = open('test.csv', 'w')
for gender in selGender:
	for smokeStatus in selSmokStatus:
		for dateOfBirth in dob:
			print("Downloading year @ {0}".format(dateOfBirth))
			for criticalIllness in selCIRider:
				for coverageTerm in coverageTermTLDCIPs:
					for sumAssured in SATLDCIPS:
						testPayload = payload.format(selCategory[0], gender, smokeStatus, \
							dateOfBirth, criticalIllness, coverageTerm, sumAssured, "", "")
						r = requests.post(url, headers=headers, data=testPayload)
						bs = BeautifulSoup(r.text, 'html.parser')
						xml = bs.find(id = 'prodStringXML')
						xml = xml.get('value')
						dic = xmltodict.parse(xml, xml_attribs=True)
						# make csv here
						# createcsv(dateOfBirth+'.txt', dic)
						try:
							print('Writing...')
							for i in range(len(dic['ProdList']['Product'])):
								writeString = ""
								for key in dic['ProdList']['Product'][i]:
									if dic['ProdList']['Product'][i][key] != None \
									and dic['ProdList']['Product'][i][key] != 'null':
										writeString += dic['ProdList']['Product'][i][key]
									writeString += ","
								writeString = writeString[:-1] # slice off the last comma
								writeString += "\n"
								file.write(writeString)
						except Exception as e:
							print(e)
							print("{0}, {1}, {2}, {3}, {4}, {5}".format( \
								gender, smokeStatus, dateOfBirth, criticalIllness, \
								coverageTerm, sumAssured))
file.close()













