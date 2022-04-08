from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="GetLoc")
municipio = input("digite o nome do municipio: ")
getLoc = loc.geocode(municipio)
endereco = getLoc[0]
endereco = endereco.split(',')

for x in endereco:
    print(f"\t{x}")

print("cordenadas = ", getLoc[1])
