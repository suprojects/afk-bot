START_STRING = {"en": """
Hello! I’m a simple AFK bot to tell others in a group that you’re (A)way (F)rom (K)eyboard whenever they mention you or reply you. Send /help to know how to use me.

You can add me to your group as a normal member to start using me.
""", "ku": """
سڵاو! من بۆتێکی سادەم بۆ ئەوەی بە ئەوانی دیکە بڵێیت کە لەسەرهێڵ نەماویت لەگەڵ هۆکارەکەی ئەگەر دیاریی بکەیت. بۆ زانیاری لەسەر چۆنیەتیی بەکارهێنانم /help بنێرە.

دەتوانیت هەر ئێستا وەک ئەندامێکی ئاسایی زیادی گروپەکەتم بکەیت بۆ دەستکردن بە بەکارهێنانم.
""", "ru": """
Здравствуйте! Я простой бот, который сообщаю другим участникам группы, что вы не в сети, когда они упоминают вас или отвечают вам.  Отправьте /help узнать, как использовать меня.

Вы можете добавить меня в свою группу как обычного участника, чтобы начать пользоваться мной.
""", "uz": """
Salom! Men guruhdagi boshqalarga siz onlayn emasligingizni aytish uchun oddiy botman.  Mendan qanday foydalanishni o‘rganish uchun /help yuboring.

Mendan foydalanishni boshlash uchun meni oddiy guruh a‘zosi sifatida o‘z guruhingizga qo‘shishingiz mumkin.
"""}
START_STRING2 = {"en": "Hey there! I’m alive.",
"uz": "Salom! Men tirikman.",
"ku": "سڵاو! من زیندووم.",
"ru": "Здравствуйте! Я живой."}
START_STRING3 = {"en": "+ Add Me To Your Group +", "ru":
	"+ Добавьте Меня В Свою Группу +",
	"ku": "+ زیادی گروپەکەتم بکە +",
	"uz": "+ Meni Guruhingizga Qo‘shib Qo‘ying +"}
HELP_STRING = {"en": """
If you send this in a group which I am in before going AFK:
	<pre>/afk [reason]</pre>

And then someone mentions or replies you, they’ll be replied like this:
	{} is AFK!
	
	Reason:
	[reason]
""", "ru": """
Если вы отправите это в группу, в которой я состою:
	/afk [причина]

А потом кто-то упомянет или ответит вам, ему ответят так:
	{} сейчас в автономном режиме!
	
	Причина:
	[причина]
""", "uz": """
Agar siz buni men bo‘lgan guruhga yuborsangiz:
	/afk [sabab]
	
Va keyin kimdir sizga qo‘ng‘iroq qiladi, ularga shunday javob berishadi:
	{} hozirda oflayn rejimda!
	
	Sabab:
	[sabab]
""", "ku": """
ئەگەر لە گروپێک کە منی لێم ئەمە بنێریت:
/afk [هۆکار]

و دواتر ئەگەر کەسێک وەڵامت بداتەوە یان تاگت بکات، ئاوها وەڵام دەدرێتەوە:
بەکارهێنەر {} لەسەرهێڵ نییە!

هۆکار:
[هۆکار]
"""}
HELP_STRING2 = {"en": "Click on the button below to get help in PM!", "uz": "Shaxsiy yordam olish uchun quyidagi tugmani bosing!", "ru": "Нажмите кнопку ниже, чтобы получить помощь наедине!", "ku": "ئەو دوگمەیەی خوارەوە بکە بۆ ئەوەی لە تب یارمەتیت بۆ بنێرم!"}
HELP_STRING3 = {"en": "Help", "ku": "یارمەتی", "ru": "Помогите", "uz": "Yordam"}
LANG_STRING = {"en": "Language", "ku": "زمان", "ru": "Язык", "uz": "Til"}

NOW_AFK = {"en": "{} is now AFK!", "ku": "بەکارهێنەر {} لەسەرهێڵ نەما!", "ru": "{} сейчас в автономном режиме!", "uz": "{} hozirda oflayn rejimda!"}

AFK = {"en": "{} is AFK!", "ku": "بەکاەهێنەر {} لەسەرهێڵ نییە!", "ru": "{} сейчас в автономном режиме!", "uz": "{} hozirda oflayn rejimda!"}

AFK2 = {"en": AFK["en"] + "\n\nReason:\n{}", "ku": AFK["ku"] + "\n\nهۆکار:\n{}", "ru": AFK["ru"] + "\n\nПричина:\n{}", "uz": AFK["uz"] + "\n\nSabab:\n{}"}

NOL_AFK = {"en": "{} is no longer AFK!", "ku": "بەکاەهێنەر {} گەڕایەوە سەرهێڵ!", "ru": "{} снова в сети!", "uz": "{} yana onlayn!"}
