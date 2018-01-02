import requests
from bs4 import BeautifulSoup
import xmltodict
import sys
import collections

url = 'http://comparefirst.sg/wap/searchProductsEvent.action'

headers = {}
headers['content-type'] = 'application/x-www-form-urlencoded'
headers['origin'] = 'http://comparefirst.sg'
headers['Referer'] = 'http://comparefirst.sg/wap/homeEvent.action'

# ----------------- This setting is for 'Term Life Products' -----------------
payload = "productGroup=invst&searchproduct=&prodGroup=term&pageAction=search" \
+ "&breadCrumb=null&viewProdsId=null" \
+ "&ProdsCompIDs=null&ProdsVisibleIDs=null&subCatSeleJson=null&subCatCountJson=null" \
+ "&sortOrderSelected=null&reportProdsCompIDs=null&searchResInitCount=10" \
+ "&searchResIncCount=5&gaSearchSummary=null&prodStringXML=&prodSummaryTxt=" \
+ "&premiumTypeDCIPs=Annual" \
+ "&coverageTermTLDCIPs=select&coverageTermTLNonDCIP=select" \
+ "&coverageTermEndow=select&premiumTermAll=select" \
+ "&premiumTermDcips=select&premiumTermNonDcips=select&PremAnnualGroup=select" \
+ "&PremSingleGroup=select&SAWLAll=select&SATLDCIPS=select&SAWLDCIPS=select" \
+ "&SATLNonDCIPS=select&SAWLNonDCIPS=select&sortNonWLGroup=1&sortWLGroup=select&sortEndoGroup=select" \
+ "&selCategory=all" \
+ "&dob={0}" \
+ "&selGender={1}" \
+ "&selSmokStatus={2}" \
+ "&selCIRider={3}" \
+ "&premiumTypeOther={4}" \
+ "&coverageTermTLAllList={5}" \
+ "&SATLAll={6}"

# Gender : M, F
selGender = ["M", "F"]
# Smoke Status : Y, N
selSmokStatus = ["Y", "N"]
# Date of Birth : dd%2Fmm%2Fyyyy
# dob = ["10%2F10%2F{0}".format(i) for i in range(1970,2018)]
# Critical Illness Benefits : Y, N
selCIRider = ["Y", "N"]
# Premium Type : Annual, Single
premiumTypeOther = ["Annual", "Single"]
# Coverage Term : 1 to 5, 6 to 10, 11 to 15, .... 36 to 40, above 40
coverageTermTLAllList = ["{0}+to+{1}".format(i,i+4) for i in range(1,41,5)]
coverageTermTLAllList.append("Above+40")
# Sum Assured
SATLAll = [50000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000] 
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
	file = open("termLifeProducts.csv", 'w')

	# create titles for the csv
	titles = ""
	titles += "DOB, Gender, Smoke Status, Critical Illness Benefits, Premium Type, Coverage Term, Sum Assured,"
	for i in range(len(keys)):
		titles = titles + keys[i] + ","
	titles = titles[:-1] # slice off the last comma
	titles = titles + "\n"
	file.write(titles)
	
	for dob in DOB:
		formattedDOB = dob.replace("%2F", "/")
		print("Downloading data for date: {0}".format(formattedDOB))
		for gender in selGender:
			for smokeStatus in selSmokStatus:
				for cib in selCIRider:
					for premiumType in premiumTypeOther:
						for coverageTerm in coverageTermTLAllList:
							for sumAssured in SATLAll:
								formattedPayload = payload.format( \
									dob, gender, smokeStatus, cib, premiumType, coverageTerm, sumAssured)
								r = requests.post(url, headers=headers, data=formattedPayload)
								bs = BeautifulSoup(r.text, 'html.parser')
								xml = bs.find(id="prodStringXML")
								xml = xml.get('value')
								dic = xmltodict.parse(xml, xml_attribs=True)
								
								print("reading data ...")
								try:
									# THIS HANDLES THE CASE WHEN THERE IS ONLY 1 PRODUCT
									if type(dic['ProdList']['Product']) == type(collections.OrderedDict()):
										writeString = "{0}, {1}, {2}, {3}, {4}, {5}, {6},".format( \
											formattedDOB, gender, smokeStatus, cib, premiumType, coverageTerm, sumAssured)
										for j in range(len(keys)):
											if dic['ProdList']['Product'][keys[j]] != None \
												and dic['ProdList']['Product'][keys[j]] != 'null':
												writeString += dic['ProdList']['Product'][keys[j]].replace(",", "")
											else:
												writeString += "NA"
											writeString += ","
										writeString = writeString[:-1]
										writeString += "\n"
										file.write(writeString)
									else:
										for i in range(len(dic['ProdList']['Product'])):
											writeString = "{0}, {1}, {2}, {3}, {4}, {5}, {6},".format( \
												formattedDOB, gender, smokeStatus, cib, premiumType, coverageTerm, sumAssured)
											for j in range(len(keys)):
												if dic['ProdList']['Product'][i][keys[j]] != None \
													and dic['ProdList']['Product'][i][keys[j]] != 'null':
													# !!! need to remove COMMA in the retrieved data !!!
													writeString += dic['ProdList']['Product'][i][keys[j]].replace(",", "")
												else:
													writeString += "NA"
												writeString += ","
											writeString = writeString[:-1] # slice off the last comma
											writeString += "\n"
											file.write(writeString)
								except Exception as e:
									error = "Error for {0}, {1}, {2}, {3}, {4}, {5}, {6}: {7}\n".format( \
										formattedDOB, gender, smokeStatus, cib, premiumType, coverageTerm, sumAssured, str(e))
									print(error, end="")
									errorLog.write(error)
									
	file.close()
	errorLog.close()

if __name__ == '__main__':
	global DOB
	global startYear
	# year > 2000 / age < 18 
	# happen to be useless
	global endYear
	startYear = int(sys.argv[1])
	endYear = int(sys.argv[2])
	DOB = ["10%2F10%2F{0}".format(i) for i in range(startYear,endYear)]
	main()