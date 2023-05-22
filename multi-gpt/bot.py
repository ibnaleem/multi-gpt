import discord, json, os, asyncio, openai, datetime, random, uuid, string, random
import translators as ts
from googletrans import Translator
from discord.ext import commands
from discord.ui import Button, View, Select, ChannelSelect
from discord import app_commands, Embed, Interaction
from typing import Optional, List
from pytube import YouTube
from langs import langs
from NASA.images import *

chat_log = []

def generate_symbol_passwords(characters, limit=1):
    symbols = string.punctuation
    if 5 >= limit > 1 and 26 >= characters > 4:
        passwords = []

        for _ in range(limit):
            pswd = ''.join(random.choice(symbols) for _ in range(characters))  # Generating an 8-character password
            passwords.append(pswd)

        return passwords

    if limit == 1 and characters == 4:
        pswd = ''.join(random.choice(symbols) for _ in range(4))

        return pswd

    else:
        return []


def generate_numbers_passwords(characters, limit=1):
    digits = string.digits
    if 5 >= limit > 1 and 26 >= characters > 4:
        passwords = []

        for _ in range(limit):
            pswd = ''.join(random.choice(digits) for _ in range(characters))  # Generating an 8-character password
            passwords.append(pswd)

        return passwords

    if limit == 1 and characters == 4:
        pswd = ''.join(random.choice(digits) for _ in range(4))

        return pswd

    else:
        return []

def generate_str_passwords(characters, limit=1):
    strs = string.ascii_letters
    if 5 >= limit > 1 and 26 >= characters > 4:
        passwords = []

        for _ in range(limit):
            pswd = ''.join(random.choice(strs) for _ in range(characters))  # Generating an 8-character password
            passwords.append(pswd)

        return passwords

    if limit == 1 and characters == 4:
        pswd = ''.join(random.choice(strs) for _ in range(4))

        return pswd

    else:
        return []


with open('config.json') as f:
    config = json.load(f)

# Access the value of TOKEN
TOKEN = config['TOKEN']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), owner_id=1046920598359638036)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(
        name="/help", url='https://www.twitch.tv/gothamchess'))
    print(f"{bot.user} is online with the ID {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(e)

# Access the value of TOKEN
KEY = config['API_KEY']

# Setting API Key for OpenAI
openai.api_key = KEY


@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    elif message.content.startswith("!"):
        pass
    else:
        if isinstance(message.channel, discord.DMChannel):
            num = 1
            while num != 0:
                chat_log.append({"role": "user", "content": message.content})

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log
                )

                gpt_response = response["choices"][0]["message"]["content"]

                chat_log.append({"role": "assistant", "content": gpt_response})

                await message.channel.send(response["choices"][0]["message"]["content"])
                num -= 1
                if num == 0:
                    break
                    
                   
@bot.tree.command(description="Information About Me")
async def info(interaction: Interaction):
    em = Embed(title="MultiGPT's Info",
               description="MultiGPT is a Discord bot that offers additional ChatGPT-functionality through various commands, including the ability to \"humanize\" AI-generated text using the `!humanize (text)` command, and summarize YouTube videos with the `!summarize (url)` command. DM MultiGPT to start a new GPT-conversation! Use `!help` for a list of commands.",
               color=0x070D0D)
    em.add_field(name="Developed by", value="<@1046920598359638036>", inline=True)
    em.add_field(name="Developed in", value="[discord.py](https://github.com/Rapptz/discord.py)", inline=True)
    em.add_field(name="GPT Version", value="GPT-3.5", inline=True)
    em.add_field(name="Number of Servers", value=len(bot.guilds), inline=True)
    em.add_field(name="Prefix", value="/", inline=True)

    button = Button(label="Invite Me", style=discord.ButtonStyle.blurple, emoji="<:logo:1085592985296715796>",
                    url="https://discord.com/api/oauth2/authorize?client_id=1085276371003129937&permissions=1099242667841&scope=bot")
    s_button = Button(label="Support Server", emoji="🛠️", url="https://discord.gg/XBRZwptq6P")
    d_button = Button(label="Donate", emoji='<:pp:1085955313020186724>', url='https://paypal.me/YxngZayn')

    view = View()
    view.add_item(button)
    view.add_item(s_button)
    view.add_item(d_button)

    await interaction.response.send_message(embed=em, view=view)

