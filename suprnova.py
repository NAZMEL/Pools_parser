from grab import Grab

class SuprnovaParse(object):
    g = Grab()
    def __init__(self, _name, _username, _password, _subdom = 'lbry'):
        self.worker_data = []
        self.subdom = _subdom
        self.name = _name
        try:
            self.g.go('https://{0}.suprnova.cc/index.php?page=login'.format(self.subdom))
            self.g.doc.set_input('username', _username.encode('ascii'))
            self.g.doc.set_input('password', _password.encode('ascii'))    
            self.g.doc.submit() 
        except Exception as ex:
            # no connection
            print(str(ex))

    def Select(self):
        self.g.go('https://{0}.suprnova.cc/index.php?page=account&action=workers'.format(self.subdom))
        html_td = self.g.doc.select('//table[@class = "table"]/tbody/tr')
        count = 1
        for item in html_td:
            tmp = item.text().split(' ')
            tmp[0] += str(count)
            
            if tmp[1] != '0':                                                     # only active workers
                self.worker_data.append(tmp)
            count+=1
        if self.worker_data == []:
            return False

    def record_data(self):
        with open('suprnova.log', 'a') as f:
            if self.Select() != False:
                for item in self.worker_data:
                    f.write(self.name +'\t\t' + item[0] + '\t' + item[1] + '\t\t\t' + item[2] + '\n')
            else:
                f.write(self.name)
            f.write('\n-----------------------------------------------------------------------------\n')
            
    def Logout(self):
        self.g.go('https://{0}.suprnova.cc/index.php?page=logout'.format(self.subdom))
    
def first_record():
    with open('suprnova.log' , 'w') as f:
        f.write('Name\t\tActive worker\t\tKahsh/s\t\tDifficulty\n')
        f.write('-----------------------------------------------------------------------------\n')

def record_subdom(subdom):
    with open('suprnova.log' , 'a') as f:
        f.write('\n\t\t\t\t' + subdom + '\n-----------------------------------------------------------------------------\n')

def read_file_supr(name):
    lines = []
    main_dict = {}
    with open (name, 'r') as file:
        lines = file.readlines()
        if lines == []:
            return False
        if not file.closed:
            file.close()

    tmp = lines[0][:-1]                      
    tmp_arr = []
    for i in range(1,len(lines)):
        lines[i] = lines[i].strip().split(' ')
        if len(lines[i]) == 1:
            main_dict[tmp] = tmp_arr
            tmp = lines[i][0]
            tmp_arr = []
            continue

        if lines[i][1].rfind('\n') != -1:
            lines[i][1] = lines[i][1][:-1]
        tmp_arr.append(lines[i])

    main_dict[tmp] = tmp_arr
    return main_dict
    
    


def main():
    first_record()
    data_supr = read_file_supr(r'Resource\suprnova.txt')
    for item in data_supr.keys():
        record_subdom(item)
        for val in data_supr[item]:
            a = SuprnovaParse(val[0],val[1], val[2], item)
            a.record_data()
            a.Logout()

if __name__ == '__main__':
    main()









