import lab02_utilitis

db = lab02_utilitis.base_datos_aleatoria(101)

print("Media PD:",lab02_utilitis.q1(db, 1))
print("Mediana PD:",lab02_utilitis.q2(db, 1))
print("Bitcount PD:",lab02_utilitis.q3(db, 1))
print("Histograma PD:",lab02_utilitis.q4(db, 1))