@bot.tree.command(description="Summarize a YouTube video")
@app_commands.describe(url="YouTube video URL")
async def summarize(interaction: Interaction, url: str):
    yt = YouTube(url)
    stream = yt.streams.filter().first()
    out_file = stream.download()

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    audio_file = open(new_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    new_t = transcript["text"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role":
                "assistant",
            "content":
                f"Your output should use the following template:\n**Summary**\n**Highlights**\n- [Emoji] Bulletpoint\n\nYour task is to summarise the text I have given you in up to seven concise bullet points, starting with a short highlight. Choose an appropriate emoji for each bullet point. Use the text above: {yt.title} {new_t}."
        }])

    embed = Embed(title=f"{yt.title}",
                  description=response['choices'][0]['message']['content'],
                  color=0x070D0D,
                  url=url)

    embed.set_footer(text="!summarize [url] for YouTube video summary")

    await interaction.response.send_message(interaction.user.mention, embed=embed)

    os.remove(new_file)

    
@bot.tree.command(description="YouTube video transcription (subtitles)")
@app_commands.describe(url="YouTube video URL")
async def transcript(interaction: Interaction, url: str):
    yt = YouTube(url)
    stream = yt.streams.filter().first()
    out_file = stream.download()

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    audio_file = open(new_file, "rb")
    trans = openai.Audio.transcribe("whisper-1", audio_file)

    filename = f"transcript-{uuid.uuid4()}.txt"
    with open(filename, "w") as j:
        j.write(trans["text"])
        j.close()

    with open(filename, 'r') as j:
        file = discord.File(j)
        await interaction.response.send_message(
            f"{interaction.user.mention} Here's the transcription for the YouTube video you provided: ",
            file=file)

        j.close()
        os.remove(new_file)
        os.remove(filename)

        
@bot.tree.command(description="Image Generation using DALLE2")
@app_commands.describe(prompt="What do you want to generate?")
async def dalle2(interaction: Interaction, prompt: str):
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    embed = Embed(description=f'"*{prompt}*"', color=0x070D0D)
    embed.set_image(url=response['data'][0]['url'])
    embed.set_footer(text="/dalle2 to generate images")

    await interaction.response.send_message(interaction.user.mention, embed=embed)

    
@bot.tree.command(description="Translate any language")
@app_commands.describe(text="Text to translate", to_lang="The language to translate to")
async def translate(interaction: Interaction, text: str, to_lang: Optional[str] = None):
    if to_lang:
        try:
            result = ts.google(text, to_language=to_lang)
            await interaction.response.send_message(result)
        except:
            await interaction.response.send_message(
                "That is not a valid language. Provide a langauge code (ex. en for English)")

    result = ts.google(text, to_language="en")
    await interaction.response.send_message(result)

    
  
@bot.tree.command(description="Astronomy Picture of the Day")
@app_commands.describe(date="The date of the APOD image to retrieve (YYYY-MM-DD)")
async def apod(interaction: Interaction, date: Optional[str] = None):
    # start_date and end_date are not working with NASA's API
    if date is not None:
        try:
            apod_client = APOD(api_key="ONFzYdMpIcH4xtgr6i2xEe6SWYeHACJtAjKyYWvC")
            url = apod_client.generate(date=date)
            embed = Embed(color=0x0a0000)
            embed.set_image(url=url)
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message(
                f"{date} is not a valid date. Dates must be in the format YYYY-MM-DD.")
    else:
        apod_client = APOD(api_key="ONFzYdMpIcH4xtgr6i2xEe6SWYeHACJtAjKyYWvC")
        url = apod_client.generate()
        embed = Embed(color=0x0a0000)
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)
        
@bot.tree.command(
    description="Daily imagery collected by DSCOVR's Earth Polychromatic Imaging Camera (EPIC)")
@app_commands.describe(natural="Most Recent Natural Color", enhanced="Most Recent Enhanced Color", date="Date of Image")
async def epic(interaction: Interaction, date: str, natural: Optional[bool] = None, enhanced: Optional[bool] = None):
    # NASA's API does not return the image for certain parameters (for example enhanced)
    if natural and enhanced:
        await interaction.response.send_message("You can only choose one: `natural` or `enhanced`.")

    if date and not natural or not enhanced or date and natural:
        try:
            epic_client = EPIC(api_key="ONFzYdMpIcH4xtgr6i2xEe6SWYeHACJtAjKyYWvC")
            img = epic_client.generate(date=date)
            embed = Embed(color=0x0a0000)
            embed.set_image(url=img)

            await interaction.response.send_message(embed=embed)

        except:
            await interaction.response.send_message(
                "You have provided an invalid `date`. Dates must be in the `YYYY-MM-DD` format. Example: 2023-05-13")

    if date and enhanced:
        try:
            epic_client = EPIC(api_key="ONFzYdMpIcH4xtgr6i2xEe6SWYeHACJtAjKyYWvC")
            img = epic_client.generate(date=date, enhanced=True)
            embed = Embed(color=0x0a0000)
            embed.set_image(url=img)

            await interaction.response.send_message(embed=embed)

        except:
            await interaction.response.send_message(
                "You have provided an invalid `date`. Dates must be in the `YYYY-MM-DD` format. Example: 2023-05-13")

    try:
        epic_client = EPIC(api_key="ONFzYdMpIcH4xtgr6i2xEe6SWYeHACJtAjKyYWvC")
        img = epic_client.generate()
        embed = Embed(color=0x0a0000)
        embed.set_image(url=img)

        await interaction.response.send_message(embed=embed)

    except:

        await interaction.response.send_message(
            "You have provided an invalid `date`. Dates must be in the `YYYY-MM-DD` format. Example: 2023-05-13")
        
