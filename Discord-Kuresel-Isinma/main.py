import discord
from os import *
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from random import *
from banaait import *
from tensorflow import *
from time import *
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
            isim = resim.filename
            url = resim.url
            await resim.save(f"./depo/{resim.filename}")
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("keras_model.h5", compile=False)
            # Load the labels
            class_names = open("labels.txt", "r").readlines()
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open(isim).convert("RGB")
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
            if secilen_sinif == "Plastik Pet Sise\n":
                cwrite = (petsisecevap[randint(0,2)])
            elif secilen_sinif == "Plastik Poset\n":
                cwrite = (posetcevap[randint(0,2)])
            elif secilen_sinif == "Metal - Kutu Sise Kavanoz\n":
                cwrite = (kutusisekavanozcevap)
            elif secilen_sinif == "Kagit Siradan Kagit\n":
                cwrite = (kagitcevap)
            elif secilen_sinif == "Kagit Karton Kutu\n":
                cwrite = (kartoncevap[randint(0,2)])
        await ctx.send(cwrite)
    else:
        await ctx.send("Fotoğraf eklemeyi unuttunuz.")

@bot.command()
async def filtre(ctx):
    await ctx.send('''Filtreleme Nedir?
    Filtreleme ya da filtrasyon, içinden yalnızca sıvının geçebileceği bir ortam ekleyerek katıları sıvılardan (sıvılar veya gazlar) ayıran çeşitli mekanik, fiziksel veya biyolojik işlemlerden herhangi biridir.
    Böbrekte, böbrek filtrasyonu, glomerulus içerisindeki kanın filtrasyonu, ardından vücudun homeostazı sürdürmesi için gerekli olan birçok maddenin seçici olarak yeniden emilmesidir.
                   ''')
    await ctx.send('''Fiyatlar(Chat GPT):
    Fabrika baca filtreleri fiyatları, filtre türüne ve özelliklerine göre geniş bir aralıkta değişiklik göstermektedir. Genel olarak, basit filtre sistemleri 500 TL gibi düşük fiyatlardan başlayabilirken, daha karmaşık ve büyük ölçekli sistemlerin fiyatları 100.000 TL'ye kadar çıkabilmektedir.''')
@bot.command()
async def factaboutwaste(ctx):
    factsabtwaste=["Her insan günde **1 kilogram çöp üretiyor.**", "2022 Küresel Atık Endeksi, ABD'yi atık üretimi, yakma, geri dönüşüm ve çöp sahası kullanımı temelinde 25. sıraya yerleştirdi. Ancak, ABD kişi başına en fazla atığı üretiyor.", "Hava kirliliği endeksi en kötü ülke **Hindistan'dır(Bharat).**", "Strafor, doğada yok olma süresi **5000-2 Milyon yıldır.**", "Endekse göre, dünya genelinde her yıl 2,1 milyar ton çöp üretiliyor ve bunların sadece yüzde 16'sı geri dönüştürülüyor. Çöplerin yüzde 46'sı geri dönüştürülemeyecek şekilde atılıyor."]
    await ctx.send(factsabtwaste[randint(0,4)])
@bot.command()
async def wikipedia_geridonusum(ctx):
    await ctx.send('''Site :
                   https://tr.wikipedia.org/wiki/Geri_dönüşüm''')
