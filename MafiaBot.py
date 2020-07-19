import discord
from discord.ext import commands
import random

TOKEN = 'NzIxMTA4MTUxMjY0MzQ2MTIz.XuPuhg.J83Tn4pFIzCXDd31J_F2I5Wa60g'
bot = commands.Bot(command_prefix='$')
Client = discord.Client()


@bot.command(pass_context=True)  # разрешаем передавать агрументы
#async def help(
       # ctx):  # выводит список всех команд. Внимание!!! При добавлении новой команды опишите что она делает здесь
    #await ctx.send(
        #"newgame 'название канала'- распределить роли между участниками голосового канала (с ролью 'Игрок', "
        #"все участники с ролью 'Ведущий' игнорируются)")


async def newgame(ctx):  # Новое распределение ролей,
    list_of_channels = ctx.message.guild.channels  # Список всех каналов. Здесь на первых двух позициях хранится
    # информация о каналах (например id категории). На 0 позиции - о текстовых, на 1 - о голосовых
    voice_channel_category_id = list_of_channels[1].id  # id категории "голосовые каналы"
    del list_of_channels[0:2]
    channel = None
    for c in list_of_channels:
        if c.category_id == voice_channel_category_id:
            if ctx.message.author in c.members:
                channel = c
    # Проверка на существование голосового канала
    if channel is None:
        await ctx.send("Вы не находитесь ни в одном голосовом канале. Войдите в один из каналов чтобы распределить "
                       "игроков")
    else:
        # Составление списка игроков. Если у пользователя стоят роли "Игрок" и "Ведущий", он не будет участвовать в
        # игре.
        players = []
        for member in channel.members:
            isPlayer = False
            isHeading = False
            for role in member.roles:
                if str(role) == 'Игрок':
                    isPlayer = True
                if str(role) == 'Ведущий':
                    isHeading = True
            if isHeading == False and isPlayer == True:
                players.append(member)
        n = len(players)
        if n < 5:
            await ctx.send("Слишком мало игроков! Нужно от 5 пользователей с ролью 'Игрок'")
        else:
            # Начинаем распределять роли
            players = sorted(players, key=lambda x: x.nick)
            roles = []
            mafia = 'Мафиози'
            don = 'Дон Мафии'
            sheriff = 'Комиссар'
            doctor = 'Доктор'
            citizen = 'Мирный'
            n = len(players)
            if n < 6:
                mafia_amount = 0
            elif n < 10:
                mafia_amount = 1
            elif n < 13:
                mafia_amount = 2
            else:
                mafia_amount = n // 3 - 1
            for x in list(range(0, mafia_amount)):
                roles.append(mafia)
            roles.append(don)
            roles.append(doctor)
            roles.append(sheriff)
            for x in list(range(0, n - mafia_amount - 3)):
                roles.append(citizen)
            cnt = 0
            random.shuffle(roles)
            # Высылаем каждому игроку в лс его роль
            for player in players:
                await ctx.send(player.nick + " - " + roles[cnt])
                if roles[cnt] == citizen:
                    await player.send("Ваша роль - Мирный житель")
                    await player.send(file=discord.File('Мирный.jpg'))
                elif roles[cnt] == mafia:
                    await player.send("Ваша роль - Мафиози")
                    await player.send(file=discord.File('Мафия.jpg'))
                elif roles[cnt] == don:
                    await player.send("Ваша роль - Дон Мафии")
                    await player.send(file=discord.File('Дон.jpg'))
                elif roles[cnt] == doctor:
                    await player.send("Ваша роль - Доктор")
                    await player.send(file=discord.File('Доктор.jpg'))
                elif roles[cnt] == sheriff:
                    await player.send("Ваша роль - Комиссар")
                    await player.send(file=discord.File('Комиссар.jpg'))
                cnt = cnt + 1


bot.run(TOKEN)
