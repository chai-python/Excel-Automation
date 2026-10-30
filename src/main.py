import pandas as pd
from pathlib import Path
data_dir = Path("data")
excel_files = [
    file for file in data_dir.glob("*.xlsx")
    if not file.name.startswith("~$")
]
if not excel_files:
    print("Excelファイルが見つかりません。")
    raise SystemExit
required_columns = ["商品名", "数量", "単価"]
dataframes = []
for file in excel_files:
    df = pd.read_excel(file)
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
        raise SystemExit
    else:
        print("必須列はすべて揃っています。")
    dataframes.append(df)
df = pd.concat(dataframes, ignore_index=True)
df["売上金額"] = df["数量"] * df["単価"]
abnormal_data = df[(df["数量"]<=0) | (df["単価"]<=0)]
normal_data = df[(df["数量"]>0) & (df["単価"]>0)]
if abnormal_data.empty:
    print("異常データはありません。")
else:
    print("異常データが見つかりました。")
    print(abnormal_data)

missing_values = df.isnull().sum()
total_missing=missing_values.sum()
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
