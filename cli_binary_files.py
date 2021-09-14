from io import BufferedWriter

from pickle import load, dump

def open_binary_file(filename, mode):
     if mode == "RANDOM":
          return RandomFile(filename)
     elif mode == "SEQUENTIAL":
          return SequentialFile(filename)
     elif mode == "SERIAL":
          return SerialFile(filename)
     else:
          raise Exception(f"Mode {mode} is invalid")
     
     

class BinaryFile():
     def __init__(self, filename, size=None):
          self.filename = filename
          self.pointer = 0
          self.closed = False
          self.size = size

          try:
               with open(self.filename, "rb") as f:
                    self.records = load(f)
          except:
               self.records = []


     ## to do - decorator function checks if file is still open
     def check_open(func):
          def wrapper(self):
               if self.closed:
                    raise Exception(f"Error - cannot operate on a closed file")

          

     def seek(self, address):          
          self.pointer = address   

     def put_record(self, record):

          try:
               self.records[self.pointer] = record              
          except:
               raise Exception(f"Address {self.pointer} does not exist in this file")


     def get_record(self):
        
          try:
               return self.records[self.pointer]
          except:
               raise Exception(f"Address {self.pointer} does not exist in this file")


     def close(self):
          with open(self.filename, "wb") as f:
               dump(self.records, f)
          
     def eof(self):
          pass

class RandomFile(BinaryFile):
     def __init__(self, filename, size=None):
          super().__init__(filename, size)

     def seek(self, address):
          if self.size is not None:
               if address > self.size:
                    raise Exception(f"Address {address} does not exist in this file")
               
          record_count = len(self.records)          
          self.records += [None for i in range((address+1) - record_count)]
          self.pointer = address

          

          
          

class SequentialFile(BinaryFile):
     def __init__(self, filename, size=None):
          super().__init__(filename)

     def get_record(self):
          record = super().get_record()          
          self.pointer += 1
          
          return record

     def put_record(self, record):          
          self.records.append(record)
          
      

class SerialFile(BinaryFile):
     def __init__(self, filename, size=None):
          super().__init__(filename)

     def put_record(self, record):          
          self.records.append(record)
      
     def get_record(self):
          record = super().get_record()          
          self.pointer += 1
          return record

     def seek(self, address):
          raise Exception("Serial files do not support direct access")
     


class Record:
     def __init__(self):
          self.name = ""
          self.age = 0

person1 = Record()
person1.name = "Bob"
person1.age = 77

person2 = Record()
person2.name = "Sally"
person2.age = 60

person3 = Record()
person3.name = "Alice"
person3.age = 50


from os import remove, getcwd

try:
     remove(getcwd()+"/serial.dat")
     remove(getcwd()+"/sequential.dat")
     remove(getcwd()+"/random.dat")
except:
     pass


if __name__ == "__main__":

     print("\nSerial file demo\n")

     file = open_binary_file("serial.dat", "SERIAL")

     file.put_record(person1)
     file.put_record(person2)
     file.put_record(person3)

     for i in range(3):
          next_record = file.get_record()
          print(f"At position {i} we have {next_record.name} who is {next_record.age} years old")

     file.close()

     print("Serial files support sequential access only.")



     print("\nSequential file demo\n")

     file = open_binary_file("sequential.dat", "SEQUENTIAL")

     file.put_record(person1)
     file.put_record(person2)
     file.put_record(person3)

     for i in range(3):
          next_record = file.get_record()
          print(f"At address {i} we have {next_record.name} who is {next_record.age} years old")

     file.seek(2)
     print(f"Jumped straight to address 2 and found {next_record.name}.")
     file.close()
     print("Serial files support both sequential access and direct access.")


     
     print("\nRandom file demo\n")

     file = open_binary_file("sequential.dat", "RANDOM")

     file.put_record(person1)
     file.put_record(person2)
     file.put_record(person3)

     for i in range(3):
          next_record = file.get_record()
          print(f"{next_record.name} who is {next_record.age} years old")
          

     print("Random files can only  be read or written sequentially")     
     print("Each record overwrites the last as the file pointer has not changed.")
     print("Let's try again - this time we will seek to a new address each record.")


     for address, record in zip([10, 20, 30], [person1, person2, person3]):
          file.seek(address)
          file.put_record(record)
          print(f"Wrote {record.name}'s record to address {address}")



     file.seek(10)
     record = file.get_record()
     print(f"Jumped straight to address 10 and found {record.name}.")
     
     

     file.seek(20)
     record = file.get_record()
     print(f"Jumped straight to address 20 and found {record.name}.")

     file.close()

     
