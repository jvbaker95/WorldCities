import json

'''Used as a class wrapper for the geolocations'''
class Polygon:
    def __init__(self,properties,coordinates,id):
        self.type = "Polygon"
        self.properties = properties
        self.coordinates = coordinates[0]
        self.id = id
        self.zone = None

        keyWords = ["core", "exterior"]
        tempList = []
        tempList = self.getLabel().split("_")
        cityString = ""
        for item in tempList:
            if item in keyWords:
                self.zone = item
            if item not in keyWords and len(item) != 2:
                cityString += "%s " % (item)
        cityString.strip()
        self.city = cityString.strip()

    def __repr__(self):
        returnString = "POLYGON ID: %s\n" % (self.id)
        returnString += "Area (KM): %s\n" % (self.getAreaKM())
        returnString += "Label: %s\n" % (self.getLabel())
        returnString += "Zone: %s\n" % (self.zone)
        returnString += "Location: %s, %s, %s" % (self.getIsIn(), self.getCountry(), self.getState())

        return returnString
    def getAreaKM(self):
        try:
            return self.properties['area_km']
        except KeyError:
            return "No Information"
    def getLabel(self):
        return self.properties['label']
    def getIsIn(self):
        return self.properties['is_in']
    def getCountry(self):
        return self.properties['country']
    def getState(self):
        try:
            return self.properties['state']
        except KeyError:
            return "Non-US"


'''Import the included json file, and use the json class 
to parse it into a dictionary.'''
jsonFile = open("Worldcities.json", mode="r")
lines = (jsonFile.read())
parsedJson = json.loads(lines)

polygonList = []

'''Convert the following 2d dictionary into a Polygon object, which will 
store the data into a class object for easy access/readability, and then
store that object into a polygon list.'''
for item in parsedJson['features']:
    newPolygon = Polygon(item['properties'],item['geometry']['coordinates'],item['id'])
    polygonList.append(newPolygon)

citySet = []


'''Print everything in the polygon list.'''
for polygon in polygonList:
    if (polygon.zone == "core"):
        citySet.append("%s, %s" % (polygon.city, polygon.zone))
        print(polygon)
        print(polygon.coordinates)
        print(len(polygon.coordinates))
        print("\n")

citySet = set(citySet)
citySet = list(citySet)
citySet.sort()

print("There are %d cities with the 'CORE' attribute in the json file." % (len(citySet)))

for city in citySet:
    print(city)