@bot.command()
async def isik_kirliligi(ctx):
    await ctx.send('''**Işık Kirliliği**
                   
                   Işık kirliliği, ışığın canlıları rahatsız edecek şekilde yanlış kullanılmasıdır.[1] Yanlış yönde, yanlış miktarda, yanlış yerde, aydınlatılması gerekmeyen yerde ışık kullanımı hem ekonomik kayıp hem de rahatsız edici bir durumdur.
                   Işık; doğal ortam ögelerinden biri olup, insanın algılar yoluyla edindiği bilginin %95'i görme duyusuyla edinildiğinden önemlidir. Işık kirliliği farklı şekillerde gerçekleşir; "ışık taşması", "kamaştırıcı ışık", "aşırı ölçüde ışık", "gökyüzü aydınlatmaları", şeklinde gruplandırılır. Güneş, aydınlatma bakımından anlamlı olan tek ışık kaynağıdır. Gündüzü geceye taşıma çabası olan aydınlatma faaliyetleri güvenlik bakımından da önemlidir.
                   ''')
    await ctx.send('''**Ortaya Çıkışı**
                   
                   Işık kirliliği modernleşme ile gelişen kentsel menşeli bir sorundur. Işık kolay çalışmak, daha sağlıklı görmek, güvende hissetmek için kullanılan araçtır. Fakat artan hatalı aydınlatmalar ışık kirliliğine neden olmaktadır. Çevre sorunları içinde eski yıllarda önemsiz bir yere sahip iken, son zamanlarda kirlilik olarak algılanmaktadır. Pek çok ülkede bu kirliliğe karşı dernekler, birlikler ve ulusal komiteler kurulmuştur. Hedef; ışığın gerekli olduğu yerde kullanımı, iyi görme şartları ve gece güvenliğinin sağlanması, enerji tasarrufu ve gökyüzü karanlığının korunmasıdır. ABD'de 'Uluslararası Karanlık Gökyüzü Birliği'nin 68 ülkeden yaklaşık 3000 üyesi bulunur. Japonya'da "Yıldızlı Gökyüzünü Koruma Birliği" kurulmuştur. Türkiye'de 1998'de "Işık kirliliği Çalışma Grubu" faaliyete başlamıştır.
                   ''')
    await ctx.send('''**Nedenleri**
                   
                   Hem çok renkli hem de gereğinden fazla ışık kullanılarak yapılan ışık gösterileri, güvenliği sağlama amacıyla gereğinden fazla ışık kullanımı, özellikle turistik alanlarda ve ticari yerlerde yapılan ışık oyunları, yaşam alanlarından dışarıya taşan ışıklar, sokak, bahçe ve parklarda hatalı aydınlatma çalışmaları ve bina üzerindeki dijital reklam panoları, ışık kirliliğine neden olan başlıca unsurlardır. Bu unsurlar, çevreye olumsuz etkilerde bulunarak hem enerji israfına hem de doğal gece ortamının bozulmasına yol açmaktadır.
                   ''')
    await ctx.send('''**Sonuçları**
                   
                   Işık kirliliği, hayvanlar ve bitkiler üzerinde ciddi olumsuz etkilere yol açmaktadır. Fazla aydınlatma, böceklerin göç ve üreme davranışlarını bozarken, gece aktif sürüngen ve memeliler, özellikle caretta caretta yavruları, yapay ışıklar nedeniyle yönlerini şaşırmaktadır. Kuşlar, göç sırasında ışık kaynaklarına çarpabilir ve ölebilir; 1954'te Georgia'da bu sebeple 50.000 kuş ölmüştür. Balıklar da fazla ışık altında aşırı enerji harcar, bu durum üreme kalitesini düşürür. Bitkilerde fazla ışık, fizyolojik bozukluklara yol açarken, kümes hayvanlarında tüy yolma ve kanibalizmi tetikler. İnsanlarda ise aşırı ışık melatonin salgısını engelleyip uyku sorunlarına, kanser riskine ve göz problemlerine neden olabilir. Ayrıca, ışık kirliliği astronomik gözlemleri engeller ve sürücülerin görüşünü olumsuz etkileyerek trafik kazalarına yol açabilir.
                   
                   Daha fazla bilgi için https://tr.wikipedia.org/wiki/Işık_kirliliği sitesine bakabilirsiniz.''')
