import FinanceDataReader as fdr

#정리된 df 만들기!
def indexdf_made():
    df = fdr.DataReader('KS11','2015')
    df.reset_index(inplace=True)
    df = df[['Date','Close']]
    return df