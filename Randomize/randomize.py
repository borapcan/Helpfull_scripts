import random 

double_plate_list=[]

for i in range(85):
    if i<10 :
        if i==8:
            pass
        else:
            double_plate_list.append(f"KOR140{i+1}.1")
            double_plate_list.append(f"KOR140{i+1}.2")
    else:
        if i==32: 
            pass
        elif i==34: 
            pass
        elif i==44:
            pass
        elif i==52: 
            pass
        elif i==55: 
            pass
        elif i==63: 
            pass
        else:
            double_plate_list.append(f"KOR14{i+1}.1")
            double_plate_list.append(f"KOR14{i+1}.2")

random.shuffle(double_plate_list)
plate_1 = double_plate_list[:len(double_plate_list)//2]
plate_2 = double_plate_list[len(double_plate_list)//2:]

for i in range(12):
    plate_1.append(f"Standard")
    plate_2.append(f"Standard")

for i in range(6):
    plate_1.append(f"Blank")
    plate_2.append(f"Blank")

random.shuffle(plate_1)
random.shuffle(plate_2)


#print(double_plate_list)

f  = open("plate_1.txt", "w+")
for list_item in plate_1:
    f.write(f"{list_item}\n")
f.close()


f  = open("plate_2.txt", "w+")
for list_item in plate_2:
    f.write(f"{list_item}\n")
f.close()
