import pandas as pd
import matplotlib.pyplot as plt

# task1
df = pd.read_csv('sales_data.csv')

plt.figure(figsize=(8, 5))
plt.plot(df['month_number'], df['total_profit'], linestyle='-', linewidth=2)
plt.xlabel('Номер месяца')
plt.ylabel('Общая прибыль')
plt.title('Общая прибыль по месяцам')
plt.grid(True)
plt.show()


# task2
plt.figure(figsize=(8, 5))
plt.plot(
    df['month_number'],
    df['total_units'],
    linestyle='--',
    color='red',
    marker='o',
    linewidth=3,
    label='Продажи'
)
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Продажи по месяцам')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()


# task3
products = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']

plt.figure(figsize=(10, 6))
for product in products:
    plt.plot(df['month_number'], df[product], label=product)
plt.xlabel('Номер месяца')
plt.ylabel('Продажи')
plt.title('Продажи по продуктам')
plt.legend()
plt.grid(True)
plt.show()

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
products = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']

for i, product in enumerate(products):
    row = i // 3
    col = i % 3
    axes[row, col].plot(df['month_number'], df[product])
    axes[row, col].set_title(product)
    axes[row, col].grid(True)

plt.tight_layout()
plt.show()


# task4
plt.figure(figsize=(8, 5))
plt.scatter(df['month_number'], df['toothpaste'], color='blue')
plt.xlabel('Номер месяца')
plt.ylabel('Продажи зубной пасты')
plt.title('Продажи зубной пасты по месяцам')
plt.grid(True, linestyle='--')
plt.show()


# task5
import numpy as np

months = df['month_number']
bar_width = 0.35
x = np.arange(len(months))

plt.figure(figsize=(10, 6))
plt.bar(x - bar_width/2, df['facecream'], width=bar_width, label='Крем для лица')
plt.bar(x + bar_width/2, df['facewash'], width=bar_width, label='Пенка для умывания')
plt.xlabel('Номер месяца')
plt.ylabel('Продажи')
plt.title('Сравнение продаж')
plt.xticks(x, months)
plt.legend()
plt.show()


# task6
total_sales = df[products].sum()
plt.figure(figsize=(8, 8))
plt.pie(
    total_sales,
    labels=total_sales.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Доля продаж по продуктам за год')
plt.show()


# task7
plt.figure(figsize=(10, 6))
plt.stackplot(
    df['month_number'],
    df['facecream'],
    df['facewash'],
    df['toothpaste'],
    labels=['Крем', 'Пенка', 'Зубная паста']
)
plt.xlabel('Номер месяца')
plt.ylabel('Продажи')
plt.legend(loc='upper left')
plt.title('Накопленные продажи')
plt.show()


#task8
fig = plt.figure(figsize=(12, 12))

# Пример расположения:
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
ax2 = plt.subplot2grid((3, 3), (0, 2))
ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=3)
ax4 = plt.subplot2grid((3, 3), (2, 0))
ax5 = plt.subplot2grid((3, 3), (2, 1))
ax6 = plt.subplot2grid((3, 3), (2, 2))

plt.tight_layout()
plt.show()