@bot.tree.command(description="Privately generate password(s)")
@app_commands.describe(letters="Do you want letters in your password(s)?", numbers="Do you want numbers in your password(s)", symbols="Do you want symbols in your password(s)", characters="How many characters in your password(s) (Max 26)", limit="How many passwords do you want to generate? (max. 5)")
async def password(interaction: Interaction, letters: Optional[bool]=None, numbers: Optional[bool]=None, symbols: Optional[bool]=None, characters: Optional[int]=16, limit: Optional[int]=1):
    author = interaction.user

    if letters and numbers and symbols is None:
        await interaction.response.send_message(f"{author.mention} At least `letters`, `numbers` or `symbols` must be set to `True`")

    if 4 > characters:
        await interaction.response.send_message(f"{author.mention} minimum password characters: `4`")

    if letters and numbers is None and symbols is True:
        if 5 >= limit > 1 and 26 >= characters > 4:
            pswds = generate_symbol_passwords(limit, characters)
            embed=Embed(title=f"PASSWORDS", description="\n\n".join(pswd for pswd in pswds), color=0x0a0000)

            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

        if limit == 1 and characters == 4:
            pswd = generate_symbol_passwords(limit, characters)
            embed = Embed(title=f"PASSWORDS", description=pswd, color=0x0a0000)


    if symbols and numbers is None and letters is True:
        if 5 >= limit > 1 and 26 >= characters > 4:
            pswds = generate_str_passwords(limit, characters)
            embed = Embed(title=f"PASSWORDS", description="\n\n".join(pswd for pswd in pswds), color=0x0a0000)

            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

        if limit == 1 and characters == 4:
            pswd = generate_str_passwords(characters, limit=1)
            embed = Embed(title=f"PASSWORDS", description=pswd, color=0x0a0000)
            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

    if symbols and letters is None and numbers is True:
        if 5 >= limit > 1 and 26 >= characters > 4:
            pswds = generate_numbers_passwords(limit, characters)
            embed = Embed(title=f"PASSWORDS", description="\n\n".join(pswd for pswd in pswds), color=0x0a0000)

            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

        if limit == 1 and characters == 4:
            pswd = generate_numbers_passwords(characters, limit=1)
            embed = Embed(title=f"PASSWORDS", description=pswd, color=0x0a0000)
            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

    if letters and numbers and symbols:
        if 5 >= limit > 1 and 26 >= characters > 4:
            pswds_nums = generate_numbers_passwords(limit, characters)
            pswds_strs = generate_str_passwords(limit, characters)
            pswds_sym = generate_symbol_passwords(limit, characters)

            all_passwords = pswds_nums + pswds_strs + pswds_sym

            final_passwords = []
            for _ in range(limit):
                shuffled_passwords = all_passwords.copy()
                random.shuffle(shuffled_passwords)
                final_password = ''.join(shuffled_passwords)
                final_passwords.append(final_password)

            embed = Embed(title=f"PASSWORDS", description='\n\n'.join(pswd for pswd in final_passwords), color=0x0a0000)

            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)

        if limit == 1 and characters == 4:
            pswds_nums = generate_numbers_passwords(characters, limit=1)
            pswds_strs = generate_str_passwords(characters, limit=1)
            pswds_sym = generate_symbol_passwords(characters, limit=1)

            joined_passwords = pswds_nums + pswds_strs + pswds_sym
            random.shuffle(joined_passwords)
            final_password = ''.join(joined_passwords)

            embed = Embed(title=f"PASSWORDS", description=final_password, color=0x0a0000)

            await interaction.response.send_message(author.mention, embed=embed, ephemeral=True)


bot.run(TOKEN)
