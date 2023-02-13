import pyromod.listen
from pyrogram import Client,filters,types
from pyrogram.errors import SessionPasswordNeeded

# proxy = {
#      "scheme": "HTTP",  # "socks4", "socks5" and "http" are supported
#      "hostname": "192.168.1.111",
#      "port": 8080
# }

Account=Client("AccountSession",10171739,"3d7bf2a25d6629a32b3a86731eebe05e",device_model="Samsung Galaxy A71")

StateLogin=Account.connect()
if StateLogin is False:
    Phone_Number=input("Phone: ")
    SendLoginCode=Account.send_code(Phone_Number)
    CodeLogin=input("Login Code: ")
    try:
        Account.sign_in(Account,Phone_Number,SendLoginCode.phone_code_hash,CodeLogin)
    except SessionPasswordNeeded:
        Account.check_password(input("Password: "))
    if Account.is_connected:
        print("Login succsess :)")
    else:
        print("Login feild :(")
Account.disconnect()

Admins=[]

NewAdmin=input("Number Id Admin: ")

Admins.append(NewAdmin)

global MessageText
MessageText=''

@Account.on_message(filters.channel)
async def NewPost(_:Account,Message:types.Message):
    try:
        global MessageText
        UserId=Message.chat.id
        MessageId=Message.id
        if MessageText!='':
            NewPost=await Account.get_discussion_message(UserId,MessageId)
            await NewPost.reply(MessageText)
    except Exception as e:
        pass

@Account.on_message(filters.chat(Admins),filters.private)
async def AdminManage(_:Account,Message:types.Message):
    UserId=Message.from_user.id
    Text=Message.text
    global MessageText
    if Text=="Help":
        await Account.send_message(UserId,"Hi\n`Ping` => Online\n`NewMessage` => Set New Message For Comment To Post Linked Group Chanell\n`SeeMessage` => Show Last Message Set.")
    elif Text=="Ping":
        await Account.send_message(UserId,"~ Online")
    elif Text=="NewMessage":
        MessageAlert="- Send Your Text Message?\nCurrent Text: {0}"
        if MessageText == '':
            MessageText=await Account.ask(UserId,MessageAlert.format('⚠️ No Message Text ⚠️'))
        else:
            MessageText=await Account.ask(UserId,MessageAlert.format(MessageText))
        MessageText=MessageText.text
        await Account.send_message(UserId,"Message Saved.")
    elif Text=="SeeMessage":
        if MessageText == '':
            await Account.send_message(UserId,'⚠️ No Set Message Text ⚠️')
        else:
            await Account.send_message(UserId,"Curent Message Is : {0}".format(MessageText))

Account.run(print("~ Run"))