from pymongo import MongoClient
host='localhost'
#create the connection url
connecturl = "mongodb://localhost:27017/"

# connect to mongodb server
print("Connecting to mongodb server")
connection = MongoClient(connecturl)

# select the 'training' database 

db = connection.training

# select the 'python' collection 

collection = db.python

# create a sample document

doc = [{
  "candidateOTRDetails": {
    "otrIds": 
      {
        "otrId": "124000000004138",
    
        "refId": [
		{
			"applicationType":"SOAP",
			"applicationId":"",
			"oldRefId":"",
			"regYear":"",
			"candidateConfirmation":"",
			"dataSource":"",
			"dataSourceType":"PostgreSQL"
		}
		]
      }
   ,
    "uniqueId": "92cffe6e-4a76-4b98-bd98-ac3d9f2a36ed",
    "candidateAadharDetails": {
      "candidateAadharVaultRefId": "2323224324",
      "candidateRegWithAadharFlag": "Y",
      "candidateAadharMatch10DtlFlag": "Y",
      "candidateEkycFlag": "Y"
    },
    "candidatePersonalDetails": {
      "candidateNameEn": "",
      "candidateNameHi": "",
      "genderId": "1",
      "genderNameEn": "Male",
      "candidateDateOfBirth": "",
      "singleParentId": "1",
      "singleParentNameEn": "No"
    },
    "candidateParentDetails": [
      {
        "familyMemberId": "",
        "familyTypeId": "1",
        "familyTypeNameEn": "Father",
        "familyMemberName": "Anil",
        "familyMemberGenderId": "1",
        "familyMemberGenderNameEn": "Male"
      },
      {
        "familyMemberId": "",
        "familyTypeId": "2",
        "familyTypeNameEn": "Mother",
        "familyMemberName": "Tanu",
        "familyMemberGenderId": "2",
        "familyMemberGenderNameEn": "Female"
      }
    ],
    "candidateMinorityDetails": {
      "minorityCategoryFlag": "Y",
      "minorityCategoryId": "1",
      "minorityCategoryNameEn": "Buddhist"
    },
    "candidateEducationQualification": {
      "qualificationId": "1",
      "qualificationNameEn": "10th Board",
      "boardUniversityId": "34",
      "boardUniversityName": "Central Board of Secondary Education, Delhi",
      "boardUniversityOthName": "",
      "boardUniversityType": "SB",
      "qualificationPassingYear": "2000",
      "qualificationRollNo": "2342414"
    },
    "candidateContactDetails": {
      "candidateMobile": "",
      "candidateEmail": "",
      "mobileAlternate": "",
      "mobileAlternateVerifiedFlag": "",
      "mobileAlternateVerifyDt": "",
      "emailAlternate": "",
      "emailAlternateVerifiedFlag": "",
      "emailAlternateVerifiedDt": ""
    },
	"candidateTermsConditionConsentFlag":"",
	"candidateTermsConditionConsentDt":"",
	"candidateAadhaarConsentFlag":"Y",
	"candidateAadhaarConsentDt":""
  }
}]

# insert a sample document

print("Inserting a document into collection.")
db.collection.insert_one(doc[0])

# query for all documents in 'training' database and 'python' collection

docs = db.collection.find()

print("Printing the documents in the collection.")

for document in docs:
    print(document)

# close the server connecton
print("Closing the connection.")
connection.close()