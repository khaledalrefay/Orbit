# المنصة وإمكانية الوصول والإدخال

اقرأ عند RTL أو keyboard/focus أو SafeArea/insets أو منصة/input مختلف.
حدد ما يدعمه المشروع؛ لا تضف واجهات لكل منصة بلا متطلبات.

## المحتويات

- المصدر وحدود الدعم
- المنصة مقابل المساحة
- RTL والنص والمعنى
- input/focus/targets
- keyboard والمناطق الآمنة
- التشخيص والتحقق

## المصدر

**[مراجعة KB/توسعة]** R10 Platform-Adaptive UI؛ لا تنسبه تلقائيًا إلى دروس الكورس.
R11 Accessibility and Usability، R03 MediaQuery، R09 تغيير القيود.
**[استنتاج]** accessibility تُختبر مع layout وstate preservation، لا في قائمة منفصلة فقط.
**[إضافة]** مصفوفة السيناريوهات التالية.
[خريطة المصادر](../source-map.md).

## حدّد الدعم

اسأل فقط عما يؤثر في المهمة:
- المنصات المستهدفة والموجودة فعلًا في المشروع.
- اللغات/اتجاه النص والموارد المتاحة.
- touch/mouse/keyboard وسلوك focus.
- متطلبات الوصول المقبولة/المطلوبة في المنتج.
- البيئة المتاحة للاختبار.

Unknown لا يعني unsupported ولا وعدًا بدعم كامل.
سجل ما لم يُتحقق منه بدل استنتاج النجاح من screenshot.

## platform ≠ width

| البعد | يقرر عادة | لا يستنتج |
|---|---|---|
| local/window width | عدد أعمدة/تركيب | iOS/Android/Desktop |
| platform | interaction/style native عند مطلب | مساحة واسعة دائمًا |
| input capability | hover/focus/shortcuts | platform وحدها تكشف كل الإدخال |
| text direction/scaler | ترتيب/قراءة/مساحة | من اسم اللغة وحده دون environment |

`Widget.adaptive` له سلوك API محدد؛ لا يعني أن كل خصائصه تتكيف أو أن الصفحة كاملة adaptive.
Material/Cupertino اختيار تصميم مشروع. لا تفرض Cupertino لكل iOS أو style جديد دون requirement.
شارك منطق الميزة، وخصص UI عندما توجد منفعة محددة.

## RTL

- Directionality/localization من التطبيق.
- EdgeInsetsDirectional وAlignmentDirectional وstart/end عندما المعنى اتجاهي.
- لا تقلب ترتيب كل شيء يدويًا ثم Directionality تقلبه مرة ثانية.
- back/forward semantics تختلف عن أيقونة زخرفية قد لا تحتاج mirroring.
- الأرقام/URLs والنص المختلط تحتاج فحصًا بصريًا وظيفيًا.
- order المرئي وقراءة semantics/focus يجب أن يظلا مفهومين.

RTL لا يعني تغيير مصدر الحقيقة أو أوامر Cubit؛ هو سياق عرض/تفاعل.
الlabels/errors/actions النصية يجب أن تأتي من نمط localization المعتمد.

## input وfocus

| السيناريو | المطلوب المحتمل | التحقق |
|---|---|---|
| touch | target مريحة وأفعال واضحة | الضغط والscroll على جهاز |
| mouse | hover/tooltip عند معنى | action لا يعتمد عليها وحدها |
| keyboard | tab order وفوكس مرئي وتفعيل | Tab/Shift+Tab/Enter/Escape بحسب UX |
| form | focus progression/submit/error | reachability وvalidation |
| screen reader | أسماء وأدوار وحالات | traversal والمعنى على منصة |

استخدم controls القياسية عندما تلائم الحاجة؛ custom GestureDetector قد يحتاج semantics/focus بنفسه.
لا تتظاهر بتوافق كامل لأنها onTap تعمل.
focus resources تنشأ وتغلق لدى owner؛ نقل subtree قد يفقد focus حتى لو controller حفظت النص.
حجم glyph ليس target؛ تحقق guideline ملائم للمنصة عندما تعتمد قيمة عددية.

## keyboard وinsets

`viewInsets` تصف أجزاء محجوبة بالكامل مثل keyboard،
`viewPadding` تمثل مناطق الحواف،
و`padding` مشتقة وتتأثر بالعلاقة مع insets.
لا تجمع القيم الثلاث عشوائيًا.

| الحالة | اتجاه معالجة | خطر |
|---|---|---|
| Scaffold تعيد sizing عند keyboard | استفد من المساحة الجديدة وscroll | إضافة bottom inset مرة أخرى قد تضاعف الفراغ |
| overlay/bottom panel مخصصة | padding/position وفق viewInsets بعد فهم ancestors | double compensation |
| notch/system gesture areas | SafeArea/قرار edge-to-edge | SafeArea ليست حل keyboard كاملًا |
| field آخر الشاشة | scroll/reveal وفوكس | height ثابتة لا تسمح الوصول |
| desktop short window | layout/scroll حتى دون keyboard software | width وحدها ليست كافية |

قِس المساحة التي وصلت فعلًا إلى المكوّن.
حفظ focus/text وتجنب تكرار submit عند geometry change جزء من التكامل.
`showKeyboard` في widget test لا يثبت geometry/sizing للكيبورد الأصلية على النظام.

## مثال directional

**[إضافة]** fragment:
```dart
Padding(
  padding: const EdgeInsetsDirectional.only(start: 16, end: 24),
  child: Align(
    alignment: AlignmentDirectional.centerStart,
    child: Text(label),
  ),
)
```

`label` يأتي من المشروع. هذا يعالج اتجاه padding/alignment، لا localization أو قراءة semantics كاملة.

## التشخيص

| العَرَض | افحص | التصحيح والتحقق |
|---|---|---|
| فراغ ضخم عند keyboard | resizeToAvoidBottomInset + manual inset | إزالة double handling بعد تتبع قيود |
| زر submit محجوب | scroll/height/focus reveal | reachable action مع keyboard/short height |
| RTL نصف صحيح | left/right وترتيب يدوي | directional decisions ومراجعة mixed content |
| keyboard لا يصل action | focus/semantics/custom control | standard control أو contract input واضح |
| resize يسحب focus | owner/subtree replacement | focus policy وwidget/platform test |
| screen reader يكرر label | semantics مكررة | معنى واحد واضح لكل عنصر |

## مصفوفة قبول

- على المنصات واللغات المعتمدة فقط، مع ذكر النطاق.
- RTL/LTR ونص طويل/scaler كبير.
- narrow/short viewport مع keyboard ظاهر؛ field وsubmit reachable.
- typing ثم resize: draft لا تضيع، وfocus وفق policy.
- mouse/keyboard إذا مدعومان؛ traversal وتفعيل الأفعال الأساسية.
- semantics/contrast/targets وفق متطلبات المشروع وأداة تحقق فعلية عند الحاجة.

## حالة التحقق

[MediaQueryData.viewInsets](https://api.flutter.dev/flutter/widgets/MediaQueryData/viewInsets.html)
قورنت بتاريخ 2026-10-01.
القيم العددية لقواعد وصول أو إعدادات منصة تحتاج مصدرًا رسميًا ملائمًا قبل اعتمادها.
لم ينفذ اختبار OS keyboard أو screen reader هنا.
