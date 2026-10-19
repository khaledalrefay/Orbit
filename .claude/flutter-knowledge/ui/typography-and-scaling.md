# Typography وTextScaler وقابلية القراءة

اقرأ عند نص طويل أو تكبير النظام أو overflow بسبب الخط أو scaling helper.
ابدأ بالمعنى والمساحة، ثم اضبط typography.

## المحتويات

- المصدر
- مستويان للـscaling
- ترتيب المعالجة
- أمثلة وحدودها
- مصفوفة النص
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** R07 Responsive Typography وأمثلة تغيير حجم النص حسب العرض.
**[مراجعة KB]** TextScaler بدل textScaleFactor، وحفظ system scaling، R11 الوصول.
**[استنتاج]** فصل design sizing عن system scaling يمنع double scaling.
**[إضافة]** ترتيب التشخيص والاختبارات.
[خريطة المصادر](../source-map.md).

## design typography مقابل system scaling

| البعد | الغرض | owner |
|---|---|---|
| Theme/TextTheme | hierarchy وحجم baseline/weight/line height | design system للمشروع |
| content/layout adaptation | تغليف/أعمدة/عرض نص/actions | UI local constraints |
| TextScaler من النظام | تفضيل المستخدم وقد يكون غير خطي | environment عبر MediaQuery |
| locale/font | glyph metrics واتجاه ومعنى | المشروع وموارد localization |

لا تضرب fontSize يدويًا في textScaleFactor ثم تترك Text يطبق system scaling مرة أخرى.
لا تعطل scaling عالميًا لتخفي overflow.
لا تفترض أن scalar واحد يصف تجربة كل أحجام الخط في non-linear scaling.

## ترتيب المعالجة

1. حدّد النص الضروري والمسموح truncation فيه.
2. تأكد أن قيود العرض صحيحة؛ Row بلا bounding مشكلة layout.
3. اسمح wrapping/height مناسبة أو scroll عند الحاجة.
4. غيّر تركيب actions/labels إذا لا يتسع.
5. اضبط Theme وفق التصميم وقابلية القراءة.
6. افحص TextScaler واللغة والمنصة.
7. إذا احتجت design scaling، حدد حدودًا ومبررًا واختبر combined behavior.

قيم base widths 400/700/1000 وclamp 0.8–1.2 الواردة في القاعدة أمثلة تعليمية.
لا تعتمدها لكل مشروع ولا تجعلها تقلص نصًا ضروريًا عند width أصغر.
ScreenUtil اختيار library مستقل؛ لا يحل semantics أو reflow تلقائيًا.

## مثال baseline

**[إضافة]** fragment:
```dart
Text(
  description,
  style: Theme.of(context).textTheme.bodyLarge,
)
```

يترك Text يأخذ scaling من environment افتراضيًا.
`description` مدخل، ويحتاج parent بعرض مناسب وارتفاع/scroll يسمح بالمحتوى.
هذا ليس ضمانًا لعدم overflow في Column محدودة height.

إذا احتجت قياسًا:
```dart
final scaler = MediaQuery.of(context).textScaler;
final scaledSize = scaler.scale(baseFontSize);
```

هذا لقرار قياس محدد؛ لا تمرر `scaledSize` كـfontSize إلى Text التي ستطبق scaler مجددًا دون ضبط مقصود.
عند TextPainter أو custom drawing، اتبع API المناسبة للـSDK حتى يطابق القياس الرسم.
لا تضف custom text measure لكل label عادية.

## truncation وFittedBox

| المحتوى | سياسة ممكنة | حد |
|---|---|---|
| عنوان بطاقة مع تفاصيل متاحة | ellipsis مع طريق واضح للنص الكامل | أثبت إمكانية الوصول للمعنى |
| validation/error/instructions أساسية | wrapping/scroll/reflow | لا تقصها تلقائيًا |
| رقم/label زخرفي | sizing خاص حسب التصميم | readability والsemantics |
| action مهم | طول label وtarget area | لا تصغر النص/الضغط إلى غير قابل للاستعمال |

FittedBox قد يصغّر محتوى بصريًا دون حل مساحة النص وظيفيًا.
استعمله فقط عندما تصميم العنصر ومعناه يسمحان بذلك؛ لا blanket fix لoverflow.
حجم الخط ليس وحده readability؛ line length وspacing وcontrast واللغة مؤثرة.

## مصفوفة التحقق

| محور | حالات مهمة |
|---|---|
| المحتوى | قصير، طويل، multi-line، أرقام طويلة/غير قابلة للفصل |
| اللغة | اللغات المدعومة، RTL/LTR ومزج أرقام وروابط |
| scale | default ثم قيمة كبيرة ذات صلة؛ نظام فعلي على المنصة |
| المكان | narrow panel، wide content مع max width، short height |
| الوظيفة | labels/actions/errors/title/body، لا body وحدها |

`TextScaler.linear(2)` محاكاة useful في widget test وفق SDK،
لكنها لا تثبت non-linear behavior الأصلي أو كل إعدادات OS.
تحقق على منصة مدعومة عند أهمية accessibility.
التصوير الثابت للتصميم لا يكشف ذلك.

## التشخيص

| العَرَض | السبب المحتمل | المعالجة |
|---|---|---|
| تضخم غير متوقع للنص | scaling يدوي + system | baseline واحدة وsystem واضح |
| خط صغير في narrow | width ratio دون minimum معنى | layout/readability أولًا |
| overflow رغم maxLines | finite height/row constraints | قيود وreflow حسب المحتوى |
| نص system كبير لا يظهر | noScaling أو FittedBox shrink | احترام preference وإعادة تركيب |
| spacing خاطئ مع RTL | physical left/right أو inline assumptions | directional layout ومراجعة النص |
| test خطي ينجح والجهاز يفشل | nonlinear/native fonts | اختبار منصة فعلي |

## معايير قبول

- TextTheme للمشروع مستخدمة حيث تلائم التصميم، دون أحجام متناثرة غير مبررة.
- no double scaling؛ preference النظام محفوظة.
- النص الضروري والمعنى/action قابلان للوصول.
- truncation قرار واضح، لا وسيلة لإخفاء constraint bug.
- نطاق التحقق يذكر linear simulation مقابل platform run.

## حالة الإصدار

[TextScaler migration](https://docs.flutter.dev/release/breaking-changes/deprecate-textscalefactor)
— مستقر منذ Flutter 3.16.
[MediaQueryData.textScaler](https://api.flutter.dev/flutter/widgets/MediaQueryData/textScaler.html)
— يعكس استراتيجية النظام.
تحقق 2026-10-01؛ مشروع أقدم يحتاج API ملائمة لنسخته ولا يُرقّى تلقائيًا.
