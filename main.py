from datetime import datetime, timedelta
import argparse
import discord
import json


parser = argparse.ArgumentParser(description='IA Melee Discord Events scheduler')
parser.add_argument('--token', dest='token', action='store', help='The token for the Discord bot')
parser.add_argument('--guild', dest='guild', action='store', help='The guild/server ID for IA Melee')

args = parser.parse_args()
token = args.token
guild_id = args.guild

with open("tourneys.json", "r") as f:
    tourneys = json.load(f)

today = datetime.now().astimezone()


class EventsClient(discord.Client):
    async def on_ready(self):
        for tourney in tourneys:
            tourney_first_date = datetime.fromisoformat(tourney["first_date"])

            today_weekday = today.weekday()
            tourney_weekday = tourney_first_date.weekday()

            if (today_weekday - tourney_weekday) % 7 == 1:
                target_date = today + timedelta(days=6)
                target_start_date = target_date.replace(hour=tourney_first_date.hour, minute=tourney_first_date.minute)
                target_end_date = target_start_date + timedelta(hours=tourney["duration_h"])
                number = tourney["offset"] + ((target_start_date - tourney_first_date).days // 7)
                await self.http.create_guild_scheduled_event(
                    guild_id=guild_id,
                    entity_metadata={
                        "location":tourney["link"].format(number=number)
                    },
                    name=tourney["name"].format(number=number),
                    privacy_level=2,
                    scheduled_start_time=target_start_date.isoformat(),
                    scheduled_end_time=target_end_date.isoformat(),
                    description=tourney["description"],
                    entity_type=3,
                )
        await self.close()


client = EventsClient(intents=None)
client.run(token)
