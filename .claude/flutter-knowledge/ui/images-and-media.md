# Images وMedia: النسب والقص وحالات التحميل

اقرأ عند صور cards/details أو icons/SVG أو media تغيّر layout.
افصل مساحة الوسيط عن كيفية رسمه داخلها.

## المحتويات

- المصدر
- geometry مقابل fit
- سياسة crop والمعنى
- loading/error
- مثال بطاقة
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** R08 Responsive Images and Media، وأمثلة صور/AspectRatio بالقاعدة.
**[مراجعة KB]** التمييز بين نسبة الحاوية والقص، R11 الوصول.
**[إضافة]** حالات التحقق والdiagnostics.
[خريطة المصادر](../source-map.md).

## geometry وfit

| القرار | الأداة/المعنى | قيد |
|---|---|---|
| مساحة محجوزة بنسبة | AspectRatio/قيود container | القيود الأعلى قد تمنع النسبة |
| الحفاظ على الصورة كاملة | BoxFit.contain | فراغ محتمل داخل الإطار |
| ملء frame مع crop | BoxFit.cover | جزء من المصدر سيختفي حسب الأبعاد |
| stretch | BoxFit.fill | قد يشوه النسب |
| تموضع الجزء المرئي | alignment/تصميم frame | لا يضمن إبقاء كل معنى الصورة |

AspectRatio لا يقرر BoxFit، وBoxFit لا يحدد حجم parent.
الصورة الطبيعية dimensions قد تصل بعد network؛ احجز geometry إذا ثبات layout مطلوب.

## crop قرار معنى

| الوسيط | بداية سياسة | تحقق |
|---|---|---|
| thumbnail زخرفية | cover ممكن | crop مقبول ولا يحذف معلومة مطلوبة |
| وثيقة/رسم/نص داخل صورة | contain أو viewer واضح | كل البيانات قابلة للوصول |
| صورة هوية/منتج | قرار focal point/design | موضوع الصورة لا يختفي |
| chart | responsive رسم/labels أو scroll/zoom مقصود | لا scale-to-fit يجعل المعنى غير مقروء |

لا تخفِ caption أو badge مهم بcrop.
إذا picture معنوية، semantics/alt-like label مناسب حسب UI،
وإذا decorative فتجنب الإعلان المكرر.
الـsemantic description يجب أن يضيف معنى، لا تكرار النص المجاور بلا فائدة.

## loading/error

- احجز حجمًا متقاربًا بين loading/success/error لتجنب قفز layout.
- fallback يعبر عن حالة مقصودة، لا مساحة فارغة ذات معنى غامض.
- retry إذا مطلوب له action قابل للاستعمال.
- لا تضع raw URL/error في label للمستخدم.
- إذا image optional، حدد هل غيابها يختلف عن فشل التحميل.
- loadingBuilder قد يعاد كثيرًا؛ ضع عملًا بسيطًا ولا تبدأ request منها.
- احترام cache/network contracts؛ لا clear cache كحل عام لفشل صورة.

## مثال frame

**[إضافة]** fragment لthumbnail مع crop معتمد:
```dart
AspectRatio(
  aspectRatio: 3 / 2,
  child: Image.network(
    imageUrl,
    fit: BoxFit.cover,
    errorBuilder: (context, error, stack) => const Center(
      child: Icon(Icons.broken_image_outlined),
    ),
  ),
)
```

`imageUrl` مدخل؛ 3:2 وcover قرارات المثال فقط.
الـAspectRatio يحجز مساحة وفق القيود حتى عند failure.
هذا لا يعرّف loading feedback أو accessibility أو network diagnostics كاملة.
الـIcon وحدها ليست رسالة failure مفهومة لكل مستخدم؛ أضف semantics/label وفق المعنى.
لا تجعل هذا template لصورة وثيقة ينبغي رؤيتها كاملة.

## صور كبيرة وأداء

حجم الرسم غير حجم decode؛ قد تحمل صورة كبيرة داخل thumbnail صغيرة.
عند مشكلة مقاسة، افحص resolution/server variants وcache/decode options المناسبة للنسخة.
لا تضف image package أو resize algorithm تلقائيًا.
اختبر memory/frame مع البيانات الحقيقية في profile mode عند الحاجة.

## SVG وicons

flutter_svg package اختيارية تحتاج نسخة واعتمادًا.
لا تحول SVG إلى PNG تلقائيًا «للتجاوب»؛ نوع الملف ليس سياسة layout.
لـcustom asset تحقق viewBox/الحجم/stroke وأثر scaling.
حجم icon المرئي لا يساوي حجم target التفاعلي:
يمكن أن يبقى glyph صغيرًا داخل مساحة ضغط وفوكس مناسبة.
Tooltip/semantic label للفعل حسب منصة/input، ولا تعتمد على hover فقط للأفعال الأساسية.

## media أخرى

فيديو/PageView/map/chart لها controller وعمر وقيود خاصة.
عند الحاجة، اقرأ API الرسمية لنسخة package والمنصة المعتمدة.
هذا المرجع لا يختار package ولا permission ولا aspect ratio عالمي.
التكيف قد يكون controls مختلفة أو full-screen mode وفق UX، وليس تصغيرًا فقط.

## التشخيص

| العَرَض | افحص | التصحيح |
|---|---|---|
| card تقفز عند وصول الصورة | geometry قبل التحميل | إطار ثابت/ratio مقصودة |
| محتوى مهم مقصوص | cover/alignment | contain/viewer/design مناسب |
| الصورة مشوهة | fit.fill أو constraints | ratio/fit يتفقان مع المحتوى |
| icon يصعب الضغط | target غير glyph size | مساحة تفاعل/semantics مناسبة |
| failure يختفي في فراغ | fallback policy | معنى ورسالة/إعادة محاولة ملائمة |
| jank/memory كبيرة | source/decode size | profile ثم resolution/variant |

## مصفوفة قبول

- نسب portrait/landscape/extreme للصور.
- URL غائبة/تحميل بطيء/failure/نجاح.
- narrow/wide card وRTL/scale للنصوص المحيطة.
- crop المقبول مقابل meaningful image.
- target/focus/semantics للفعل، ليست صورة الشكل فقط.
- أداء لا يُعلن بلا قياس.

## حالة التحقق

المبادئ مصدرها R08/R11 مع صياغة سياقية.
أي API package أو media platform يحتاج تحقق نسخة المشروع.
المثال Flutter fragment لم يُشغّل هنا.
