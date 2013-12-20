import requests
from Tkinter import *

key = "sSZmea1S_5_Rkpv1Od3HcxVh7B0a"
secret = "YiMyZbcjTy2uwEHyg5yME0tF8tEa"
apihost = "https://agave.iplantc.org/"

class Application(Frame):
    def __init__(self, username="dalanders", password="Shadow@3876", key=key, secret=secret, apihost=apihost, master=None):
        self.apihost = apihost
        self.username = username
        self.password = password
        self.key = key
        self.secret = secret
        self.token = self.getToken("access_token")
        self.refreshToken = self.getToken("refresh_token")
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def getToken(self, tokenType):
        dataPayload = {"grant_type":"client_credentials","username":self.username,"password":self.password,"scope":"PRODUCTION"}
        headersPayload = {"Content-Type":"application/x-www-form-urlencoded"}
        req = requests.post(apihost + "/token", auth=(self.key, self.secret), data=dataPayload, headers=headersPayload)
        return req.json()[tokenType]

    def get(self, rtype, path):
        rtype = rtype + "/2.0/"
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.get(apihost + rtype + path, headers = headersPayload)
        return req.json()

    def post(self, rtype, path, data):
        rtype = rtype + "/2.0/"
        dataPayload = data
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.post(apihost + rtype + path, headers = headersPayload, data=dataPayload)
        return req.json()

    def delete(self, rtype, path):
        rtype = rtype + "/2.0/"
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.delete(apihost + rtype + path, headers = headersPayload)
        return req.json()

    def put(self, rtype, path, data):
        rtype = rtype + "/2.0/"
        dataPayload = data
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.put(apihost + rtype + path, headers = headersPayload, data=dataPayload)
        return req.json()

    def makeListFromResult(self, json, item="name"):
        listFromResult = list()
        for i in range(len(json["result"])):
            listFromResult.append(json["result"][i][item])
        return listFromResult    

    def getAction(self):
        return self.action.get()

    def getRtypestr(self):
        return self.rtypestr.get()

    def getSpecifics(self):
        return self.specifics.get()

    def getResultType(self):
        return self.resultType.get()

    def submitRequest(self):
        self.clearListBox()
        global currentList
        action = self.getAction()
        rtype = self.getRtypestr()
        spec = self.getSpecifics()
        resultType = self.getResultType()
        if action=="get":
            thisRequest = self.get(rtype, spec)
            thisRequestList = self.makeListFromResult(thisRequest, resultType)
            for item in thisRequestList:
                self.listBox.insert(END, item)
            currentList = thisRequestList

    def clearListBox(self):
        global currentList
        self.listBox.delete(0, END)
        currentList = list()

    def deleteListBoxSelect(self):
        global currentList
        namesToRemove = list()
        for each in map(int, self.listBox.curselection()):
            namesToRemove.append(currentList[each])
        for each in namesToRemove:
            currentList.remove(str(each))
            self.listBox.delete(0, END)
        for item in currentList:
            self.listBox.insert(END, item)
        #print currentList

    def select(self):
        global currentList
        namesToKeep = list()
        for each in map(int, self.listBox.curselection()):
            namesToKeep.append(currentList[each])
        self.listBox.delete(0, END)
        currentList = namesToKeep
        for item in currentList:
            self.listBox.insert(END, item)
        #print currentList

    def printCurrentList(self):
        global currentList
        print currentList

    def createWidgets(self):
        self.logo = PhotoImage(file="logo.gif")
        self.Title = Label(self, image=self.logo)
        self.Title.grid(row=0, column=0, columnspan=6, pady=10)

        self.Submit = Button(self)
        self.Submit["text"] = "Submit"
        self.Submit["command"] = self.submitRequest
        self.Submit.grid(row=3, column=5)

        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["command"] = self.quit
        self.QUIT.grid(row=4, column=5)

        self.action = StringVar(self)
        self.action.set("get")
        self.actionOption = OptionMenu(self, self.action, "get", "post", "put", "delete")
        self.actionOption.grid(row=1, column=2, columnspan=2, pady=7.5)

        self.rtypestr = StringVar(self)
        self.rtypestr.set("files")
        self.rtypeOption = OptionMenu(self, self.rtypestr, "files", "apps")
        self.rtypeOption.grid(row=2, column=2, columnspan=2, pady=7.5)

        self.label1 = Label(self)
        self.label1["text"] = "Request"
        self.label1.grid(row=1, column=0)

        self.label2 = Label(self)
        self.label2["text"] = "API"
        self.label2.grid(row=2, column=0)

        self.specifics = StringVar(self)
        self.specifics.set("listings/")
        self.specificsEntry = Entry(self, textvariable=self.specifics)
        self.specificsEntry.grid(row=3, column=2, columnspan=2, pady=7.5)

        self.label3 = Label(self)
        self.label3["text"] = "Location"
        self.label3.grid(row=3, column=0)

        self.resultType = StringVar(self)
        self.resultType.set("name")
        self.resultTypeEntry = Entry(self, textvariable=self.resultType)
        self.resultTypeEntry.grid(row=4, column=2, columnspan=2, pady=7.5)

        self.label4 = Label(self)
        self.label4["text"] = "Result Type"
        self.label4.grid(row=4, column=0)

        self.label5 = Label(self, fg='red')
        self.label5["text"] = "Selected List A"
        self.label5.grid(row=6, column=0)

        self.listBox = Listbox(self, selectmode=EXTENDED)
        self.listBox.config(height=30, width=50)
        self.listBox.grid(row=7, column=0, columnspan=3)

        self.label7 = Label(self, fg='red')
        self.label7["text"] = "Selected List B"
        self.label7.grid(row=6, column=3)

        self.listBoxB = Listbox(self, selectmode=EXTENDED)
        self.listBoxB.config(height=30, width=50)
        self.listBoxB.grid(row=7, column=3, columnspan=3)

        self.listDelete = Button(self)
        self.listDelete["text"] = "Delete"
        self.listDelete["command"] = self.deleteListBoxSelect
        self.listDelete.grid(row=2, column=5)

        self.selectMe = Button(self)
        self.selectMe["text"] = "Select"
        self.selectMe["command"] = self.select
        self.selectMe.grid(row=1, column=5)

        self.printCL = Button(self)
        self.printCL["text"] = "Print Selection"
        self.printCL["command"] = self.printCurrentList
        self.printCL.grid(row=0, column=5)

        self.label6 = Label(self)
        self.label6["text"] = "Data"
        self.label6.grid(row=5, column=0)

        self.data = StringVar()
        self.dataEntry = Entry(self, textvariable=self.data)
        self.dataEntry.grid(row=5, column=2, columnspan=2, pady=7.5)

root = Tk()
root.wm_title('Aloe for Agave')
app = Application(master=root)
app.mainloop()
root.destroy()