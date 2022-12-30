import json

brand = 'Fiat'          #Change these variables when adding other brands and models to json file
brand_int_value = 22    #These values are visible in https://www.nettiauto.com/ inspector mode
                        #Also remember change rawdata.txt


tempDictionary = {brand: {'brand_int': brand_int_value}}


#This function separates the values ​​corresponding to the brand and the model, which are needed when searching Nettiauto's Rest api.
#Raw data must be manually copied from https://www.nettiauto.com/ inspector mode before running that function.
def separate_brand_and_model():
    with open('rawdata.txt') as r:
        lines = r.readlines()

    for row in lines:
        value = row.rsplit('"')[1]
        if value == "Malli" or value =="":
            continue
        model = row.rsplit(">")[1].rsplit("<")[0]
        tempDictionary[brand][model] = int(value)


#Run this function first. That creates json file at the begining.
def create_dictionary():
    separate_brand_and_model()

    json_object = json.dumps(tempDictionary, indent=4)

    file = open("BRANDS_AND_MODELS.json", "w")

    file.write(json_object)

    file.close()

#Run this function when "BRANDS_AND_MODELS.json" file already exist and wanted to add items to dictionary
def append_to_dictionary():

    #first creating new tempDictionary
    separate_brand_and_model()

    #Then compine old and new dictionary and save that in json file
    with open("BRANDS_AND_MODELS.json", 'r+') as file:
        file_existing_data = json.load(file)
        compined_dictionary = file_existing_data | tempDictionary
        file.seek(0)
        json.dump(compined_dictionary, file, indent=4)
    


def main():
    #create_dictionary()
    append_to_dictionary()

if __name__ == "__main__":
    main()
