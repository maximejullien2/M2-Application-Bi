import pandas as pd

table = pd.read_csv('data/donneesFusioner.csv')


# print(table['Poid'])


def display_table():
    print(table)


def extract_column(column_name=None):
    """
    Extract all of the values of a collumn and return the list

    Args:
        column_name (string): The collumn name (ex: "C1").

    Returns:
        list: The collumn.
    """
    if column_name:
        if column_name in table.columns:
            return table[column_name].tolist()
        else:
            print("Collumn " + column_name + "not found")
            return None


def extract_column_argumented(column_name, second_collumn, second_value):
    """
    Extract all of the values of a collumn filtered by the second collumn value and return the list

    Args:
        column_name (string): The collumn name (ex: "C1").
        second_collumn (string): The second collumn name (ex: "Catégories").
        second_value (string): The collumn value we want to be the same (ex: "Acceptabilité technique").
    Returns:
        list: The filtered collumn.
    """
    if column_name:
        if column_name in table.columns and second_collumn in table.columns:
            localResult = []
            count = 0
            for i in table[second_collumn].tolist():
                if i == second_value:
                    localResult.append(table[column_name].tolist()[count])
                count = count + 1
            return localResult
        else:
            print("Collumn not found")
            return None


def removeDuplicate(entryList):
    return list(dict.fromkeys(entryList))


# def computeThemeValue():


def computeTrueWeight():
    counter = 0
    for i in table["Weight"].tolist():
        currentValue = 0.25 * table["ThemeValue"].tolist()[counter] * i #le truc a améliorer dans le futur
        table.loc[counter, "TrueWeight"] = currentValue
        counter = counter + 1
    table.to_csv("data/donneesFusioner.csv", index=False)

if __name__ == '__main__':
    # display_table()
    # print (extract_column_argumented("Thèmes", "Acceptabilité technique"))
    # print(extract_column("Thèmes"))
    # print(removeDuplicate(extract_column_argumented("Thèmes","Catégories","Acceptabilité technique")))
    computeTrueWeight()
    countty=0
    for y in table["TrueWeight"].tolist():
        print(y)
        countty=countty+y
    print(countty)
    print(table["TrueWeight"].tolist())
