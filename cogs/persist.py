import discord
import pickle
import env
import asyncio

from discord.ext import commands, tasks

BACKUP_FILE = 'jenna.pk'
BACKUP_CHANNEL = 695931720909717534
BACKUP_LIMITS = 10

class Persist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.loaded = False
        self.data_changed = False
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.backup_channel = self.bot.get_channel(BACKUP_CHANNEL)
        last_message = await self.backup_channel.history(limit=1).flatten()
        backup_file = last_message[0].attachments if last_message else None

        if backup_file:
            await backup_file[0].save(BACKUP_FILE)
            self.data = pickle.load(open(BACKUP_FILE, 'rb'))
        self.loaded = True
        
        if env.TESTING: return
        self.backup_loop.start()
    
    async def wait_until_loaded(self):
        while not self.loaded:
            await asyncio.sleep(.5)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data_changed = self.data.get(key) != value
        self.data[key] = value
    
    @tasks.loop(seconds=10)
    async def backup_loop(self):
        if not self.data_changed: return
        await self.upload_backup()
        await self.delete_old_backups()

    async def upload_backup(self):
        pickle.dump(self.data, open(BACKUP_FILE, 'wb'))
        await self.backup_channel.send(file=discord.File(BACKUP_FILE))
    
    async def delete_old_backups(self):
        all_backups = await self.backup_channel.history(limit=None, oldest_first=True).flatten()
        expired = len(all_backups) - BACKUP_LIMITS
        if expired > 0:
            old_backups = all_backups[:expired]
            await self.backup_channel.delete_messages(old_backups)

def setup(bot):
    bot.add_cog(Persist(bot))