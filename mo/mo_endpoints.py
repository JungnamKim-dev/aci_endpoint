class mo_endpoints():
    def __init__(self):
        self.map_endpoint = {}

    def update_EndPoint(self, dn, **datas):
        if dn not in self.map_endpoint:
            self.map_endpoint[dn] = {}
        
        if len(datas) > 0:
            for key in datas:
                self.map_endpoint[dn][key] = datas[key]

    def delete_EndPoint(self, dn):
        if dn in self.map_endpoint:
            del self.map_endpoint[dn]

    def print_EndPoint(self, attr=[]):
        print("============ EndPoint List ==============")
        for dn, datas in self.map_endpoint.items():
            print("DN:%s" % dn)
            output_attr = ""
            for key in datas.keys():
                if len(attr) == 0 or key in attr:
                    output_attr += "'%s':'%s', " % (key, datas[key])
            print("\t{%s}" % output_attr)

        print("============ EndPoint List(end) ==============")


