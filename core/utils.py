import csv
import random
import re
import sys

from faker import Faker

fake = Faker("pt_BR")

data = []
for _ in range(int(sys.argv[1])):
    nome = fake.first_name()
    sobrenome = fake.last_name()
    cpf = re.sub(r"\D", "", fake.cpf())
    idade = random.randint(18, 99)

    data.append([nome, sobrenome, cpf, idade])

with open("dados_fake.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["nome", "sobrenome", "cpf", "idade"])
    writer.writerows(data)
