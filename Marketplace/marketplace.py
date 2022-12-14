# each product is represented by an application
# buy product by making a call to the app and performing a payment to the creator

from pyteal import *

class Item:
    # class holds the variables
    class Vars:
        supplier = Bytes("Supplier")
        name = Bytes("Name")
        image = Bytes("Image")
        description = Bytes("Description")
        price = Bytes("Price")
        sold = Bytes("Sold")
    # class holds the methods
    class Methods:
        fund = Bytes("Fund")
    # method for sending the cart to crowdfund
    def fund(self):
        # assign the first app arg to count
        amount = Txn.application_args[1]
    # method creates a product
    def app_creation(self):
        return Seq(
            # requires 5 app args for call
            Assert(Txn.application_args.length() == Int(5)),
            # requires note
            Assert(Txn.note() == Bytes("marketplace:uv1")),
            # requires price is greater than zero
            Assert(Btoi(Txn.application_args[4]) > Int(0)),
            # supplier is zeroth app arg
            App.globalPut(self.Vars.supplier, Txn.application_args[0]),
            # name is first app arg
            App.globalPut(self.Vars.name, Txn.application_args[1]),
            # image is second app arg
            App.globalPut(self.Vars.image, Txn.application_args[2]),
            # description is third app arg
            App.globalPut(self.Vars.description, Txn.application_args[3]),
            # price is the fourth app arg
            App.globalPut(self.Vars.price, Txn.application_args[4]),
            # intiializes the sold var to zero sold
            App.globalPut(self.Vars.sold, Int(0)),
            # approves the sequence
            Return(Int(1)),
        )
    # method for deleting a item
    def app_delete(self):
        # only allows deletion of item if caller is app creator
        return Return(Txn.sender() == Global.creator_address())
        # application start method
    def app_start(self):
        return Cond(
            # calls app create method if app doesn't exist
            [Txn.application_id() == Int(0), self.app_creation()],
            # if the txn type is delete then delete app
            [Txn.on_completion() == OnComplete.DeleteApplication, self.app_delete()],
            # if the zeroth app arg is fund, call the fund method
            [Txn.application_args[0] == self.Methods.fund, self.fund()],
        )
    # approval program
    def approval_prog(self):
        # returns the app start method 
        return self.app_start()
    # clear program
    def clear_prog(self):
        # return as approved
        return Return(Int(1))