def main():
    f = open("Desktop/Input.txt","r")
    inputString = f.read()
    #print(var1)
    f.close()

    print(inputString)
    inputArray = inputString.split("\\")

    f1 = open("Desktop/Output.txt","w+")
    print(inputArray)
    #f1.write(inputArray)
    f1.close()
    
if __name__=="__main__":
    main()
