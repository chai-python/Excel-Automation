import pandas as pd
from pathlib import Path
data_dir = Path("data")
excel_files = [
    file for file in data_dir.glob("*.xlsx")
    if not file.name.startswith("~$")
]
if not excel_files:
    print("Excelファイルが見つかりません。")
    raise SystemExit(1)
required_columns = ["商品名", "数量", "単価"]
dataframes = []
for file in excel_files:
    try:
        df = pd.read_excel(file)
    except Exception as e:
        print("Excelファイルの読み込みに失敗しました。")
        print("ファイル名：", file.name)
        print(e)
        raise SystemExit(1)
    actual_columns=df.columns
    missing_columns=[]
    for column in required_columns:
        if column not in actual_columns:
            missing_columns.append(column)
    if missing_columns:
        print("ファイル名：", file.name)
        print("必須列が不足しています。")
        for column in missing_columns:
            print("不足している列: ", column)
        raise SystemExit(1)
    else:
        print("必須列はすべて揃っています。")
    df["元ファイル名"]=file.name
    dataframes.append(df)
df = pd.concat(dataframes, ignore_index=True)
quantity_numeric = pd.to_numeric(df["数量"], errors="coerce")
price_numeric = pd.to_numeric(df["単価"], errors="coerce")

#異常判断
quantity_invalid=(df["数量"].notna()) & (quantity_numeric.isna())
price_invalid=(df["単価"].notna()) & (price_numeric.isna())
quantity_missing=df["数量"].isna()
price_missing=df["単価"].isna()
product_missing=df["商品名"].isna()

quantity_out_of_range=quantity_numeric==0
price_out_of_range=price_numeric<=0


abnormal_mask=(
    quantity_invalid 
    | price_invalid 
    | quantity_missing 
    | price_missing 
    | product_missing
    | quantity_out_of_range
    | price_out_of_range
)

missing_values = df.isnull().sum()
total_missing=missing_values.sum()

return_mask=(quantity_numeric<0) & (~abnormal_mask)

df["売上金額"] = quantity_numeric * price_numeric
df["異常理由"] = ""
df.loc[quantity_missing,"異常理由"] += "数量の欠損;"
df.loc[price_missing,"異常理由"] += "単価の欠損;"
df.loc[product_missing,"異常理由"] += "商品名の欠損;"
df.loc[quantity_invalid,"異常理由"] += "数量が数値ではない;"
df.loc[price_invalid,"異常理由"] += "単価が数値ではない;"
df.loc[quantity_out_of_range,"異常理由"] += "数量が0;"
df.loc[price_out_of_range,"異常理由"] += "単価が0以下;"

df["異常理由"]=df["異常理由"].str.rstrip(";")



abnormal_data=df[abnormal_mask]
normal_data = df[~abnormal_mask & ~return_mask]
return_data=df[return_mask]
if abnormal_data.empty:
    print("異常データはありません。")
else:
    print("異常データが見つかりました。")
    print(abnormal_data)

if return_data.empty:
    print("返品候補データはありません。")
else:
    print("返品候補データが見つかりました。")
    print(return_data)

if total_missing == 0:
    print("==== 欠損値チェック ====")
    print("欠損値はありません。")
else :
    print("==== 欠損値チェック ====")
    print("欠損値が見つかりました。")
    for missing, values in missing_values.items():
        if values>0:
            print(f"{missing}: {values}件")

total_sales=normal_data["売上金額"].sum()
print("==== 商品別売上集計 ====")
sales_by_product = normal_data.groupby("商品名")["売上金額"].sum()
for product, sales in sales_by_product.items():
    print(f"{product}: {sales:,}円")
print("==== 総売上金額 ====")
print(f"{total_sales:,}円")