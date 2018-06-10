import csv

class Nation:
    def __init__(self, name, staticData):
        self.name = name
        self.data = {}
        for prop in staticData:
            self.data[prop] = staticData[prop]

    def addYearData(self, year, yearData):
        self.data[year] = yearData

class World:
    def __init__(self):
        self.totalNations = 0
        self.earliestYear = False
        self.latestYear = False
        self.allProps = ['iso2c','iso3c','country','year','gdp_percap','life_expect','population','birth_rate','neonat_mortal_rate','region','income']
        self.staticProps = ['iso2c','iso3c','region']
        self.yearlyProps =  ['gdp_percap', 'life_expect', 'population', 'birth_rate','neonat_mortal_rate', 'income']
        self.data = self.processCSV()

        print('total nation count: '+str(self.totalNations))
        print('earliest year: '+str(self.earliestYear))
        print('latest year: '+str(self.latestYear))

    def processCSV(self):
        output = {}
        def getSubData(data, yearly = False):
            if yearly:
                props = self.yearlyProps
            else:
                props = self.staticProps
            
            outputData = {}
            for prop in props:
                outputData[prop] = data[prop]
            
            return outputData

        print('csv process initalized...')
        with open('./data/nations.csv', newline='') as csvfile:
            nations = csv.reader(csvfile)
            props = []
            for row in nations:
                if len(props) < 1:
                    props = row
                else:
                    nationData = {}
                    for i in range(len(props)):
                        nationData[props[i]] = row[i]
                    
                    country = nationData['country']
                    year = nationData['year']
                    if not self.earliestYear or int(year) < self.earliestYear:
                        self.earliestYear = int(year)
                   
                    if not self.latestYear or int(year) > self.latestYear:
                        self.latestYear = int(year)

                    if country not in output:
                        self.totalNations += 1
                        output[country] = Nation(country, getSubData(nationData, False))
                    output[country].addYearData(year, getSubData(nationData, True))
        print('csv process finished.')
        
        return output

    def showAllNations(self):
        for nation in self.data:
            print(self.data[nation].name)

    # def showAllGDP(self, year):