import os

class fgrab:
    def __init__(self,path):
        self.path = path
        self.result = list()

    def get_all_in_dir(self,filetype):
        for filename in os.listdir(self.path):
            if filename.endswith(filetype):
                r = os.path.join(self.path, filename)
                self.result.append(r)
        return self.result