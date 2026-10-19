# ربط state بالواجهة والتأثيرات

اقرأ عند Builder/Listener/Selector أو تكرار navigation/toast أو rebuild غير مفهوم.
اجعل الرسم قابلًا للتكرار، والتأثير مرتبطًا بانتقال مقصود.

## المحتويات

- المصدر
- builder/listener/consumer/selector
- توقيت التأثير وملكيته
- الفلاتر وحدودها
- مثال انتقال
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** M08 BlocBuilder BlocListener and BlocConsumer.
**[مراجعة KB]** TR-002 فصل العرض والتأثيرات، M17 نطاق rebuild.
**[إضافة]** قواعد الربط والتشخيص السياقية.
[خريطة المصادر](../source-map.md).

## اختيار Widget

| الأداة | عملها | متى تستخدم |
|---|---|---|
| BlocBuilder | رسم من state | تغير محتوى UI مع snapshot |
| BlocListener | رد فعل على تغير state مؤهل | navigation/snackbar/dialog وفق انتقال |
| BlocConsumer | يجمع builder+listener | نفس الموضع يحتاج الاثنين فعلًا |
| BlocSelector | تحديد جزء immutable | reader يحتاج قيمة مستقلة ضيقة |
| context.read | access لأمر دون subscription | user action/trigger معلوم |
| watch/select | subscription وفق API المشروع | يتطلب scope وقيمة مناسبة |

لا تستخدم Consumer لمجرد أن اسمها يشمل كل شيء.
لا تنفذ navigation/requests/notifications داخل builder.
Builder قد يعمل مع parent rebuild أو Theme/MediaQuery/local state حتى لو لم يتغير Cubit.

## ما هو effect؟

نتيجة جانبية لا يصفها مجرد redraw: route push، message، dialog، طلب focus عند مرحلة معينة.
loading/content/error داخل الشاشة عادة render state، لا listener effect.
قد توجد حاجة إلى الاثنين، مثل inline validation ورسالة نجاح؛ حدد كل responsibility.

لكل effect:
- من owner الذي ينفذه مرة في المكان المقصود؟
- ما transition الذي يسمح به؟
- هل يعاد عند retry/success جديدة؟
- هل يجب التعامل معه إذا بدأ listener بعد الحالة؟
- هل route exit أو duplicate listeners يمنعه/يضاعفه؟

## timing وinitial

BlocListener يستجيب لتغيرات state المؤهلة، وليس replay للحالة الحالية عند mount.
previous المستخدمة في listenWhen تبدأ بالحالة عند تهيئة listener.
لا تبنِ requirement «انقل فورًا لأن Cubit كانت successful قبل mount» على listener وحدها.
صمم guard/route initialization أو explicit effect contract إذا الحاجة موجودة.

كل listener منفصلة تستطيع تنفيذ effect؛ «مرة لكل transition» لا يعني مرة على مستوى التطبيق كله.
ينبغي وجود owner واحد للتأثير المطلوب.
إذا success جديدة تأتي مرتين متطابقتين، equality/operation identity/filters يحددون السلوك؛ لا تفترض once عالمي.

## مثال انتقال

**[إضافة]** fragment؛ SaveCubit/SaveState/SavePhase من المشروع، لا تعريف عام:

```dart
BlocListener<SaveCubit, SaveState>(
  listenWhen: (previous, current) =>
      previous.phase != current.phase &&
      current.phase == SavePhase.success,
  listener: (context, state) {
    // تنفيذ تأثير النجاح المتفق عليه هنا، في owner واحد.
  },
  child: const SaveForm(),
)
```

يصلح إذا كل save جديدة تمر بمرحلة أخرى قبل success.
إذا توجد عدة عمليات successful متزامنة دون phase transition مختلفة،
قد تحتاج operation ID/effect model وفق requirement.
لا تضف effect queue architecture لكل feature تلقائيًا.

## الفلاتر

`buildWhen` يقلل updates القادمة من Bloc stream للموضع؛ لا يضمن أن builder لا يعمل لأسباب أخرى.
`listenWhen` يختار eligible transitions؛ لا يعوض نقص state أو ملكية التأثير.
Selector يحتاج selected value immutable وقيمة equality مناسبة.

مثال اختيار:
- list widget تختار items؛ spinner تختار phase إذا عقد UI يسمح فصلها.
- لا تختَر mutable List ثم تعدلها in-place.
- لا تقطع حقولًا يجب رسمها معًا على نحو يجعل UI تلاحظ combinations غير متسقة.
- تكاليف selectors/filtering ينبغي أن تناسب حاجة فعلية.

## local resources

Controller/animation وفوكس موارد UI:
- تنشأ وتغلق في صاحبها.
- الربط بين state/input لا يعيد النص/selection عند كل rebuild بلا intent.
- إذا change مصدره المستخدم ثم listener تعيد القيمة، احمِ feedback loop.
- resize يغير Layout؛ لا يعيد initialization أو requestFocus تلقائيًا.
- بعد await في UI، mounted/resources validity قبل الاستخدام.

التفاصيل في [lifecycle-and-di.md](lifecycle-and-di.md)
و[platform-accessibility-and-input.md](../ui/platform-accessibility-and-input.md).

## التشخيص

| العَرَض | افحص | التصحيح |
|---|---|---|
| snackbar/navigation عدة مرات | builder effect أو listeners مكررة | effect owner واحد وانتقال واضح |
| effect لا يحدث عند فتح الصفحة | initial state قبل listener | explicit entry behavior حسب المتطلب |
| UI لا يتحدث | buildWhen/equality/select value | فحص snapshot وfilter لا إضافة setState عشوائيًا |
| child يعاد رغم buildWhen=false | parent/environment rebuild | تشخيص السبب الصحيح |
| text selection تقفز | كتابة controller عند كل redraw | تحديث مقصود يحفظ input semantics |
| layout change يطلق effect | إنشاء listener/owner داخل branch | owner مستقر وعقد transition |

## معايير تحقق

- إعادة build بلا تغير intent لا ترسل request ولا تنفذ effect.
- انتقال نجاح واحد يؤدي إلى التأثير المتفق عليه من owner واحد.
- initial/pre-existing success تعاملها صريح إذا المنتج يحتاجه.
- retry وتغير operation identity لا يمنعان تأثيرًا جديدًا مشروعًا.
- selectors تعتمد snapshots immutable ومساواة صحيحة.
- resize/Theme/TextScaler يغير العرض دون آثار غير مطلوبة.
- اختبارات effect behavioral؛ لا تكتفِ بفحص نوع Widget.

## حالة الإصدار

[BlocListener](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocListener-class.html)
و[BlocSelector](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocSelector-class.html)
— flutter_bloc 9.1.1، تحقق 2026-10-01.
استعمل constructor `bloc:` عند تمرير instance صراحة، بحسب API الفعلية.
أمثلة Save مرجعية تحتاج عقود مشروع ولم تُشغّل هنا.
