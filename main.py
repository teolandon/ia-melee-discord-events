import discord

class EventsClient(discord.Client):
    async def on_ready(self):
        guild = self.guilds[0]
        await self.http.create_guild_scheduled_event(
            guild_id=guild_id,
            entity_metadata={
                "location":"https://www.start.gg/tournament/dmgc-smash-bros-local-38/"
            },
            name="DMGC Weekly 38",
            privacy_level=2,
            scheduled_start_time="2022-09-01T19:00-05:00",
            scheduled_end_time="2022-09-01T22:00-05:00",
            description="Des Moines Melee & Ultimate Weekly Tournament",
            entity_type=3,
        )
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        pass

client = EventsClient(intents=None)
client.run(token)
