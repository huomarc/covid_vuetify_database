from covid import Covid

covid = Covid()

italy_cases = covid.get_status_by_country_name("italy")


print(italy_cases['id'])
print(italy_cases['country'])
print(italy_cases['confirmed'])
print(italy_cases['deaths'])
print(italy_cases['recovered'])
print(italy_cases['last_update'])