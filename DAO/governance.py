# 100 fungible tokens are minted for the 
# 5 NTFs for the board of directors [ARC3 standard]

from pyteal import *

def approval_program():
    on_creation = Seq(
        [
            # Global byteslice 1
            App.globalPut(Bytes("App_Name"), Bytes("Community 1 Voting Application")),
            # Global byteslice 2
            App.globalPut(Bytes("A_Description"), Bytes("Details for option A.")),
            # Global byteslice 3
            App.globalPut(Bytes("B_Description"), Bytes("Details for option B.")),
            # Global byteslice 4
            App.globalPut(Bytes("C_Description"), Bytes("Details for option C.")),
            # Global byteslice 5
            App.globalPut(Bytes("D_Description"), Bytes("Details for option D.")),
            # Global int 1
            App.globalPut(Bytes("A_Count"), Int(0)),
            # Global int 2
            App.globalPut(Bytes("B_Count"), Int(0)),
            # Global int 3
            App.globalPut(Bytes("C_Count"), Int(0)),
            # Global int 4
            App.globalPut(Bytes("D_Count"), Int(0)),
            # expecting four arguments for the registration and voting time frames
            Assert(Txn.application_args.length() == Int(4)),
            # registration begins blockround
            App.globalPut(Bytes("RegBegin"), Btoi(Txn.application_args[0])),
            # registration ending blockround
            App.globalPut(Bytes("RegEnd"), Btoi(Txn.application_args[1])),
            # vote begining blockround
            App.globalPut(Bytes("VoteBegin"), Btoi(Txn.application_args[2])),
            # vote ending blockround
            App.globalPut(Bytes("VoteEnd"), Btoi(Txn.application_args[3])),
            # Approves sequence
            Return(Int(1))
        ]
    )

    # checks to see if txn sender is the contract creator
    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    # this gets the sender vote from an external application's local state
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))

    # when delete app is called get vote of sender is called and the if statement is called
    on_closeout = Seq(
        [
            get_vote_of_sender,
            # if vote hasnt ended and the user has voted, we delete their vote
            If(
                And(
                    Global.round() <= App.globalGet(Bytes("VoteEnd")),
                    get_vote_of_sender.hasValue(),
                ),
                App.globalPut(
                    get_vote_of_sender.value(),
                    App.globalGet(get_vote_of_sender.value()) - Int(1),
                ),
            ),
            # otherwise we just approve the app deletion
            Return(Int(1)),
        ]
    )

    # checks that the registration period is active before approving opt in
    on_register = Seq(
        And(
            Global.round() >= App.globalGet(Bytes("RegBegin")),
            Global.round() <= App.globalGet(Bytes("RegEnd")),
        ),
        # must have a community voting token
        Assert(),
        # checks if account is a board member with special rights
        App.localPut(Bytes("")),
    )

    # first app arg is assigned to choice variable
    choice = Txn.application_args[1]
    # gets the current choice count value
    choice_tally = App.globalGet(choice)

    # this is the only noop call in this application
    on_vote = Seq(
        [
            # first we check that the voting period is active
            Assert(
                And(
                    Global.round() >= App.globalGet(Bytes("VoteBegin")),
                    Global.round() <= App.globalGet(Bytes("VoteEnd")),
                )
            ),
            # check the local state of the voter and add to the global count
            If(Vote is for A increment A)
                then add + 1 to A
            If(Vote is for B increment B)
                then add + 1 to B
            If(Vote is for C increment C)
                then add + 1 to C
            If(Vote is for D increment D)
                then add + 1 to D

            # need to get the local state of the user and check if it is a board member
            check state for first nft board member
            check state for second nft board member
            check state for third nft board member
            check state for fourth nft board member
            check state for fifth nft board member


            # next the vote of the txn sender is retrieved
            get_vote_of_sender,
            # if the vote exists then we continue executing the sequence
            If(get_vote_of_sender.hasValue(), Return(Int(0))),
            # the choice key is accessed and the tally is updated by adding one 
            App.globalPut(choice, choice_tally + Int(1)),
            # records the voter's choice in the voted key of the voter's local state
            App.localPut(Int(0), Bytes("voted"), choice),
            Return(Int(1)),
        ]
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_register],
        [Txn.application_args[0] == Bytes("vote"), on_vote],
    )

    return program


def clear_state_program():
    # gets the vote of the voted value from the external app
    get_vote_of_sender = App.localGetEx(Int(0), App.id(), Bytes("voted"))
    program = Seq(
        [
            get_vote_of_sender,
            # if the vote has not ended, then remove the account's vote
            If(
                And(
                    Global.round() <= App.globalGet(Bytes("VoteEnd")),
                    get_vote_of_sender.hasValue(),
                ),
                App.globalPut(
                    get_vote_of_sender.value(),
                    App.globalGet(get_vote_of_sender.value()) - Int(1),
                ),
            ),
            Return(Int(1)),
        ]
    )

    return program


if __name__ == "__main__":
    with open("vote_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=2)
        f.write(compiled)

    with open("vote_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=2)
        f.write(compiled)