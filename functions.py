def bin_to_dec(number):
    #print len(str(number))
    binary_sum = []
    reversed_number = str(number)[::-1]
    for i in range (0,len(str(number))):
        #print str(number)[i]
        if str(reversed_number)[i]=='0':
            #print 0
            binary_sum.append(0)
        if str(reversed_number)[i]=='1':
            #print 1
            binary_sum.append(2**int(i))
    result = 0
    for sum in binary_sum:
        result+=sum
    #print number
    #print reversed_number
    #print binary_sum
    return result



def bin_to_hex(number):
    #print len(str(number))
    binary_sum = []
    hex_pipe =[]
    lennn = 0
    hex_number = ''
    reversed_number = str(number)[::-1]

    for i in range(1, 1+len(str(number))):
        hex_number +=  str(reversed_number)[i-1]
        #print reversed_number[i]
        #print i,' = ', i%4
        if(i%4==0 and i!=1):
            hex_pipe.append(hex_number)
            hex_number = ''
        lennn =  int(len(str(number)))/4.0
    if (lennn%2 != 0.0):
        hex_pipe.append(hex_number)
    #print hex_pipe

    for i in range (0,len(hex_pipe)):
        if (hex_pipe[i]==''):
            del hex_pipe[i]
    #print hex_pipe

    result_list = []
    for hex in hex_pipe:
        sum = 0
        for i in range (0,len(hex)):
            if str(hex)[i] == '0':
                pass
            if str(hex)[i] == '1':
                #print i
                sum += 2 ** int(i)
                #print sum, '-------------',2 ** int(i)

        if (sum>9):
            if(sum==10):
                sum = 'A'
            elif (sum== 11):
                sum = 'B'
            elif (sum == 12):
                sum = 'C'
            elif(sum==13):
                sum = 'D'
            elif (sum == 14):
                sum = 'E'
            elif(sum==15):
                sum = 'F'
        result_list.append(str(sum))

    result = ''
    for reversed1 in reversed(result_list):
        result += str(reversed1)
    return result


def dec_to_bin(number):
    bin_number=''
    number = int(number)
    #for i in range(0, len(str(number))):
    while(number >= 1):
        bin_number += str(number%2)
        number= number/2

        #print number
    bin_number = bin_number[::-1]
    return bin_number

def dec_to_hex(number):
    result =''
    result = dec_to_bin(number)
    #print result
    result = bin_to_hex(result)
    return result

def hex_to_dec(number):
    hex_number=''
    result = 0
    reversed=str(number)[::-1].upper()
    #print reversed
    for i in range (0,len(reversed)):
        #result += (int(reversed[i])*(10**i))

        if(reversed[i]=='A'):
              hex_number = 10
        elif (reversed[i]== 'B'):
               hex_number = 11
        elif (reversed[i] == 'C'):
               hex_number = 12
        elif(reversed[i]=='D'):
               hex_number = 13
        elif (reversed[i] == 'E'):
               hex_number = 14
        elif(reversed[i]=='F'):
               hex_number = 15
        if(hex_number==''):
            hex_number=int(reversed[i])
        #print (int(reversed[i]) * (10 ** i))
        result += hex_number * (16 ** i)
        #print int(reversed[i])
        hex_number=''
    return result

def hex_to_bin(number):
    result = ''
    result = hex_to_dec(number)
    #print result
    result = dec_to_bin(result)
    return result