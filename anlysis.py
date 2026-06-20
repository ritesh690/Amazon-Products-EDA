import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("amazon.csv")

print(df.head())
print("\nColumns:")
print(df.columns)
print("\nShape:")
print(df.shape)

print(df.isnull().sum())
print(df.duplicated().sum())


# Remove rows with missing rating_count
df = df.dropna(subset=['rating_count'])

print("New Shape:", df.shape)

print(df[['discounted_price','actual_price','discount_percentage']].head())


# Convert prices to numeric
df['discounted_price'] = df['discounted_price'].str.replace('₹','', regex=False).str.replace(',','', regex=False).astype(float)

df['actual_price'] = df['actual_price'].str.replace('₹','', regex=False).str.replace(',','', regex=False).astype(float)

# Convert discount percentage
df['discount_percentage'] = df['discount_percentage'].str.replace('%','', regex=False).astype(float)

print(df[['discounted_price','actual_price','discount_percentage']].head())

top_discount = df[['product_name','discount_percentage']].sort_values(
    by='discount_percentage',
    ascending=False
)

print(top_discount.head(10))

#Top 10 Product Categories on Amazon
top_categories = df['category'].value_counts().head(10)

plt.figure(figsize=(20,10))
top_categories.plot(kind='bar')

plt.title("Top 10 Product Categories on Amazon")
plt.xlabel("Category")
plt.ylabel("Number of Products")

plt.tight_layout()
plt.savefig("top_categories.png")
plt.show()

#Top 10 Highest Rated Products
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

top_rated = df[['product_name','rating']].sort_values(
    by='rating',
    ascending=False
)

print(top_rated.head(10))

#Top 10 Most Reviewed Products
df['rating_count'] = df['rating_count'].astype(str)
df['rating_count'] = df['rating_count'].str.replace(',', '', regex=False)
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

most_reviewed = df[['product_name','rating_count']].sort_values(
    by='rating_count',
    ascending=False
)

print(most_reviewed.head(10))

#Category-wise Average Rating
category_rating = df.groupby('category')['rating'].mean()

print(category_rating.sort_values(ascending=False).head(10))


#second graph
top_reviewed = most_reviewed.head(10)

plt.figure(figsize=(10,5))
plt.barh(top_reviewed['product_name'], top_reviewed['rating_count'])

plt.title("Top 10 Most Reviewed Products")
plt.xlabel("Number of Reviews")

plt.tight_layout()
plt.savefig("top_reviewed.png")
plt.show()

#Discount Analysis Graph
top_discount = df[['product_name','discount_percentage']].sort_values(
    by='discount_percentage',
    ascending=False
).head(10)

plt.figure(figsize=(15,8))
plt.barh(top_discount['product_name'], top_discount['discount_percentage'])

plt.title("Top 10 Highest Discounted Products")
plt.xlabel("Discount Percentage")

plt.tight_layout()
plt.savefig("top_discount.png")
plt.show()


#insights
print("Average Rating:", df['rating'].mean())

print("Average Discount:", df['discount_percentage'].mean())

print("Highest Discount:")
print(df.loc[df['discount_percentage'].idxmax(), 'product_name'])