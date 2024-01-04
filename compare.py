import pandas as pd

with open("job_20240103135833.csv","r") as csv_1,open ("job_20240103153842.csv") as csv_2:
    import_1 = csv_1.readlines()
    import_2 = csv_2.readlines()

with open("uniqe_data","w") as uniqe_data:
    for row in import_2:
        if row not in import_1:
            uniqe_data.write(row)
