import pandas as pd


def display_table(table):
    """
    Display the whole panda table

    Args:
        table (pandas.core.frame.DataFrame): The table to display
    """
    print(table)


def extract_column(table, column_name):
    """
    Extract all of the values of a collumn and return the list

    Args:
        table (pandas.core.frame.DataFrame): The csv table to manipulate
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


def extract_column_argumented(table, column_name, second_collumn, second_value):
    """
    Extract all of the values of a collumn filtered by the second collumn value and return the list

    Args:
        table (pandas.core.frame.DataFrame): The csv table to manipulate
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
    """
    A simple function to remove duplicates from a list

    Args:
        entryList (a list): The list with too many duplicate of the same values

    Returns:
        list: The list without any duplicate entries.
    """
    return list(dict.fromkeys(entryList))


# def computeThemeValue():


def cleanCollumn(table, donnees="donneesFusionerDecher", collumnName="TrueWeight"):
    """
    Empty a collumn from the csv. WARNING: Data may be lost in case of a wrong collumn name.

    Args:
        table (pandas.core.frame.DataFrame): The csv table to manipulate
        column_name (string): The collumn name that need to be clean (ex: "TrueWeight").
        donnees (string): the name of the file to save the new data
    """
    table[collumnName] = 0.0
    table.to_csv("data/"+donnees+".csv", index=False)


def computeTrueWeight(table,donnees):
    """
    Will calculate the true weight for every row/criteria of the table then save it in the csv.
    This one version will check every row in the table.

    Args:
        table (pandas.core.frame.DataFrame): The table to manipulate
        donnees (string): the name of the file to save the new data
    """
    cleanCollumn(table, donnees)
    counter = 0
    for i in table["Weight"].tolist():
        currentValue = (1/len(table["Catégories"].unique())) * table["ThemeValue"].tolist()[counter] * i
        table.loc[counter, "TrueWeight"] = currentValue
        counter = counter + 1
    if donnees is not None:
        table.to_csv("data/"+donnees+".csv", index=False)
    return table


def computeTrueWeightFiltered(table, categories, donnees = None):
    """
    Will calculate the true weight for every row/criteria that is in one of the categories of the table then save it in the csv.

    Args:
        table (pandas.core.frame.DataFrame): The table to manipulate
        categories (string list): The categories of the table to manipulate
        donnees (string): the name of the file to save the new data
    """
    cleanCollumn(table,donnees)
    counter = 0
    for i in table["Weight"].tolist():
        for y in categories:
            if table["Catégories"][counter] == y:
                currentValue = 1 / len(categories) * table["ThemeValue"].tolist()[counter] * i
                table.loc[counter, "TrueWeight"] = currentValue
        counter = counter + 1
    if donnees is not None:
        table.to_csv("data/"+donnees+".csv", index=False)
    return table



if __name__ == '__main__':
    table = pd.read_csv('../data/donneesFusionerDecher.csv')
    # display_table(table)
    # print(extract_column(table, "Thèmes", "donneesFusionerDecher"))
    # print(removeDuplicate(extract_column_argumented(table,"Thèmes","Catégories","Acceptabilité technique")))
    computeTrueWeight(table, "donneesFusionerDecher")

    # focaliser = ["Environnement naturel", "Économie"]
    # computeTrueWeightFiltered(table, focaliser, "donneesFusionerDecher")
    countty = 0
    for y in table["TrueWeight"].tolist():
        countty = countty + y
    print("total true weight= ", countty)
    print(table["TrueWeight"].tolist())
