import matplotlib.pyplot as plt

# Twoje dane
ILOSCFIRM = [21, 20, 23, 18, 19, 22, 17, 24, 25, 16, 26, 15, 14, 27, 28, 13, 40, 29, 1, 12, 11, 30, 31, 10, 32, 9, 33, 8, 7, 34, 35, 6, 5, 36, 4, 37, 38, 3, 2, 39]
LICZBA_MAGAZYNOW = [2467, 2385, 2339, 2337, 2324, 2314, 2270, 2181, 2175, 2145, 2040, 2009, 1946, 1908, 1784, 1774, 1748, 1698, 1659, 1605, 1574, 1547, 1464, 1427, 1270, 1188, 1143, 1103, 1030, 963, 860, 806, 740, 709, 584, 575, 537, 516, 429, 425]

plt.figure(figsize=(12, 6))
plt.bar(ILOSCFIRM, LICZBA_MAGAZYNOW, color='blue', alpha=0.7)
plt.xlabel('Ilość firm')
plt.ylabel('Liczba magazynów')
plt.title('Rozkład liczby firm przypisanych do magazynów')
plt.xticks(ILOSCFIRM)
plt.tight_layout()

plt.show()
