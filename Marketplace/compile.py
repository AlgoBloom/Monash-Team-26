from pyteal import *

from marketplace import Item

if __name__ == "__main__":
    approval_program = Item().approval_prog()
    clear_program = Item().clear_prog()

    # Mode.Application specifies that this is a smart contract
    compiled_approval = compileTeal(approval_program, Mode.Application, version=6)
    print(compiled_approval)
    with open("marketplace_approval.teal", "w") as teal:
        teal.write(compiled_approval)
        teal.close()

    # Mode.Application specifies that this is a smart contract
    compiled_clear = compileTeal(clear_program, Mode.Application, version=6)
    print(compiled_clear)
    with open("marketplace_clear.teal", "w") as teal:
        teal.write(compiled_clear)
        teal.close()