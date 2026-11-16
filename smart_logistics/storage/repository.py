import json

import os

class Repository:

    def __init__(self,file_name):
        self.file_name=file_name


        os.makedirs("data",exist_ok=True)

        self.file_path=os.path.join("data",file_name)

        if not os.path.exists(self.file_path):
            with open(self.file_path,"w") as file :

                json.dump([],file)


    def load_data(self)    :
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save_data(self, data):
        temp_path = self.file_path + ".tmp"

        with open(temp_path, "w") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_path, self.file_path)

    def add(self, new_data):
        data = self.load_data()
        data.append(new_data)
        self.save_data(data)

    def get_all(self):
        return self.load_data()  
      

    def get_by_id(self, record_id):
      data = self.load_data()

      for record in data:
        if record["id"] == record_id:
            return record

      
      return None    




    def update(self, record_id, updated_data):

        data = self.load_data()

        for index, record in enumerate(data):

            if record["id"] == record_id:

                data[index] = updated_data

                self.save_data(data)

                return True

        return False


    def delete(self, record_id):

        data = self.load_data()

        for record in data:

            if record["id"] == record_id:

                data.remove(record)

                self.save_data(data)

                return True

        return False