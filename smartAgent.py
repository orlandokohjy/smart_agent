import requests
from bs4 import BeautifulSoup
import xmltodict
import sys

url = 'http://comparefirst.sg/wap/searchProductsEvent.action'

headers = {}
headers['content-type'] = 'application/x-www-form-urlencoded'
headers['origin'] = 'http://comparefirst.sg'
headers['Referer'] = 'http://comparefirst.sg/wap/homeEvent.action'

# ----------------- This setting is for 'direct purchase' -----------------
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
# dob = ["10%2F10%2F{0}".format(i) for i in range(1970,2018)]
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
# Premium Term : To+age+70, To+age+85
premiumTermDcips = ["To+age+70", "To+age+85"]
# Sum Assured : 50000, 100000, 200000
SAWLDCIPS = ["50000", "100000", "200000"]
# Sort Result By : 1, 2, 3, 4, 5, 6 (doesn't matter ATM)
# sortWLGroup = ""

# ---------------------- payload ----------------------
# payload.format(selCategory,selGender,selSmokStatus,dob,selCIRider,\
# 	coverageTermTLDCIPs,SATLDCIPS,premiumTermDcips,SAWLDCIPS))



# ---------------------- keys ----------------------
keys = ['id', 'InsurerId', 'InsurerName', 'InsurerIcon', 'ProductId', 'ProductName', \
 'ProductIcon', 'ProductGroup', 'ProductSubCategory', 'ProductSubCategoryID', \
 'SumAssured', 'CoverageTerm', 'AnnualPremium', 'TotalPremium', 'AnnualPremiumNum', \
 'TotalPremiumNum', 'PremiumPaymentMode', 'PremiumPayPeriod', 'upondeathGuaranteedAmount5Year', \
 'upondeathGuaranteedAmount10Year', 'upondeathGuaranteedAmount20Year', \
 'upondeathGuaranteedAmount30Year', 'DistributedCost', 'CreditRating', 'ProductFeatures1', \
 'ProductFeatures2', 'ProductFeatures3', 'ProductFeatures4', 'ProductFeatures5', 'ProductFeatures6', \
 'ProductFeatures7', 'ProductFeatures8', 'ProductFeatures9', 'ProductFeatures10', 'CiRideApp', \
 'TpdRideapp', 'OptlRide1', 'OptlRide2', 'OptlRide3', 'OptlRide4', 'OptlRide5', 'CompulRide1', \
 'CompulRide2', 'CompulRide3', 'CompulRide4', 'CompulRide5', 'ProductSummary2', 'ProductSummary3', \
 'ProductSummary4', 'ProductSummary5', 'exclusionsURL', 'brochureURL', 'InsurerInfoURL', \
 'ContactInsurer', 'LastUpdatedOn', 'Subtitle']

def main():
	errorLog = open("errorLog.txt", 'w')

	# category = 'term-life':
	file = open(selCategory[0] + ".csv", 'w')

	# create titles for the csv
	titles = ""
	for key in keys:
		titles = titles + key + ","
	titles = titles[:-1] # slice off the last comma
	titles = titles + "/n"
	file.write(titles)
	
	for dob in DOB:
		print("Downloading {0} data for {1}".format(selCategory[0],dob.replace("%2F", "/")))
		for gender in selGender:
			for smokeStatus in selSmokStatus:
				for cib in selCIRider:
					for coverageTerm in coverageTermTLDCIPs:
						for sumAssured in SATLDCIPS:
							formattedPayload = payload.format(selCategory[0], \
								gender, smokeStatus, dob, cib, coverageTerm, \
								sumAssured, "", "")
							r = requests.post(url, headers=headers, data=formattedPayload)
							bs = BeautifulSoup(r.text, 'html.parser')
							xml = bs.find(id="prodStringXML")
							xml = xml.get('value')
							dic = xmltodict.parse(xml, xml_attribs=True)
							try:
								print("reading data ...")
								for i in range(len(dic['ProdList']['Product'])):
									writeString = ""
									for key in keys:
										if dic['ProdList']['Product'][i][key] != None \
										and dic['ProdList']['Product'][i][key] != 'null':
											writeString += dic['ProdList']['Product'][i][key] + ","
										else:
											writeString += "NA,"
									writeString = writeString[:-1] # slice off the last comma
									writeString += "\n"
									file.write(writeString)
							except Exception as e:
								print(e)
								errorLog.write(str(e))
								errorLog.write("Error for {0}, {1}, {2}, {3}, {4}, {5}, {6}\n".format( \
									selCategory[0], dob, gender, smokeStatus, cib, coverageTerm, sumAssured))
	file.close()
	

	file = open(selCategory[1] + ".csv", 'w')
	
	# create titles for the csv
	titles = ""
	for key in keys:
		titles = titles + key + ","
	titles = titles[:-1] # slice off the last comma
	titles = titles + "/n"
	file.write(titles)

	for dob in DOB:
		print("Downloading {0} data for {1}".format(selCategory[1],dob.replace("%2F", "/")))
		for gender in selGender:
			for smokeStatus in selSmokStatus:
				for cib in selCIRider:
					for premiumTerm in premiumTermDcips:
						for sumAssured in SAWLDCIPS:
							formattedPayload = payload.format(selCategory[1], \
								gender, smokeStatus, dob, cib, "", \
								"", premiumTerm, sumAssured)
							r = requests.post(url, headers=headers, data=formattedPayload)
							bs = BeautifulSoup(r.text, 'html.parser')
							xml = bs.find(id="prodStringXML")
							xml = xml.get('value')
							dic = xmltodict.parse(xml, xml_attribs=True)
							try:
								print("reading data ...")
								for i in range(len(dic['ProdList']['Product'])):
									writeString = ""
									for key in dic['ProdList']['Product'][i]:
										if dic['ProdList']['Product'][i][key] != None \
										and dic['ProdList']['Product'][i][key] != 'null':
											writeString += dic['ProdList']['Product'][i][key] + ","
										else:
											writeString += "NA,"
									writeString = writeString[:-1] # slice off the last comma
									writeString += "\n"
									file.write(writeString)
							except Exception as e:
								print(e)
								errorLog.write(str(e))
								errorLog.write("Error for {0}, {1}, {2}, {3}, {4}, {5}, {6}".format( \
									selCategory[1], dob, gender, smokeStatus, cib, premiumTerm, sumAssured))
	file.close()
	errorLog.close()

if __name__ == '__main__':
	global DOB
	global startYear
	# year > 2000 / age < 18 
	# happen to be useless
	# for whole-life
	# year < 1980ish seem to be useless
	global endYear
	startYear = int(sys.argv[1])
	endYear = int(sys.argv[2])
	DOB = ["10%2F10%2F{0}".format(i) for i in range(startYear,endYear)]
	main()