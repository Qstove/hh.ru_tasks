import itertools

#convert tuple to string
def convertTuple(tup): 
    str =  ''.join(tup) 
    return str
  
#relationship for buttons (0..9)
numbers_rel_to_PIN = {
    '1': ('1', '2', '4'),
    '2': ('2', '1', '3','5'),
    '3': ('3', '2', '6'),
    '4': ('4', '1', '5','7'),
    '5': ('5', '2', '4','6','8'),
    '6': ('6', '3', '5','9'),
    '7': ('7', '4', '8'),
    '8': ('8', '5', '7','9','0'),
    '9': ('9', '6', '8'),
    '0': ('0','8')
}

inputPinString = input("Какой говоришь был пароль?..\n")

list_of_arrays = []
for num in inputPinString:
    numArr = numbers_rel_to_PIN[num]
    list_of_arrays.append(numArr)

listOfPins = []
for element in itertools.product(*list_of_arrays):
    listOfPins.append(convertTuple(element))

listOfPins.sort()

print(*listOfPins, sep = ",") 

