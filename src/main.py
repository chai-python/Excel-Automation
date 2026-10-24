import pandas as pd
df = pd.read_excel("data/sales_data.xlsx")
df["売上金額"] = df["数量"] * df["単価"]
print(df)
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

total_sales=df["売上金額"].sum()
print("==== 商品別売上集計 ====")
sales_by_product=df.groupby("商品名")["売上金額"].sum()
for product, sales in sales_by_product.items():
    print(f"{product}: {sales:,}円")
print("==== 総売上金額 ====")
print(f"{total_sales:,}円")
