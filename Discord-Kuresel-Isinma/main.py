import discord
from os import *
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from random import *
from banaait import *
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
@bot.command()
async def ne_yapmaliyim(ctx):
    petsisecevap = ["Yakınlarda geri dönüşüm çöp kutuları varsa plastik olana at.", "Sahildeysen denize atma, Suyun altındaki canlılara zarar veriyorsun! Onun yerine plastik geri dönüşüm çöp kutusuna atabilirsin.", "Bence onları topla, sonra plastik çöp kutusuna atarsın."]
    posetcevap = ["İçi boşsa öbür çöpleri toplamak için kullanabilirsin. $copler_hangi_kutuya_atilacak yazarak gruplarına göre çöpü atabilirsin.", "Eğer içi doluysa, $copler_hangi_kutuya_atilacak yazarak gruplarına göre çöpü atabilirsin.", "Tek bu çöp varsa, plastik geri dönüşüm kutusuna at. Fakat başka var olabilir."]
    kutusisekavanozcevap = "Metal geri dönüşüm kutusuna atabilirsin."
    kagitcevap = "Kağıt geri dönüşüm çöp kutusuna atabilirsin."
    kartoncevap = ["Karton kutu boşsa öbür çöpleri toplamak için kullanabilirsin, $copler_hangi_kutuya_atilacak yazarak gruplarına göre çöpü atabilirsin.", "Eğer içi doluysa, $copler_hangi_kutuya_atilacak yazarak gruplarına göre çöpü atabilirsin.", "Kağıt geri dönüşüm çöp kutusuna atabilirsin."]
    if ctx.message.attachments:
        for resim in ctx.message.attachments:
            pr_ismi = resim.filename
            pr_url = resim.url
            await resim.save(f"./{resim.filename}")
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("keras_model.h5", compile=False)
            # Load the labels
            class_names = open("labels.txt", "r").readlines()
            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            # Replace this with the path to your image
            image = Image.open(pr_ismi).convert("RGB")
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            # turnthe image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            # Load the image into the array
            data[0] = normalized_image_array
            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            secilen_sinif = class_name[2:]
            if secilen_sinif == "Plastik - Pet Sise\n":
                cwrite = (petsisecevap[randint(0,2)])
            elif secilen_sinif == "Plastik - Poset\n":
                cwrite = (posetcevap[randint(0,2)])
            elif secilen_sinif == "Metal - Kutu Sise / Kavanoz\n":
                cwrite = (kutusisekavanozcevap)
            elif secilen_sinif == "Kagit - Siradan Kagit\n":
                cwrite = (kagitcevap)
            elif secilen_sinif == "Kagit - Karton Kutu\n":
                cwrite = (kartoncevap[randint(0,2)])
        await ctx.send(cwrite)
    else:
        await ctx.send("Fotoğraf eklemeyi unuttunuz.")

@bot.command()
async def copler_hangi_kutuya_atilacak(ctx):
    global jetonum
    with open(f'images/image.png', 'rb') as f:
        # Dönüştürülen Discord kütüphane dosyasını bu değişkende saklayalım!
        picture = discord.File(f)
   # Daha sonra bu dosyayı bir parametre olarak gönderebiliriz!
    await ctx.send(file=picture)
bot.run(jetonum)