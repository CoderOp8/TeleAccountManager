from pyrogram import Client, filters
from Tools.client import Execute, Run
from Tools.parser import parse_kwargs
from Tools.info import logger, db
from Tools.methods.refresh import Refresh
from Tools.methods.get_code import GetCode
from time import perf_counter as pc
from rich.console import Console

client = Client(
    "MainAccount"
)

def is_me(filter,cli,update):
    try:
        return update.from_user.id == cli.me.id
    except:
        return False
console = Console()
console.print("🚀 NASA Script Is Running...", style="bold green")

IsMe = filters.create(is_me, "IsMe")

@client.on_message(filters.text & IsMe)
async def main_handler(bot, m):
    user = m.from_user
    txt = m.text.split()
    command = txt[0].replace("/", "")

    

    if command in ["send_message", "join_chats","leave_chats", "ref","click","send_contact", "add_contact", "send_reaction","send_vote", "unsend_vote", "export_chats","captcha", "watch"]:
        kwargs = parse_kwargs(m.text, txt[0])
        await m.reply("📋 Executing The Task...")
        try:
            count = pc()
            result = await Execute(command, kwargs)
            return await m.reply(f"✅ Task Executed: {result['done']}/{result['total']} Accounts\n🕚 Estimated Time Taken: {pc() - count}s\n\n🔺By @CoderOp")

        except Exception as e:
            logger.error(e)
            return await m.reply("⚠️ Please Check The Code Again.")

    elif command == "run":
        if m.reply_to_message is not None:
            if m.reply_to_message.document is not None:
                script = m.reply_to_message.document
                await m.reply_to_message.download(script.file_name)

                await m.reply(f"Executing {script.file_name.replace('.json','')}⏰")
                count = pc()
                result = await Run(bot,m,f"downloads/{script.file_name}")
                return await m.reply(f"Finished {script.file_name.replace('.json', '')} in {pc() - count} Seconds✅")


        return await m.reply('Please reply to a message that has a script')

    elif command == "delete":
        try:
            account = txt[1]
            if db.check_exist(account):
                ss = db.get_account_info(account)["session_string"]
                db.delete_account(account)
                app = Client(account, session_string=ss)
                try:
                    await app.connect()
                    await app.log_out()
                except:
                    pass
                return await m.reply(f"Deleted {account}✅")
            return await m.reply("This phone number is not in the DB")
        except:
            return await m.reply("Please put a phone number to delete")

    elif command == "refresh":
        await m.reply("🔺 Refreshing Accounts")
        inf = await Refresh.refresh()
        text = f'''
🔎 Refreshed Account Lists Details:

🗄 Total Accounts : {inf["total"]}
❗️ Banned Accounts : {inf["banned"]}
❕ Revoked Accounts : {inf["revoked"]}
✅ Remaining Accounts : {inf["remain"]}

✨ Owner : @CoderOP

        '''
        return await m.reply(text)

    elif command == "get_code":
        try:
            account = txt[1]
            if db.check_exist(account):
                ss = db.get_account_info(account)["session_string"]
                code  = await GetCode.get_code(account, ss)
                if isinstance(code, str):
                    return await m.reply(f"{account} code is {code}")
                elif code is None:
                    return await m.reply("did not recive the code yet!")
                elif code is False:
                    db.delete_account(account)
                    return await m.reply(f"{acccount} Is Banned 📛")
            return await m.reply("This phone number is not in the DB")
        except Exception as e:
            print(e)
            return await m.reply("Please but a phone number")

client.run()
