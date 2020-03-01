import pandas as pd
import os

class AnomalyDetector:      

    # Rule 1: One point is more than 3 standard deviations from the mean (outlier)
    def rule1(self, data, mean, sigma):

        def isBetween(value, lower, upper):
            isBetween = value < upper and value > lower
            return 0 if isBetween else 0

        upperLimit = mean + 3 * sigma
        lowerLimit = mean - 3 * sigma

        data['Rule1'] = data.apply(lambda row: isBetween(row['amount'], lowerLimit, upperLimit), axis = 1)

    # Rule 2: Nine (or more) points in a row are on the same side of the mean (shift)
    def rule2(self, data, mean):
        values = [0]*len(data)

        # +1 means upside, -1 means downside
        upsideOrDownside = 0
        count = 0
        for i in range(len(data)):
            amount = data.iloc[i]['amount']
            if amount > mean:
                if upsideOrDownside == 1:
                    count += 1
                else: 
                    upsideOrDownside = 1
                    count = 1
            elif amount < mean: 
                if upsideOrDownside == -1:
                    count += 1
                else: 
                    upsideOrDownside = -1
                    count = 1

            if count >= 9:
                values[i] = 1

        data['Rule2'] = values              

    # Rule 3: Six (or more) points in a row are continually increasing (or decreasing) (trend)
    def rule3(self, data):
        values = [0]*len(data)

        previousAmount = data.iloc[0]['amount']
        # +1 means increasing, -1 means decreasing
        increasingOrDecreasing = 0
        count = 0
        for i in range(1, len(data)):
            amount = data.iloc[i]['amount']
            if amount > previousAmount:
                if increasingOrDecreasing == 1:
                    count += 1
                else:
                    increasingOrDecreasing = 1
                    count = 1
            elif amount < previousAmount:
                if increasingOrDecreasing == -1:
                    count += 1
                else:
                    increasingOrDecreasing = -1
                    count = 1

            if count >= 6:
                values[i] = 1

            previousAmount = amount

        data['Rule3'] = values 

    # Rule 4: Fourteen (or more) points in a row alternate in direction, increasing then decreasing (bimodal, 2 or more factors in data set)
    def rule4(self, data):
        values = [0]*len(data)

        previousAmount = data.iloc[0]['amount']
        # +1 means increasing, -1 means decreasing
        bimodal = 0
        count = 1
        for i in range(1, len(data)):
            amount = data.iloc[i]['amount']
            
            if amount > previousAmount:
                bimodal += 1
                if abs(bimodal) != 1:
                    count = 0
                    bimodal = 0
                else:
                    count += 1
            elif amount < previousAmount:
                bimodal -= 1
                if abs(bimodal) != 1:
                    count = 0
                    bimodal = 0
                else:
                    count += 1

            previousAmount = amount

            if count >= 14:
                values[i] = 1

        data['Rule4'] = values 

    # Rule 5: Two (or three) out of three points in a row are more than 2 standard deviations from the mean in the same direction (shift)
    def rule5(self, data, mean, sigma):
        if len(data) < 3: return

        values = [0]*len(data)
        upperLimit = mean - 2 * sigma
        lowerLimit = mean + 2 * sigma        

        for i in range(len(data) - 3):
            first = data.iloc[i]['amount']
            second = data.iloc[i+1]['amount']
            third = data.iloc[i+2]['amount']
            
            setValue = False
            validCount = 0
            if first > mean and second > mean and third > mean:
                validCount += 1 if first > lowerLimit else 0
                validCount += 1 if second > lowerLimit else 0
                validCount += 1 if third > lowerLimit else 0
                setValue = validCount >= 2
            elif first < mean and second < mean and third < mean:
                validCount += 1 if first < upperLimit else 0
                validCount += 1 if second < upperLimit else 0
                validCount += 1 if third < upperLimit else 0
                setValue = validCount >= 2

            if setValue:
                values[i+2] = 1

        data['Rule5'] = values

    # Rule 6: Four (or five) out of five points in a row are more than 1 standard deviation from the mean in the same direction (shift or trend)
    def rule6(self, data, mean, sigma):
        if len(data) < 5: return

        values = [0]*len(data)
        upperLimit = mean - sigma
        lowerLimit = mean + sigma   

        for i in range(len(data) - 5):
            pVals = list(map(lambda x: data.iloc[x]['amount'], range(i, i+5)))

            setValue = False
            if len(list(filter(lambda x: x > mean, pVals))) == 5:
                setValue = len(list(filter(lambda x: x > lowerLimit, pVals))) >= 4
            elif len(list(filter(lambda x: x < mean, pVals))) == 5:
                setValue = len(list(filter(lambda x: x < upperLimit, pVals))) >= 4

            if setValue:
                values[i+4] = 1

        data['Rule6'] = values

    # Rule 7: Fifteen points in a row are all within 1 standard deviation of the mean on either side of the mean (reduced variation or measurement issue)
    def rule7(self, data, mean, sigma):
        if len(data) < 15: return
        values = [0]*len(data)
        upperLimit = mean + sigma
        lowerLimit = mean - sigma 
        
        for i in range(len(data) - 15):
            setValue = True
            for y in range(15):
                item = data.iloc[i + y]['amount']
                if item >= upperLimit or item <= lowerLimit: 
                    setValue = False
                    break
            
            if setValue:
                values[i+14] = 1

        data['Rule7'] = values

    # Rule 8: Eight points in a row exist with none within 1 standard deviation of the mean and the points are in both directions from the mean (bimodal, 2 or more factors in data set)
    def rule8(self, data, mean, sigma):
        if len(data) < 8: return
        values = [0]*len(data)

        for i in range(len(data) - 8):
            setValue = True
            for y in range(8):
                item = data.iloc[i + y]['amount']
                if abs(mean - item) < sigma:
                    setValue = False
                    break

            if setValue:
                values[i+8] = 1

        data['Rule8'] = values

def loadData():
    dirname = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.join(dirname, 'dataset.xlsx')
    df = pd.read_excel(root_path)
    return df

def saveResult(data):
    filename = 'results.csv'
    dirname = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dirname, filename)
    data.to_csv(path)
    print('Results are saved at \'%s\' as \'%s\'\n' % (dirname,filename))

if __name__ == '__main__':
    
    df = loadData()
    print('\nSample data loaded.')
    
    df = df.drop('day', axis = 1)

    trainIndexLimit = 52 * 7
    trainSet = df[:trainIndexLimit]
    testSet = df[trainIndexLimit:]
    
    mean = trainSet['amount'].mean()
    sigma = trainSet['amount'].std()
    print('Mean(𝑥̅): %d' % mean)
    print('Std(𝜎): %d' % sigma)

    weeklyData = testSet.groupby('week').mean()
    detector = AnomalyDetector()
    
    print('Applying all rules...⏳')
    detector.rule1(weeklyData, mean, sigma)
    detector.rule2(weeklyData, mean)
    detector.rule3(weeklyData)
    detector.rule4(weeklyData)
    detector.rule5(weeklyData, mean, sigma)
    detector.rule6(weeklyData, mean, sigma)
    detector.rule7(weeklyData, mean, sigma)
    detector.rule8(weeklyData, mean, sigma)
    
    resultDf = weeklyData.drop('amount', axis = 1)

    print('Completed ✅')
    saveResult(resultDf)   