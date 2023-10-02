import pandas as pd

class Manipulator:
    def __init__(self, dataframe, q1=0.25, q3=0.75):
        #first and third quartiles as given thresholds
        # recommended that enter different thresholds for different datas
        self.dataframe = dataframe
        self.q1 = q1
        self.q3 = q3

    def outlier_thresholds(self, col_name):
        #getting limits
        quartile1 = self.dataframe[col_name].quantile(self.q1)
        quartile3 = self.dataframe[col_name].quantile(self.q3)
        interquantile_range = quartile3 - quartile1
        up_limit = quartile3 + 1.5 * interquantile_range
        low_limit = quartile1 - 1.5 * interquantile_range
        return low_limit, up_limit

    def grab_outliers(self, col_name, index=False):
        #showing outliers
        low, up = self.outlier_thresholds(col_name)

        outliers = self.dataframe[((self.dataframe[col_name] < low) | (self.dataframe[col_name] > up))]

        if outliers.shape[0] > 10:
            print(outliers.head())
        else:
            print(outliers)

        if index:
            outlier_index = outliers.index
            return outlier_index
    
    def remove_outliers(self, col_name):
        #deleting outlier columns 
        low_limit, up_limit = self.outlier_thresholds(col_name)
        df_without_outliers = self.dataframe[~((self.dataframe[col_name] < low_limit) | (self.dataframe[col_name] > up_limit))]
        return df_without_outliers
    
    def replace_with_thresholds(self, col_name):
        #replacing outliers with thresholds
        low_limit, up_limit = self.outlier_thresholds(col_name)
        self.dataframe.loc[(self.dataframe[col_name] < low_limit), col_name] = low_limit
        self.dataframe.loc[(self.dataframe[col_name] > up_limit), col_name] = up_limit
    
    def striptist(self):
        #purpose: deleting unwamted spaces at the beginning of the string in the data frame
        df=self.dataframe
        for i in df:
            if df[i].dtype=='object':
                df[i]=df[i].str.strip()
        return df