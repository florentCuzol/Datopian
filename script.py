import pandas as pd

xls = pd.ExcelFile("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls")
raw = pd.read_excel(xls,sheet_name="Data 1",header=2)
data = raw

data['Date'] = pd.to_datetime(data['Date'])

daily = data
daily.columns = ["Date","Price"]
daily.to_csv("daily_data.csv",index=False)

monthly = data.groupby([data.Date.dt.year, data.Date.dt.month]).first("Henry Hub Natural Gas Spot Price (Dollars per Million Btu)")
monthly["Price"] = round(monthly["Price"],2)
monthly.index.names = ["Year","Month"]
monthly = monthly.reset_index()
monthly["Year"] = monthly["Year"].map(str)
monthly["Month"] = monthly["Month"].map(str)

monthly["Date"] = monthly["Year"] + "-" + monthly["Month"]
monthly = monthly[["Date","Price"]]

monthly.to_csv("monthly_data.csv",index=False)

yearly = data.groupby([data.Date.dt.year]).first("Price")
yearly["Price"] = round(yearly["Price"],2)

yearly.to_csv("yearly_data.csv",index=False)
