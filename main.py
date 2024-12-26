import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import opus
import random
import os

if not opus.is_loaded():
    opus.load_opus("libopus.so")  # Railway автоматически находит библиотеку Opus

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Получаем токен из переменной окружения

# Глобальный путь к звуковым файлам
SOUND_PATH = "sounds/"  # Папка, где хранятся звуковые файлы

# Список звуков
SOUNDS = [
    "здарова_братиш.mp3", "family.mp3", "trenbalon.mp3", "fart.mp3",
    "mama-ia-pokakal.mp3", "ia-mishka-gomogei-dyriavyi-gomogei.mp3",
    "chto-u-vas-zdes-proiskhodit.mp3", "Dzhigit.mp3", "ded.mp3", "negr.mp3",
    "lya-ty-krysa.mp3", "sistema-poiska-aktivirovana.mp3",
    "ay-bolno-v-noge.mp3", "pelmeni.mp3", "rayonnyy-prokuror.mp3",
    "CHjornye_glaza.mp3", "ser.mp3", "CHE_ZA_LEV_JETOT_TIGR.mp3", "oshibka.mp3", "жопа.mp3", "трезвыми.mp3", "кунг-фу.mp3"
]

# Звук для конкретного пользователя
USER_SPECIFIC_SOUND = "милк_пупс.mp3"
SPECIFIC_USER_NAME = "Mi1kBoobs"  # Имя пользователя на сервере

# Настройка намерений (intents)
intents = discord.Intents.all()
intents = discord.Intents.default()  # Загружаем базовые намерения
intents.presences = True  # Включаем отслеживание статусов пользователей (Presence Intent)
intents.members = True  # Включаем работу с участниками сервера (Server Members Intent)

bot = commands.Bot(command_prefix="!", intents=intents)


# Событие: бот запущен
@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен и готов к работе!")


# Обработчик входа/выхода участников в голосовой канал
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # Пользователь вошёл в канал
        if not member.bot:  # Игнорируем самого бота
            voice_client = discord.utils.get(bot.voice_clients,
                                             guild=after.channel.guild)
            if voice_client is None or not voice_client.is_connected(
            ):  # Если бот ещё не подключён
                voice_client = await after.channel.connect(
                )  # Подключаемся к голосовому каналу

            # Если это конкретный пользователь
            if member.name == SPECIFIC_USER_NAME:
                sound_to_play = USER_SPECIFIC_SOUND
                print(
                    f"Проигрывается персональный звук для {member.name}: {sound_to_play}"
                )
            else:
                # Для всех остальных случайный звук
                sound_to_play = random.choice(SOUNDS)
                print(
                    f"Проигрывается случайный звук для {member.name}: {sound_to_play}"
                )

            # Проигрываем звук
            audio = FFmpegPCMAudio(f"{SOUND_PATH}{sound_to_play}")
            voice_client.play(audio)

    # Проверяем, если канал опустел
    if before.channel is not None and len(
            before.channel.members) == 1:  # 1 — это бот
        voice_client = discord.utils.get(bot.voice_clients,
                                         guild=before.channel.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            print("Канал пуст, бот отключился.")


# Команда: бот подключается к голосовому каналу
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Подключился к голосовому каналу!")
    else:
        await ctx.send("Вы не в голосовом канале!")


# Команда: бот отключается от голосового канала
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Отключился от голосового канала!")
    else:
        await ctx.send("Я не подключён к голосовому каналу!")


# Запуск бота
bot.run(TOKEN)
