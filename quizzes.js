/* =============================================================
   SEC2021 — quizzes.js
   مفتاح كل مصفوفة = id الموديول في content.js
   correct = موضع الإجابة الصحيحة (يبدأ من 0). المواضع موزّعة عمداً.
   لإضافة سؤال: أضف كائناً بالشكل نفسه إلى مصفوفة الموديول.
   ============================================================= */

const QUIZZES = {

  m1: [
    {
      q: { ar: "ما الذي يميّز الحاسب عن الآلة الحاسبة أساساً؟", en: "What mainly makes a computer different from a calculator?" },
      options: [
        { ar: "أنه أسرع في الجمع والطرح", en: "It is faster at adding and subtracting" },
        { ar: "أن شاشته أكبر وألوانه أوضح", en: "Its screen is bigger with clearer colours" },
        { ar: "أنه يخزّن برنامجاً كاملاً وينفّذه وحده، ويتغيّر عمله بتغيير البرنامج", en: "It stores a whole program and runs it on its own, and its work changes when the program changes" },
        { ar: "أنه يتصل بالإنترنت", en: "It connects to the internet" }
      ],
      correct: 2,
      why: { ar: "السرعة والشاشة والاتصال صفات ثانوية. الجوهر هو «التعليمات المخزّنة»: الجهاز نفسه يكتب خطاباً ويحسب رواتب دون أي تغيير مادي فيه.", en: "Speed, screen, and connectivity are secondary. The essence is \"stored instructions\": the same machine writes a letter and calculates salaries with no physical change." }
    },
    {
      q: { ar: "رتّب دورة المعالجة ترتيباً صحيحاً.", en: "Put the processing cycle in the right order." },
      options: [
        { ar: "إدخال ← معالجة ← إخراج ← تخزين", en: "Input, processing, output, storage" },
        { ar: "معالجة ← إدخال ← تخزين ← إخراج", en: "Processing, input, storage, output" },
        { ar: "تخزين ← إخراج ← إدخال ← معالجة", en: "Storage, output, input, processing" },
        { ar: "إدخال ← تخزين ← إخراج ← معالجة", en: "Input, storage, output, processing" }
      ],
      correct: 0,
      why: { ar: "تدخل البيانات أولاً، ثم تُعالَج، ثم تظهر النتيجة، ثم تُحفَظ لتبقى بعد إطفاء الجهاز.", en: "Data enters first, is then processed, the result is shown, and finally it is saved so it survives shutdown." }
    },
    {
      q: { ar: "«درجة حرارة المريض خالد اليوم 38.5 وهي مرتفعة» — هذه العبارة مثال على:", en: "\"Patient Khalid's temperature today is 38.5, which is high\" — this is an example of:" },
      options: [
        { ar: "بيانات خام فقط", en: "Raw data only" },
        { ar: "برنامج", en: "A program" },
        { ar: "عتاد", en: "Hardware" },
        { ar: "معلومات", en: "Information" }
      ],
      correct: 3,
      why: { ar: "الرقم 38.5 وحده بيانات خام. وحين ارتبط بمريض وتاريخ وتفسير صار معلومة يُتّخذ عليها قرار.", en: "The number 38.5 alone is raw data. Once linked to a patient, a date, and an interpretation, it becomes information you can act on." }
    },
    {
      q: { ar: "لماذا يستخدم الحاسب النظام الثنائي (0 و1)؟", en: "Why does a computer use the binary system (0 and 1)?" },
      options: [
        { ar: "لأن الرياضيات لا تعرف غير هذين الرقمين", en: "Because mathematics knows only these two digits" },
        { ar: "لأن الدوائر الإلكترونية تميّز بسهولة وموثوقية بين حالتين: مرور التيار أو عدمه", en: "Because electronic circuits reliably tell two states apart: current flowing or not" },
        { ar: "لأنه أسرع في الطباعة على الشاشة", en: "Because it prints faster on screen" },
        { ar: "لأن المبرمجين يفضّلون الأرقام الصغيرة", en: "Because programmers prefer small numbers" }
      ],
      correct: 1,
      why: { ar: "الصفر والواحد ترجمة مباشرة لحالتين كهربائيتين يسهل تمييزهما بدقة وبكلفة منخفضة؛ فالسبب هندسي لا رياضي.", en: "Zero and one map directly onto two electrical states that are easy to tell apart accurately and cheaply. The reason is engineering, not mathematics." }
    },
    {
      q: { ar: "ملف حجمه 2 GB. أي العبارات صحيح؟", en: "A file is 2 GB in size. Which statement is correct?" },
      options: [
        { ar: "أصغر من ملف حجمه 500 MB", en: "It is smaller than a 500 MB file" },
        { ar: "يساوي تقريباً 2 KB", en: "It is about the same as 2 KB" },
        { ar: "أكبر من 1 TB", en: "It is larger than 1 TB" },
        { ar: "أكبر من ملف حجمه 500 MB بنحو أربع مرات", en: "It is about four times larger than a 500 MB file" }
      ],
      correct: 3,
      why: { ar: "الجيجابايت الواحد ≈ 1024 ميجابايت، فـ 2 GB ≈ 2048 MB، أي نحو أربعة أضعاف 500 MB. والتيرابايت أكبر من الجيجابايت لا أصغر.", en: "One gigabyte is about 1024 megabytes, so 2 GB is about 2048 MB — roughly four times 500 MB. And a terabyte is larger than a gigabyte, not smaller." }
    },
    {
      q: { ar: "جهاز قياس السكر المنزلي من أي نوع من الحواسيب؟", en: "A home glucose meter is which type of computer?" },
      options: [
        { ar: "حاسب مدمج", en: "An embedded computer" },
        { ar: "خادم", en: "A server" },
        { ar: "حاسب فائق", en: "A supercomputer" },
        { ar: "ليس حاسباً بأي معنى", en: "Not a computer in any sense" }
      ],
      correct: 0,
      why: { ar: "هو حاسب صغير داخل جهاز آخر يؤدي مهمة واحدة محددة، وهذا تعريف الحاسب المدمج. الخادم يخدم مستخدمين كثيرين عبر الشبكة.", en: "It is a small computer inside another device doing one specific job, which is the definition of an embedded computer. A server serves many users over a network." }
    }
  ],

  m2: [
    {
      q: { ar: "ما وظيفة اللوحة الأم؟", en: "What does the motherboard do?" },
      options: [
        { ar: "تنفيذ تعليمات البرامج", en: "Carry out program instructions" },
        { ar: "توصيل القطع ببعضها ونقل البيانات والكهرباء بينها", en: "Connect the parts and move data and power between them" },
        { ar: "تخزين الملفات بشكل دائم", en: "Store files permanently" },
        { ar: "تبريد المعالج", en: "Cool the processor" }
      ],
      correct: 1,
      why: { ar: "تنفيذ التعليمات وظيفة المعالج، والتخزين الدائم وظيفة القرص. اللوحة الأم هي الأساس والطرق التي تربط الجميع.", en: "Carrying out instructions is the processor's job and permanent storage is the disk's. The motherboard is the base and the roads linking everything." }
    },
    {
      q: { ar: "ما الفرق الجوهري بين الذاكرة RAM والتخزين؟", en: "What is the essential difference between RAM and storage?" },
      options: [
        { ar: "الذاكرة أغلى من التخزين دائماً", en: "Memory always costs more than storage" },
        { ar: "التخزين أسرع من الذاكرة", en: "Storage is faster than memory" },
        { ar: "الذاكرة داخل الصندوق والتخزين خارجه", en: "Memory is inside the case and storage is outside" },
        { ar: "الذاكرة مؤقتة تُمحى بانقطاع الكهرباء، والتخزين دائم يبقى", en: "Memory is temporary and erased when power is lost; storage is permanent" }
      ],
      correct: 3,
      why: { ar: "الفرق في الدوام لا في السعر ولا الموقع. ولهذا تخسر العمل غير المحفوظ عند انطفاء مفاجئ: كان في الذاكرة ولم يصل إلى التخزين.", en: "The difference is permanence, not price or location. That is why you lose unsaved work in a sudden shutdown: it was in memory and never reached storage." }
    },
    {
      q: { ar: "موظف يفتح نظام العمل وإكسل وعشرين تبويباً فيبدأ الجهاز بالتجمّد القصير. ما السبب الأرجح؟", en: "An employee opens the work system, Excel, and twenty tabs, and the machine starts freezing briefly. What is the likely cause?" },
      options: [
        { ar: "امتلاء الذاكرة RAM", en: "RAM is full" },
        { ar: "امتلاء سلة المحذوفات", en: "The recycle bin is full" },
        { ar: "ضعف دقة الشاشة", en: "Low screen resolution" },
        { ar: "عدم وجود بطاقة رسوميات", en: "No graphics card" }
      ],
      correct: 0,
      why: { ar: "كثرة البرامج المفتوحة تستهلك الذاكرة، فيلجأ النظام إلى القرص كذاكرة احتياطية وهو أبطأ بكثير، فيظهر التلعثم.", en: "Many open programs consume memory, so the system falls back on the disk as backup memory, which is far slower, and you feel the stutter." }
    },
    {
      q: { ar: "أي ترقية تعطي عادةً أكبر فرق في سرعة جهاز قديم مقابل أقل مبلغ؟", en: "Which upgrade usually gives the biggest speed gain on an old machine for the least money?" },
      options: [
        { ar: "شاشة بدقة أعلى", en: "A higher-resolution screen" },
        { ar: "لوحة مفاتيح جديدة", en: "A new keyboard" },
        { ar: "استبدال قرص HDD بقرص SSD", en: "Replacing an HDD with an SSD" },
        { ar: "تغيير مزوّد الطاقة", en: "Changing the power supply" }
      ],
      correct: 2,
      why: { ar: "القرص التقليدي يعتمد أجزاء متحركة وهو أبطأ حلقة في الجهاز عادة. الانتقال إلى SSD يظهر أثره فوراً في الإقلاع وفتح البرامج.", en: "A traditional disk relies on moving parts and is usually the slowest link. Moving to an SSD shows its effect immediately at startup and when opening programs." }
    },
    {
      q: { ar: "لماذا يحتاج المعالج إلى تبريد؟", en: "Why does a processor need cooling?" },
      options: [
        { ar: "لمنع تشوّش الصورة على الشاشة", en: "To stop the picture from distorting on screen" },
        { ar: "لأن الذاكرة تسخن أكثر منه", en: "Because memory gets hotter than it does" },
        { ar: "لتقليل استهلاك الكهرباء فقط", en: "Only to reduce electricity use" },
        { ar: "لأن ملايين العمليات تنتج حرارة، وتجاوز الحد يجعله يبطئ نفسه حمايةً", en: "Because millions of operations produce heat, and beyond a limit it slows itself down to stay safe" }
      ],
      correct: 3,
      why: { ar: "الحرارة نتيجة طبيعية للعمل. وعند تجاوز الحد الآمن يخفّض المعالج أداءه تلقائياً، وهذا سبب شائع لبطء الأجهزة المتّسخة بالغبار.", en: "Heat is a natural result of work. Past a safe limit the processor lowers its own performance, a common reason dusty machines feel slow." }
    },
    {
      q: { ar: "في التسمية Core i5-1335U ماذا تعني i5؟", en: "In the name Core i5-1335U, what does i5 mean?" },
      options: [
        { ar: "عدد الأنوية", en: "The number of cores" },
        { ar: "فئة المعالج داخل عائلة إنتل", en: "The processor tier within Intel's family" },
        { ar: "سعة الذاكرة بالجيجابايت", en: "Memory capacity in gigabytes" },
        { ar: "سنة الصنع", en: "The year it was made" }
      ],
      correct: 1,
      why: { ar: "i5 فئة، والرقم الذي يليها يدل على الجيل. ولهذا قد يتفوّق i5 حديث على i7 قديم جداً، فالمقارنة تكون بالفئة والجيل معاً.", en: "i5 is a tier and the number after it indicates the generation. That is why a recent i5 can beat a very old i7: compare tier and generation together." }
    },
    {
      q: { ar: "أي المجموعات كلها أجهزة إدخال؟", en: "Which group contains only input devices?" },
      options: [
        { ar: "الطابعة، الشاشة، السمّاعات", en: "Printer, monitor, speakers" },
        { ar: "الشاشة، الميكروفون، الطابعة", en: "Monitor, microphone, printer" },
        { ar: "الماسح الضوئي، قارئ الباركود، الميكروفون", en: "Scanner, barcode reader, microphone" },
        { ar: "السمّاعات، لوحة المفاتيح، الشاشة", en: "Speakers, keyboard, monitor" }
      ],
      correct: 2,
      why: { ar: "الطابعة والشاشة والسمّاعات أجهزة إخراج. أما الماسح والقارئ والميكروفون فتُدخل بيانات إلى الجهاز.", en: "Printer, monitor, and speakers are output devices. Scanner, reader, and microphone all bring data into the machine." }
    },
    {
      q: { ar: "شاشة اللمس تُصنَّف على أنها:", en: "A touch screen is classified as:" },
      options: [
        { ar: "جهاز إدخال وإخراج معاً", en: "Both an input and an output device" },
        { ar: "جهاز إدخال فقط", en: "An input device only" },
        { ar: "جهاز إخراج فقط", en: "An output device only" },
        { ar: "وحدة تخزين", en: "A storage unit" }
      ],
      correct: 0,
      why: { ar: "تعرض النتيجة (إخراج) وتستقبل لمسة المستخدم (إدخال)، مثل الطابعة متعددة الوظائف والقرص الخارجي.", en: "It displays results (output) and receives the user's touch (input), like an all-in-one printer or an external drive." }
    },
    {
      q: { ar: "طالب ميزانيته محدودة ويحتاج جهازاً للدراسة والمكتب. أي مواصفة يُفضَّل ألا يضحّي بها؟", en: "A student on a limited budget needs a machine for study and office work. Which specification should they avoid compromising on?" },
      options: [
        { ar: "بطاقة رسوميات منفصلة قوية", en: "A strong dedicated graphics card" },
        { ar: "معالج من الفئة i9", en: "An i9-tier processor" },
        { ar: "ذاكرة 64 GB", en: "64 GB of memory" },
        { ar: "تخزين SSD بدل HDD", en: "SSD storage instead of HDD" }
      ],
      correct: 3,
      why: { ar: "المواصفات الثلاث الأخرى فائضة عن حاجة الدراسة المكتبية وترفع السعر بلا فائدة محسوسة، بينما يظهر أثر SSD في كل استخدام يومي.", en: "The other three exceed what office study needs and raise the price with no felt benefit, while an SSD shows its effect in every daily task." }
    },
    {
      q: { ar: "ما وظيفة برنامج التعريف Driver؟", en: "What does a driver do?" },
      options: [
        { ar: "يحمي الجهاز من الفيروسات", en: "Protects the machine from viruses" },
        { ar: "يشرح لنظام التشغيل كيف يتعامل مع قطعة معيّنة", en: "Tells the operating system how to work with a specific part" },
        { ar: "يزيد سعة القرص الصلب", en: "Increases hard disk capacity" },
        { ar: "يبرّد المعالج برمجياً", en: "Cools the processor through software" }
      ],
      correct: 1,
      why: { ar: "ولهذا فالطابعة الجديدة التي لا تعمل يكون سببها غالباً غياب برنامج التعريف المناسب لا عطلاً في الطابعة نفسها.", en: "That is why a new printer that does not work usually has a missing driver rather than a hardware fault." }
    },
    {
      q: { ar: "أي مما يلي يُصنَّف برمجيات ثابتة Firmware؟", en: "Which of the following is classified as firmware?" },
      options: [
        { ar: "BIOS/UEFI المخزّن على اللوحة الأم", en: "The BIOS/UEFI stored on the motherboard" },
        { ar: "برنامج إكسل", en: "Excel" },
        { ar: "نظام ويندوز 11", en: "Windows 11" },
        { ar: "متصفح الإنترنت", en: "The web browser" }
      ],
      correct: 0,
      why: { ar: "إكسل والمتصفح برمجيات تطبيقية، وويندوز برمجيات نظام. أما البيوس فبرنامج صغير مخزّن داخل قطعة عتاد ليشغّلها.", en: "Excel and the browser are application software and Windows is system software. The BIOS is a small program stored inside a hardware part to run it." }
    },
    {
      q: { ar: "معالج A تردده 3.5 GHz من جيل قديم جداً، ومعالج B تردده 2.5 GHz من جيل حديث. ما الاستنتاج الصحيح؟", en: "Processor A runs at 3.5 GHz from a very old generation; processor B runs at 2.5 GHz from a recent one. What is the right conclusion?" },
      options: [
        { ar: "A أسرع حتماً لأن رقمه أكبر", en: "A is certainly faster because its number is bigger" },
        { ar: "التردد لا معنى له إطلاقاً", en: "Clock speed means nothing at all" },
        { ar: "قد يتفوّق B لأن الجيل الأحدث ينجز شغلاً أكبر في الدورة الواحدة", en: "B may well win, because a newer generation does more work per cycle" },
        { ar: "لا يمكن المقارنة إلا بمعرفة لون الجهاز وحجمه", en: "No comparison is possible without knowing the machine's colour and size" }
      ],
      correct: 2,
      why: { ar: "التردد مؤشر واحد فقط. المقارنة الصحيحة تجمع الجيل والفئة وعدد الأنوية، لا رقماً منفرداً.", en: "Clock speed is only one indicator. A correct comparison combines generation, tier, and core count, not a single number." }
    },
    {
      q: { ar: "ما وحدة التخزين ذات السعة الأصغر بين هذه؟", en: "Which of these had the smallest capacity?" },
      options: [
        { ar: "قرص DVD", en: "A DVD" },
        { ar: "القرص المرن Floppy Disk", en: "A floppy disk" },
        { ar: "قرص SSD سعة 512 GB", en: "A 512 GB SSD" },
        { ar: "قرص CD-ROM", en: "A CD-ROM" }
      ],
      correct: 1,
      why: { ar: "القرص المرن نحو 1.44 MB فقط، والـCD نحو 700 MB، والـDVD نحو 4.7 GB. الفارق بين أول القائمة وآخرها مئات الآلاف من الأضعاف.", en: "A floppy held about 1.44 MB, a CD about 700 MB, and a DVD about 4.7 GB. The gap from first to last is hundreds of thousands of times." }
    },
    {
      q: { ar: "اشترى موظف طابعة شبكية ثم اكتشف أن جهازه لا يملك منفذ Ethernet. أين تقع المشكلة؟", en: "An employee bought a network printer, then found his machine has no Ethernet port. Where is the problem?" },
      options: [
        { ar: "في ضعف المعالج", en: "A weak processor" },
        { ar: "في قلّة الذاكرة", en: "Not enough memory" },
        { ar: "في نوع نظام التشغيل", en: "The type of operating system" },
        { ar: "في المنافذ المتاحة على الجهاز", en: "The ports available on the machine" }
      ],
      correct: 3,
      why: { ar: "المنافذ مسألة توصيل لا قوة. قراءة المنافذ ضمن بطاقة المواصفات قبل الشراء تمنع هذا النوع من المفاجآت.", en: "Ports are a matter of connection, not power. Reading the ports on the specification sheet before buying prevents this kind of surprise." }
    }
  ],

  m3: [
    {
      q: { ar: "أي وصف يطابق وظيفة نظام التشغيل؟", en: "Which description matches what an operating system does?" },
      options: [
        { ar: "برنامج لكتابة المستندات وتنسيقها", en: "A program for writing and formatting documents" },
        { ar: "قطعة عتاد داخل الصندوق", en: "A hardware part inside the case" },
        { ar: "موقع إنترنت لتحميل البرامج", en: "A website for downloading programs" },
        { ar: "برنامج يدير موارد الجهاز ويقف وسيطاً بين العتاد والبرامج والمستخدم", en: "A program that manages the machine's resources between hardware, programs, and the user" }
      ],
      correct: 3,
      why: { ar: "نظام التشغيل برمجيات نظام لا تطبيقات ولا عتاد. وبدونه لا تستطيع البرامج مخاطبة العتاد مباشرة.", en: "An operating system is system software, not an application and not hardware. Without it, programs cannot address hardware directly." }
    },
    {
      q: { ar: "أي هذه ليست من وظائف نظام التشغيل الخمس؟", en: "Which of these is NOT one of the five operating system jobs?" },
      options: [
        { ar: "إدارة الذاكرة", en: "Memory management" },
        { ar: "تصميم الدوائر الإلكترونية داخل المعالج", en: "Designing the electronic circuits inside the processor" },
        { ar: "إدارة الملفات", en: "File management" },
        { ar: "إدارة الأجهزة الطرفية", en: "Device management" }
      ],
      correct: 1,
      why: { ar: "تصميم الدوائر عمل تصنيعي في المصنع، لا وظيفة برمجية. الوظائف الخمس: معالج وذاكرة وملفات وأجهزة وأمن ومستخدمون.", en: "Circuit design is manufacturing work, not a software job. The five jobs are processor, memory, files, devices, and security with users." }
    },
    {
      q: { ar: "ما الذي تغيّر جوهرياً بين MS-DOS وWindows 95؟", en: "What essentially changed between MS-DOS and Windows 95?" },
      options: [
        { ar: "اختفت الحاجة إلى المعالج", en: "The processor was no longer needed" },
        { ar: "صار النظام مفتوح المصدر", en: "The system became open source" },
        { ar: "انتقل التعامل من كتابة أوامر نصية إلى واجهة رسومية بالنوافذ والفأرة", en: "Interaction moved from typed commands to a graphical interface with windows and a mouse" },
        { ar: "ألغيت الملفات والمجلدات", en: "Files and folders were abolished" }
      ],
      correct: 2,
      why: { ar: "نقلة الواجهة الرسومية جعلت الحاسب جهازاً لعامة الناس. أما الملفات والمعالج فباقية، وويندوز ما زال مغلق المصدر.", en: "The graphical interface made the computer a device for everyone. Files and the processor remained, and Windows is still closed source." }
    },
    {
      q: { ar: "ملف اسمه patients_2026.csv — بأي برنامج يُفتح عادة؟", en: "A file named patients_2026.csv — which program usually opens it?" },
      options: [
        { ar: "إكسل أو برامج تحليل البيانات", en: "Excel or data analysis tools" },
        { ar: "باوربوينت", en: "PowerPoint" },
        { ar: "مشغّل الفيديو", en: "A video player" },
        { ar: "برنامج تحرير الصور", en: "A photo editor" }
      ],
      correct: 0,
      why: { ar: "الامتداد بعد النقطة يحدد نوع الملف والبرنامج المناسب له، و.csv صيغة بيانات جدولية نصية.", en: "The extension after the dot decides the file type and the right program, and .csv is a text-based tabular data format." }
    },
    {
      q: { ar: "ما العلاقة بين نواة لينكس والتوزيعات مثل Ubuntu؟", en: "What is the relationship between the Linux kernel and distributions such as Ubuntu?" },
      options: [
        { ar: "التوزيعات أنظمة منفصلة لا علاقة لها بلينكس", en: "Distributions are separate systems unrelated to Linux" },
        { ar: "النواة نسخة تجارية من أوبونتو", en: "The kernel is a commercial version of Ubuntu" },
        { ar: "النواة أساس مشترك، والتوزيعات أنظمة كاملة مبنية عليه بواجهات وبرامج مختلفة", en: "The kernel is a shared base, and distributions are complete systems built on it with different interfaces and programs" },
        { ar: "لا يمكن استخدام النواة إلا داخل ويندوز", en: "The kernel can only be used inside Windows" }
      ],
      correct: 2,
      why: { ar: "كالمحرّك الواحد الذي تُبنى حوله سيارات مختلفة: الأساس واحد والتجربة تختلف بحسب التوزيعة.", en: "Like one engine with different cars built around it: the base is the same and the experience differs by distribution." }
    },
    {
      q: { ar: "أي العبارات صحيحة عن البرمجيات مفتوحة المصدر؟", en: "Which statement about open source software is correct?" },
      options: [
        { ar: "شفرتها مخفية مثل ويندوز تماماً", en: "Its code is hidden, exactly like Windows" },
        { ar: "شفرتها متاحة للاطلاع والتعديل وفق شروط ترخيص محددة", en: "Its code is available to read and modify under specific licence terms" },
        { ar: "لا يجوز استخدامها في أي جهة حكومية", en: "It may not be used in any government body" },
        { ar: "تعني أنها بلا حقوق ولا شروط إطلاقاً", en: "It means there are no rights or terms at all" }
      ],
      correct: 1,
      why: { ar: "«مفتوح» يعني شفافاً ومتاحاً وفق ترخيص، لا متروكاً بلا شروط. وبعض التراخيص تشترط نشر تعديلاتك بالرخصة نفسها.", en: "\"Open\" means transparent and available under a licence, not abandoned without terms. Some licences require you to publish your changes under the same licence." }
    },
    {
      q: { ar: "موظف سجّل دخوله بحسابه بنجاح، ثم مُنع من فتح ملف مريض في قسم آخر. ما تفسير ذلك؟", en: "An employee signed in successfully with their account, then was blocked from opening a patient file in another department. Why?" },
      options: [
        { ar: "كلمة المرور خاطئة", en: "The password is wrong" },
        { ar: "نظام التشغيل معطّل", en: "The operating system is faulty" },
        { ar: "الملف غير موجود أصلاً", en: "The file does not exist" },
        { ar: "نجحت المصادقة لكن الصلاحيات لا تخوّله الوصول إلى هذا المورد", en: "Authentication succeeded, but his permissions do not authorise access to that resource" }
      ],
      correct: 3,
      why: { ar: "المصادقة تجيب «من أنت؟» وقد نجحت بدليل الدخول. والتخويل يجيب «وماذا يحق لك؟» وهو ما منعه. الدخول إلى النظام لا يعني حق الاطلاع على كل ملف فيه.", en: "Authentication answers \"who are you?\" and it succeeded, since he signed in. Authorization answers \"what may you do?\" and that is what blocked him. Signing in does not grant the right to every file." }
    },
    {
      q: { ar: "طلب موظف في قسم المواعيد صلاحية «مسؤول نظام» ليسهّل عمله اليومي. ما التوصية المهنية؟", en: "An employee in the appointments department asked for administrator rights to make daily work easier. What is the professional recommendation?" },
      options: [
        { ar: "منحه أقل صلاحية تكفي لإنجاز مهامه، عملاً بمبدأ الحد الأدنى من الصلاحيات", en: "Grant the smallest permission that covers his tasks, following the principle of least privilege" },
        { ar: "منحه الصلاحية لأنها تختصر الوقت", en: "Grant it, because it saves time" },
        { ar: "منحه حساب زميله المسؤول ليستخدمه عند الحاجة", en: "Give him his administrator colleague's account to use when needed" },
        { ar: "إلغاء حسابه واستخدام حساب مشترك للقسم", en: "Delete his account and use one shared department account" }
      ],
      correct: 0,
      why: { ar: "الصلاحية الزائدة تفتح باب خطأ أو تسريب لا رجعة فيه. ومشاركة الحساب أو استخدام حساب مشترك تُلغي إمكانية معرفة من فعل ماذا في سجلات النظام.", en: "Excess permission opens the door to an irreversible error or leak. Sharing an account, or using one shared account, destroys any way of knowing from the logs who did what." }
    }
  ],

  m4: [
    {
      q: { ar: "قسم يريد تسجيل بيانات 2000 مراجع مع زياراتهم المتكررة ويشترك في التسجيل ثلاثة موظفين. أي أداة أنسب؟", en: "A department wants to record 2000 visitors with their repeated visits, with three staff entering data. Which tool fits best?" },
      options: [
        { ar: "Word", en: "Word" },
        { ar: "Access", en: "Access" },
        { ar: "PowerPoint", en: "PowerPoint" },
        { ar: "Excel", en: "Excel" }
      ],
      correct: 1,
      why: { ar: "سجلات كثيرة ومترابطة ويشترك فيها أكثر من مستخدم = قاعدة بيانات. استخدام Excel هنا يؤدي إلى تكرار البيانات وتعارض النسخ.", en: "Many linked records shared by several users means a database. Using Excel here leads to duplicated data and conflicting copies." }
    },
    {
      q: { ar: "ما الفائدة العملية الأهم لاستخدام الأنماط (Styles) في Word؟", en: "What is the most useful practical benefit of using styles in Word?" },
      options: [
        { ar: "تصغير حجم الملف", en: "Reducing the file size" },
        { ar: "منع الآخرين من تعديل المستند", en: "Stopping others from editing the document" },
        { ar: "تسريع الطباعة", en: "Making printing faster" },
        { ar: "تغيير شكل كل العناوين مرة واحدة، وتوليد فهرس المحتويات آلياً", en: "Changing every heading at once, and generating the table of contents automatically" }
      ],
      correct: 3,
      why: { ar: "النمط تنسيق محفوظ باسم؛ تعديله يسري على كل ما طُبِّق عليه. ومن يستخدمه يكسب الفهرس التلقائي وجزء التنقل مجاناً.", en: "A style is a named saved format, and editing it applies everywhere. Using it also earns the automatic table of contents and navigation pane for free." }
    },
    {
      q: { ar: "ما الفرق بين الصيغة والدالة في Excel؟", en: "What is the difference between a formula and a function in Excel?" },
      options: [
        { ar: "كل ما يبدأ بعلامة يساوي صيغة، والدالة صيغة جاهزة لها اسم مثل SUM", en: "Anything starting with = is a formula; a function is a named ready-made formula such as SUM" },
        { ar: "الصيغة للأرقام والدالة للنصوص فقط", en: "Formulas are for numbers and functions are for text only" },
        { ar: "لا فرق بينهما إطلاقاً", en: "There is no difference at all" },
        { ar: "الدالة تُكتب يدوياً والصيغة تُدرج من القائمة", en: "A function is typed by hand and a formula is inserted from a menu" }
      ],
      correct: 0,
      why: { ar: "‎=B2*3 صيغة وليست دالة، و=SUM(B2:B40) صيغة ودالة معاً. فكل دالة صيغة، وليست كل صيغة دالة.", en: "=B2*3 is a formula but not a function, while =SUM(B2:B40) is both. Every function is a formula; not every formula is a function." }
    },
    {
      q: { ar: "كتبت في الخلية C2 الصيغة ‎=B2*$D$1 ثم سحبتها إلى C3. ماذا تصير؟", en: "You typed =B2*$D$1 in cell C2, then dragged it to C3. What does it become?" },
      options: [
        { ar: "=B2*$D$1", en: "=B2*$D$1" },
        { ar: "=B3*$D$2", en: "=B3*$D$2" },
        { ar: "=B3*$D$1", en: "=B3*$D$1" },
        { ar: "=B2*$D$2", en: "=B2*$D$2" }
      ],
      correct: 2,
      why: { ar: "المرجع النسبي B2 يتحرك مع السحب فيصير B3، والمرجع المطلق ‎$D$1 مثبّت بعلامتي الدولار فلا يتغيّر.", en: "The relative reference B2 moves with the drag and becomes B3, while the absolute reference $D$1 is pinned by the dollar signs and stays." }
    },
    {
      q: { ar: "تريد عرض تغيّر عدد المراجعين خلال اثني عشر شهراً. أي رسم بياني أنسب؟", en: "You want to show how visitor numbers changed over twelve months. Which chart fits best?" },
      options: [
        { ar: "الرسم الخطي", en: "A line chart" },
        { ar: "الرسم الدائري", en: "A pie chart" },
        { ar: "جدول بلا رسم", en: "A table with no chart" },
        { ar: "رسم مبعثر لنقطتين", en: "A scatter plot of two points" }
      ],
      correct: 0,
      why: { ar: "الخط يُظهر التغيّر عبر الزمن واتجاهه. والدائري للنسب من كل واحد في لحظة واحدة، فلا يصلح لسلسلة زمنية.", en: "A line shows change over time and its direction. A pie shows parts of one whole at one moment, so it does not suit a time series." }
    },
    {
      q: { ar: "ما وظيفة المفتاح الأساسي (Primary Key) في جدول قاعدة البيانات؟", en: "What does a primary key do in a database table?" },
      options: [
        { ar: "يحمي قاعدة البيانات بكلمة مرور", en: "Protects the database with a password" },
        { ar: "يرتّب السجلات أبجدياً", en: "Sorts the records alphabetically" },
        { ar: "يحدد عدد الحقول المسموح بها", en: "Limits how many fields are allowed" },
        { ar: "يميّز كل سجل تمييزاً فريداً لا يتكرر ولا يُترك فارغاً", en: "Identifies each record uniquely, never repeated and never empty" }
      ],
      correct: 3,
      why: { ar: "وهو أساس الربط بين الجداول: رقم المراجع في جدول المراجعين هو ما يربط زياراته في جدول الزيارات.", en: "It is also the basis of linking tables: the visitor number in the visitors table is what links their visits in the visits table." }
    },
    {
      q: { ar: "أي مكوّنات Access هو «السؤال الذي تطرحه على البيانات»؟", en: "Which part of Access is \"the question you ask the data\"?" },
      options: [
        { ar: "الجدول Table", en: "Table" },
        { ar: "الاستعلام Query", en: "Query" },
        { ar: "النموذج Form", en: "Form" },
        { ar: "التقرير Report", en: "Report" }
      ],
      correct: 1,
      why: { ar: "الجدول يخزّن، والنموذج شاشة إدخال، والتقرير مخرج منسّق للطباعة. الاستعلام هو ما يسأل ويعرض النتيجة، ويُحفظ ليُعاد تشغيله.", en: "A table stores, a form is an entry screen, and a report is a formatted output. A query is what asks and shows the answer, and it is saved to be re-run." }
    },
    {
      q: { ar: "ما العلاقة التي تصف «مراجع واحد له عدة زيارات»؟", en: "Which relationship describes \"one visitor has several visits\"?" },
      options: [
        { ar: "واحد إلى واحد", en: "One to one" },
        { ar: "متعدد إلى متعدد", en: "Many to many" },
        { ar: "واحد إلى متعدد", en: "One to many" },
        { ar: "لا توجد علاقة", en: "No relationship" }
      ],
      correct: 2,
      why: { ar: "سجل واحد في جدول المراجعين يقابله عدة سجلات في جدول الزيارات، وهي أشهر العلاقات في قواعد البيانات.", en: "One record in the visitors table matches several records in the visits table, the most common relationship in databases." }
    },
    {
      q: { ar: "ما فائدة الشريحة الرئيسة (Slide Master) في PowerPoint؟", en: "What is the slide master for in PowerPoint?" },
      options: [
        { ar: "تشغيل العرض تلقائياً بلا تدخل", en: "Running the presentation automatically" },
        { ar: "إضافة مؤثرات صوتية للشرائح", en: "Adding sound effects to slides" },
        { ar: "ترجمة الشرائح إلى لغة أخرى", en: "Translating the slides into another language" },
        { ar: "قالب ترث منه كل الشرائح ألوانها وخطوطها، فتعديله يغيّر العرض كله", en: "A template all slides inherit colours and fonts from, so editing it changes the whole deck" }
      ],
      correct: 3,
      why: { ar: "هي نظير الأنماط في Word: مكان واحد للتعديل بدل تكرار العمل في كل شريحة.", en: "It is the equivalent of styles in Word: one place to edit instead of repeating the work on every slide." }
    },
    {
      q: { ar: "أرسلت تقريراً بصيغة .docx إلى جهة خارجية لاعتماده فقط. ما المشكلة؟", en: "You sent a report as .docx to an external body only for approval. What is the problem?" },
      options: [
        { ar: "الصيغة الأصلية قابلة للتعديل، والأنسب إرسال PDF لمن يقرأ ويعتمد", en: "The native format is editable; a PDF is better for someone who only reads and approves" },
        { ar: "صيغة .docx لا تُفتح إلا على ويندوز", en: "A .docx file only opens on Windows" },
        { ar: "الملف سيصل فارغاً حتماً", en: "The file will certainly arrive empty" },
        { ar: "لا مشكلة إطلاقاً، فكل الصيغ متطابقة", en: "No problem at all; all formats are identical" }
      ],
      correct: 0,
      why: { ar: "PDF يحفظ الشكل ولا يُعدَّل بسهولة. الصيغة الأصلية تُرسل لمن سيعدّل معك فقط.", en: "A PDF preserves the look and is not easily edited. The native format goes only to someone who will edit with you." }
    },
    {
      q: { ar: "أي العبارات صحيحة عن نسخة أوفيس على الويب مقارنة بنسخة سطح المكتب؟", en: "Which statement about Office on the web compared with the desktop version is correct?" },
      options: [
        { ar: "إمكاناتها أوسع من نسخة سطح المكتب", en: "It has more features than the desktop version" },
        { ar: "تعمل بلا إنترنت مثل نسخة سطح المكتب", en: "It works offline like the desktop version" },
        { ar: "تحفظ تلقائياً في السحابة، لكن بعض الأدوات المتقدمة غير متاحة، وAccess غير موجود فيها", en: "It saves automatically to the cloud, but some advanced tools are missing and Access is not available" },
        { ar: "تنتج ملفات بصيغ مختلفة لا تفتحها نسخة سطح المكتب", en: "It produces files in different formats that the desktop version cannot open" }
      ],
      correct: 2,
      why: { ar: "الملف واحد في النسختين. الفرق في الحاجة إلى الإنترنت، وطريقة الحفظ، واتساع الإمكانات، وغياب Access عن الويب.", en: "The file is the same in both. The differences are the need for internet, how saving works, feature depth, and Access being absent on the web." }
    },
    {
      q: { ar: "قسم يريد إرسال خطاب موعد شخصي إلى 300 مراجع، والأسماء مسجّلة في جدول Excel. ما الحل الأنسب؟", en: "A department wants to send a personalised appointment letter to 300 visitors whose names are in an Excel sheet. What is the best approach?" },
      options: [
        { ar: "كتابة 300 مستند يدوياً", en: "Typing 300 documents by hand" },
        { ar: "الدمج البريدي بين قالب في Word وجدول الأسماء", en: "A mail merge between a Word template and the names table" },
        { ar: "تحويل جدول Excel إلى عرض PowerPoint", en: "Converting the Excel sheet into a PowerPoint deck" },
        { ar: "إرسال ملف Excel نفسه إلى الجميع", en: "Sending the Excel file itself to everyone" }
      ],
      correct: 1,
      why: { ar: "الدمج البريدي يصل قالباً واحداً بمصدر بيانات فيُنتج مستنداً لكل سجل. وإرسال ملف الأسماء للجميع خطأ مهني يكشف بيانات الآخرين.", en: "A mail merge joins one template to a data source and produces a document per record. Sending the names file to everyone is a professional error that exposes other people's data." }
    },
    {
      q: { ar: "ما الدالة التي تعدّ عدد الأيام التي تجاوز فيها عدد المراجعين 100 في النطاق B2:B31؟", en: "Which function counts the days where visitors exceeded 100 in the range B2:B31?" },
      options: [
        { ar: "=COUNTIF(B2:B31,\">100\")", en: "=COUNTIF(B2:B31,\">100\")" },
        { ar: "=SUM(B2:B31)", en: "=SUM(B2:B31)" },
        { ar: "=AVERAGE(B2:B31)", en: "=AVERAGE(B2:B31)" },
        { ar: "=MAX(B2:B31)", en: "=MAX(B2:B31)" }
      ],
      correct: 0,
      why: { ar: "COUNTIF تعدّ الخلايا التي تحقق شرطاً. أما SUM فتجمع القيم، وAVERAGE تحسب المتوسط، وMAX تعطي أكبر قيمة.", en: "COUNTIF counts cells meeting a condition. SUM adds the values, AVERAGE computes the mean, and MAX returns the largest value." }
    },
    {
      q: { ar: "ما الميزة السحابية التي تنهي مشكلة الملفات المسماة «التقرير_النهائي_المعدل_2»؟", en: "Which cloud feature ends the problem of files named \"report_final_revised_2\"?" },
      options: [
        { ar: "الطباعة إلى PDF", en: "Printing to PDF" },
        { ar: "ضغط الملفات", en: "Compressing files" },
        { ar: "حماية الملف بكلمة مرور", en: "Password-protecting the file" },
        { ar: "نسخة واحدة مشتركة مع تحرير متزامن وسجل إصدارات", en: "One shared copy with co-editing and version history" }
      ],
      correct: 3,
      why: { ar: "سبب تعدد النسخ هو تبادل الملف بالبريد. النسخة المشتركة في السحابة تجعل الجميع يعملون على ملف واحد، وسجل الإصدارات يعيد أي حالة سابقة.", en: "The multiple copies come from mailing the file around. A shared cloud copy keeps everyone on one file, and version history restores any earlier state." }
    },
    {
      q: { ar: "زميل يطلب منك إرسال ملف Excel فيه أسماء مرضى وأرقام هوياتهم عبر تطبيق محادثة شخصي. ما التصرف الصحيح؟", en: "A colleague asks you to send an Excel file with patient names and ID numbers through a personal messaging app. What is the right action?" },
      options: [
        { ar: "إرساله بعد حذف عمود واحد فقط", en: "Send it after deleting one column" },
        { ar: "إرساله مع كتابة «سري» في اسم الملف", en: "Send it with the word \"confidential\" in the file name" },
        { ar: "الاعتذار واستخدام القنوات المعتمدة في الجهة لمشاركة بيانات المرضى", en: "Decline and use the organisation's approved channels for sharing patient data" },
        { ar: "إرساله لأن الزميل موظف في الجهة نفسها", en: "Send it because the colleague works at the same organisation" }
      ],
      correct: 2,
      why: { ar: "بيانات المرضى تخضع لسياسات الجهة وأنظمة حماية البيانات، والانتماء للجهة نفسها لا يعني صلاحية الاطلاع. القناة المعتمدة والصلاحية هما الأساس.", en: "Patient data falls under organisational policy and data protection rules, and working at the same place does not grant access rights. The approved channel and proper authorisation are what matter." }
    },
    {
      q: { ar: "ما الغرض من تتبّع التغييرات (Track Changes) في Word؟", en: "What is track changes in Word for?" },
      options: [
        { ar: "حفظ الملف تلقائياً كل دقيقة", en: "Saving the file automatically every minute" },
        { ar: "تسجيل تعديلات كل مراجع بلون مميّز ليُقبل التعديل أو يُرفض", en: "Recording each reviewer's edits in a distinct colour so they can be accepted or rejected" },
        { ar: "منع فتح الملف على أجهزة أخرى", en: "Preventing the file from opening on other machines" },
        { ar: "ترجمة المستند آلياً", en: "Translating the document automatically" }
      ],
      correct: 1,
      why: { ar: "وهو أساس مراجعة التقارير الرسمية: ترى من غيّر ماذا، وتقرّر قبول كل تعديل أو رفضه قبل الاعتماد.", en: "It is the basis of reviewing official reports: you see who changed what, and decide to accept or reject each edit before approval." }
    }
  ],

  m5: [
    {
      q: { ar: "أي هذه ليست شرطاً في الخوارزمية السليمة؟", en: "Which of these is NOT a condition for a sound algorithm?" },
      options: [
        { ar: "أن تكون خطواتها محددة لا تحتمل أكثر من فهم", en: "Its steps are defined and cannot be read in two ways" },
        { ar: "أن تكون مكتوبة بلغة برمجة معيّنة", en: "It is written in a specific programming language" },
        { ar: "أن تكون منتهية ولا تدور بلا توقف", en: "It is finite and does not run forever" },
        { ar: "أن يكون لها مدخلات ومخرجات", en: "It has inputs and outputs" }
      ],
      correct: 1,
      why: { ar: "الخوارزمية فكرة مستقلة عن اللغة: وصفة الطبخ وإجراءات فرز المرضى خوارزميات، ويمكن تنفيذها بأي لغة أو بلا حاسب أصلاً.", en: "An algorithm is an idea independent of language: a recipe and a triage procedure are algorithms, and can be carried out in any language or with no computer at all." }
    },
    {
      q: { ar: "في أي مرحلة من دورة تطوير البرنامج يكون تصحيح الخطأ أرخص ما يكون؟", en: "At which stage of the development cycle is fixing an error cheapest?" },
      options: [
        { ar: "الترميز", en: "Coding" },
        { ar: "الاختبار", en: "Testing" },
        { ar: "تحليل المشكلة", en: "Analysis" },
        { ar: "الصيانة بعد التشغيل", en: "Maintenance after go-live" }
      ],
      correct: 2,
      why: { ar: "خطأ يُكتشف في التحليل يُصحَّح بجملة، وفي الترميز بساعة، وبعد التشغيل قد يكلّف إعادة بناء ومسؤولية على بيانات حقيقية.", en: "An error caught in analysis is fixed with a sentence, in coding with an hour, and after go-live it may cost a rebuild and responsibility over real data." }
    },
    {
      q: { ar: "ما الشكل الذي يمثّل القرار في المخطط الانسيابي؟", en: "Which shape represents a decision in a flowchart?" },
      options: [
        { ar: "المعيّن", en: "The diamond" },
        { ar: "البيضاوي", en: "The oval" },
        { ar: "المستطيل", en: "The rectangle" },
        { ar: "متوازي الأضلاع", en: "The parallelogram" }
      ],
      correct: 0,
      why: { ar: "البيضاوي بداية أو نهاية، والمستطيل عملية، ومتوازي الأضلاع إدخال أو إخراج. والمعيّن له مخرجان: نعم ولا.", en: "The oval is start or end, the rectangle a process, and the parallelogram input or output. The diamond has two exits: yes and no." }
    },
    {
      q: { ar: "ما الفرق بين المترجم (Compiler) والمفسّر (Interpreter)؟", en: "What is the difference between a compiler and an interpreter?" },
      options: [
        { ar: "المترجم للغات العربية والمفسّر للغات الإنجليزية", en: "A compiler is for Arabic and an interpreter for English" },
        { ar: "المفسّر يحوّل الكود إلى مخطط انسيابي", en: "An interpreter turns code into a flowchart" },
        { ar: "لا فرق، فكلاهما اسمان لشيء واحد", en: "No difference; they are two names for one thing" },
        { ar: "المترجم يحوّل البرنامج كاملاً مرة واحدة قبل التشغيل، والمفسّر يترجم وينفّذ سطراً سطراً", en: "A compiler converts the whole program once before running; an interpreter translates and runs line by line" }
      ],
      correct: 3,
      why: { ar: "ولهذا تظهر أخطاء المترجم كلها قبل التشغيل، بينما تظهر أخطاء المفسّر عند بلوغ السطر الخاطئ. وبايثون لغة مفسّرة.", en: "That is why a compiler shows all errors before running, while an interpreter shows them when it reaches the faulty line. Python is interpreted." }
    },
    {
      q: { ar: "برنامج يحسب معدل طالب ويعمل بلا توقف، لكنه يعطي 45 بدل 75. أي نوع من الأخطاء هذا؟", en: "A program computes a student average, runs without stopping, but returns 45 instead of 75. Which error type is this?" },
      options: [
        { ar: "خطأ صياغة Syntax Error", en: "Syntax error" },
        { ar: "خطأ تشغيل Runtime Error", en: "Runtime error" },
        { ar: "خطأ منطقي Logic Error", en: "Logic error" },
        { ar: "ليس خطأ، بل عطل في الجهاز", en: "Not an error, but a hardware fault" }
      ],
      correct: 2,
      why: { ar: "البرنامج يعمل ولا يتوقف، لكن النتيجة خاطئة — وهذا الخطأ المنطقي، وأخطرها لأنه لا يصرخ. ويُكتشف بالاختبار بحالات تُعرف نتيجتها سلفاً.", en: "The program runs and does not stop, but the result is wrong — a logic error, the most dangerous kind because it stays silent. It is caught by testing with cases whose answer you already know." }
    },
    {
      q: { ar: "لماذا اختير بايثون لهذا المقرر تحديداً؟", en: "Why was Python chosen for this course?" },
      options: [
        { ar: "قواعدها قريبة من الإنجليزية البسيطة، ومفسّرة فترى نتيجة السطر فوراً، ومجانية مفتوحة المصدر، ومكتباتها واسعة", en: "Its rules are close to simple English, it is interpreted so you see a line's result at once, it is free and open source, and its libraries are broad" },
        { ar: "لأنها أقدم لغة برمجة في العالم", en: "Because it is the world's oldest programming language" },
        { ar: "لأنها اللغة الوحيدة التي يفهمها المعالج مباشرة", en: "Because it is the only language a processor understands directly" },
        { ar: "لأنها لغة منخفضة المستوى قريبة من العتاد", en: "Because it is a low-level language close to the hardware" }
      ],
      correct: 0,
      why: { ar: "لا لغة يفهمها المعالج مباشرة سوى لغة الآلة. وبايثون لغة عالية المستوى، أي بعيدة عن تفاصيل العتاد وقريبة من الإنسان.", en: "No language is understood directly by the processor except machine language. Python is high-level, meaning far from hardware detail and close to humans." }
    }
  ]

};
