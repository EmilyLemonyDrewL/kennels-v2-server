from views import search_animals

# test name search
print("NAME TEST")
find = "Darcia"
results = search_animals(find)
print(results)

# test breed search
print("BREED TEST")
find = "Bo"
results = search_animals(find)
print(results)

print("TEST 3")
find = "corn"
results = search_animals(find)
print(results)