@bot.command()
async def su_kirliligi(ctx):
    await ctx.send('''**Su Kirliliği**
    
    Su kirliliği; göl, nehir, okyanus, deniz ve yeraltı suları gibi su barındıran havzalarda görülen kirliliğe verilen genel addır. Her çeşit su kirliliği, kirliliğin bulunduğu havzanın çevresinde veya içinde yaşayan tüm canlılara zarar verdiği gibi, çeşitli türlerin ve biyolojik toplulukların yok olmasına ortam hazırlar. Su kirliliği, içinde zararlı bileşenler barındıran atık suların, yeterli arıtım işleminden geçirilmeksizin havzalara boşaltılmasıyla meydana gelir.''')
    await ctx.send('''**Genel**
    
    Su kirliliği, küresel olarak büyük bir sorun olduğu gibi, birçok ölüm ve salgın hastalık olaylarının nedeni olarak görülmektedir. Günde 14,000 insan doğrudan veya dolaylı olarak su kirliliğinin neden olduğu hastalıklar sonucunda yaşamını yitirmektedir.Buna ek olarak gelişmekte olan ve gelişmiş ülkelerde görülen akut sorunların yanında, bu kirliliğin azaltılması için çalışmalar yapılmaktadır. Bugün dünyada yüzde olarak en çok kirli su havzasına sahip olan ülke Amerika Birleşik Devletleri'dir. Son zamanlarda yapılan ulusal bir araştırmada bu ülkedeki nehir havzalarının yüzde kırk beşi, göl havzalarının yüzde kırk yedisi, liman ve haliçlerin yüzde otuz ikisi kirlenmiş durumdadır.
    Su kirliliği kavramı, genel olarak insanların neden olduğu etkenlerden dolayı oluşan kirliliği tanımlamak için kullanılır. Ancak kimi zamanlarda bazı canlı türlerindeki bozulan dengeler sonucunda da diğer canlılarca su kirliliği oluşabilmektedir. Doğal yoldan oluşan su kirliliğinin nedenleri arasında yanardağlar, aşırı alg üremesi, rüzgarlar ve depremler yer almaktadır. Bunların dışında su kirliliği sınıflandırmalarında farklı ölçütler ve farklı kirlilik çeşitleri bulunmaktadır.''')
    await ctx.send('''Site :
    https://tr.wikipedia.org/wiki/Su_kirliliği''')
@bot.command()
async def toprak_kirliligi(ctx):
    await ctx.send('''**Toprak kirliliği**
                   
                   Toprak kirliliği, katı, sıvı ve radyoaktif artık ve kirleticiler tarafından toprağın fiziksel ve kimyasal özelliklerinin bozulmasıdır. Topraklarda meydana gelecek tüm olumsuz değişimler insan yaşamını kuvvetle etkileyecek güce sahiptir. İnsanların geçmişten gelen ve geçmişte zararları fark edilmemiş olan alışkanlıkları, bu gün toprak kirlenmesi ve bununla birlikte ortaya çıkan yer altı ve yüzey sularının kirlenmesine sebep olmaktadır. Toprak kayaçların parçalanmasıyla oluşur. Oluşumu çok uzun sürede gerçekleşen toprak insan eli ile çok kısa sürede tahrip edilir. Tarımın yapılabilmesi için temel unsur verimli tarım arazileridir yani topraktır. Daha çok ürün elde edebilmek için kullanılan gübreler, tarım ilaçları sağladıkları yararın yanı sıra toprak kirliliğinin önemli sebepleri arasında yer almaktadır. Çevreye gelişigüzel atılan çöpler, evsel atıkların ve sanayi atıklarının arıtılmadan toprağa karıştırılması da toprağı kirleten etkenlerdendir.''')
    await ctx.send('''**Toprak Kirliliği Nedenleri**
                   
                   * Erozyon
                   * Yorulma
                   * Çoraklaşma
                   * Kirlenme
                   
                   Erozyon ile toprağın kayması, yer değiştirmesi bir toprak kirliliği etkenidir. Kentleşme, sanayileşme ve tarımsal faaliyetler toprak kirliliğine neden olan başka faktörlerdir. Yer seçiminin yanlış yapılması, sanayi atık sularından ve fabrika bacalarından çıkan zehirli gaz ve partiküller toprağın kirlenmesine neden olmaktadır. Sadece toprak üzerindeki uygulamalar değil, atmosferden kaynaklanan olumsuzluklar da toprak kirlenmesine ayrı bir etkendir. Tarım topraklarının büyük ölçüde sanayide kullanımı, geriye dönüşü zor olan kirlenmeler meydana getirmektedir. Tarım teknolojisindeki gelişmelerin sonucu mineral gübrelerin, tarım ilaçlarının kullanılması, endüstri atıklarının toprağa sızması veya atılması da toprak kirliliğini doğurur. Ayrıca gelişigüzel çevreye dökülen çöp, ev ve küçük işletme artıkları da toprağı kirletmektedir. Ev atıkları denilen yemek, sebze, kâğıt, plastik, kumaş artıkları, küçük işletme ve endüstri atıkları, ahır, mezbaha, kombina gibi yerlerin atıkları bilhassa yerleşim birimleri ve civarında toprak kirliliği yaratmaktadır.''')
    await ctx.send('''Daha fazla bilgi için https://tr.wikipedia.org/wiki/Toprak_kirliliği sitesine bakabilirsiniz.''')
bot.run(jetonum)