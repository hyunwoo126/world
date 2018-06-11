import csv



class Nation:
    def __init__(self, name, staticData):
        self.name = name
        self.data = {}
        for prop in staticData:
            self.data[prop] = staticData[prop]

    def addYearData(self, year, yearData):
        self.data[year] = yearData

    def getGDP(self, year, perCap = False):
        data = self.data
        if year not in data or 'gdp_percap' not in data[year] or 'population' not in data[year]:
            return False
        else:
            data = data[year]
            try:
                return round(float(data['gdp_percap']) * float(data['population'] if not perCap else 1))
            except ValueError:
                return False

class World:
    def __init__(self):
        self.totalNations = 0
        self.earliestYear = False
        self.latestYear = False
        self.allProps = ['iso2c','iso3c','country','year','gdp_percap','life_expect','population','birth_rate','neonat_mortal_rate','region','income']
        self.staticProps = ['iso2c','iso3c','region']
        self.yearlyProps =  ['gdp_percap', 'life_expect', 'population', 'birth_rate','neonat_mortal_rate', 'income']
        self.filePath = './data/datavis/nations.csv'
        self.nations = self.processCSV()

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
        with open(self.filePath, newline='') as csvfile:
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

    def allTheNations(self):
        for nation in self.nations:
            print(self.nations[nation].name)

    def worldPop(self, year):
        pop = 0
        nations = self.nations
        for nation in nations.values():
            if year in nation.data and nation.data[year]['population']:
                pop += round(float(nation.data[year]['population']))
        return pop

    def showAllGDP(self, year, perCap = False):
        def fnRanking(nation):
            GDP = self.nations[nation].getGDP(year, perCap)
            if GDP:
                return GDP
            else:
                return 0
        ranked = sorted(self.nations, key=fnRanking, reverse=True)
        rank = 1
        for nation in ranked:
            nationInst = self.nations[nation]
            GDP = nationInst.getGDP(year, perCap)
            if not GDP:
                text = '----'
            else:
                text = str(GDP)
            print(str(rank).ljust(4), nationInst.name.ljust(34), text)
            rank += 1