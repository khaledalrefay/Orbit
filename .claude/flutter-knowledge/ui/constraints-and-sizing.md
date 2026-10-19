# Constraints والقياسات

اقرأ عند overflow أو unbounded axis أو اختيار LayoutBuilder/MediaQuery.
ابدأ بمسار القيود، ثم اختر Widget؛ لا تعالج كل عَرَض بقيمة ثابتة.

## المحتويات

- المصدر والآلية
- local مقابل window
- Flex والقيود
- sizing tools
- مثال وتشخيص
- التحقق

## المصدر

**[كورس بحسب KB]** R01–R04: Core Concepts، Layout System، MediaQuery vs LayoutBuilder، Constraints and Sizing.
**[مراجعة KB]** التوضيحات الخاصة بالمحاور والقياسات الحديثة في هذه الأقسام.
**[إضافة]** طريقة تتبع constraint path والجداول والأمثلة.
[خريطة المصادر](../source-map.md).

## الآلية

الـparent يمرر القيود، child يختار حجمًا ضمنها، ثم parent يحدد موضعه.
`tight` يعني min==max لذلك البعد؛ `loose` يسمح باختيار حجم ضمن الحد.
بعد يمكن أن يكون unbounded دون أن يصبح كل layout غير صالح؛ المشكلة عندما يطلب child التوسع لمالانهاية.
لـscroll direction غالبًا قيود مختلفة عن cross axis.

تتبع: viewport → Scaffold/body → padding/panel → Flex/scroll → child.
دوّن maxWidth/maxHeight عند نقطة الفشل. لا تبدأ من قياس الجهاز كله.

## local أم window؟

| الحاجة | مصدر مناسب | خطأ شائع |
|---|---|---|
| تصميم بطاقة داخل sidebar | LayoutBuilder محلي | استخدام width النافذة كاملة |
| اختيار shell عام | قيد body أو window وفق تركيب الصفحة | shell وchild يختلفان بسبب مصدرين بلا قصد |
| padding/keyboard/TextScaler | MediaQuery من السياق المناسب | global cached value لا تتحدث |
| حجم physical pixels | API للعرض عند حاجة فعلية | استعمالها كـlogical layout width |
| sliver يعتمد على مساحة محور عرض | SliverLayoutBuilder | افتراض أنه يعطي BoxConstraints |

Flutter layout يتعامل مع logical pixels.
devicePixelRatio لتحويل physical/logical عندما الحاجة تتطلبه، لا لحساب breakpoint مرة أخرى.
تجنب global views.first أو cached MediaQuery للحالة المتجاوبة؛ تعدد windows وتغير البيئة يبطلان الافتراض.

## Flex

| الأداة | عملها | شرط |
|---|---|---|
| Expanded | ملء الحصة المتبقية بإحكام | Flex في main axis له مساحة finite مناسبة |
| Flexible | السماح بالحصة دون إجبار ملئها عند loose | لا يُصلح parent غير محدودة تلقائيًا |
| Spacer | flex space | نفس شروط Flex |
| Row مع Text طويلة | النص يحتاج عرضًا bounded | Expanded/Flexible أو عرض محدد مقصود |
| spaceBetween | يوزع الفراغ المتبقي | لا يصغّر children التي لا تتسع |

Expanded/Flexible ParentData يجب أن تصلا إلى Flex المناسب دون RenderObject Widget يفصل العلاقة.
مثلًا ضع `Expanded(child: Padding(...))` داخل Row، لا Padding يحيط بـExpanded داخل Row.
الـwidgets الشفافة في الشجرة لا تجعل كل مكان صالحًا للـExpanded.

Column داخل vertical SingleChildScrollView قد تكون main axis unbounded.
إضافة Expanded فيها ليست طريقة لصنع viewport.
اختر composition/قيود/scroll owner صحيحة بدل patch ارتفاع شاشة عام.

## أدوات sizing

| الأداة | استخدام | قيد |
|---|---|---|
| SizedBox | فجوة أو بعد مقصود | ليس ارتفاعًا ثابتًا لكل محتوى متغير |
| ConstrainedBox | min/max للمحتوى | parent قد تكون أضيق من min المطلوبة |
| Align/Center | تموضع وتخفيف بعض القيود | افهم القيود التي يعيدانها |
| FractionallySizedBox | نسبة من مساحة bounded | نسبة لمالانهاية غير مفيدة |
| AspectRatio | محاولة نسبة ضمن constraints | القيود قد تمنع تحقيق النسبة |
| IntrinsicHeight/Width | قياس intrinsic محدود عند حاجة | قد يضيف عمل layout مكلفًا؛ قِس ولا تعمم |
| Wrap | runs جديدة عندما لا تتسع العناصر | ليس lazy list للبيانات الطويلة |
| Flow | positioning متخصص | لا اختيار أول لشاشة form/list عادية |

افصل spacing design tokens عن حجم محتوى يتأثر بالخط/اللغة.
لا يقتضي التجاوب أن كل رقم يتحول إلى نسبة من عرض النافذة.

## مثال Row

**[إضافة]** fragment لـtitle/action ضمن عرض finite:

```dart
Row(
  children: [
    Expanded(
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium,
      ),
    ),
    const SizedBox(width: 12),
    TextButton(onPressed: onOpen, child: const Text('فتح')),
  ],
)
```

`title` و`onOpen` مدخلات المكوّن.
هذا يسمح تغليف title؛ لا يضمن نجاح Row إذا button نفسه لا يتسع عند width ضيق/نص كبير.
في تلك الحالة، غيّر التركيب إلى Column/Wrap أو action row وفق معنى المحتوى.
لا تقلص النص الضروري بــFittedBox لتخفي overflow.

## مثال قرار محلي

**[إضافة]** LayoutBuilder يقرر عدد أعمدة panel من constraints.maxWidth.
يجب أن تصل إليه finite width؛ إذا غير ذلك، اعرف لماذا قبل حساب threshold.
يمكن لبطاقة في نافذة واسعة أن تختار layout ضيقة إذا panel ضيقة؛ هذا مطلوب عند local adaptation.
لا تصنف المكوّن Desktop لأن النافذة واسعة.

## التشخيص

| العَرَض | تتبع | حل محتمل والتحقق |
|---|---|---|
| RenderFlex overflow | widths والنص/action والscale | bounding + إعادة ترتيب عند حاجة |
| unbounded viewport | scroll nesting والparent height | viewport finite أو slivers في owner واحد |
| Expanded exception | finite main axis وParentData | Flex relation صحيحة لا shrinkWrap عشوائيًا |
| مكوّن داخل panel يستخدم تصميم واسع | MediaQuery full window | local constraints |
| AspectRatio لا يحقق الشكل | tight min/max متعارضة | layout contract لا افتراض أن الأداة تتجاوز parent |
| حجم لا يتغير عند resize | cached width/global API | dependency محلية متجددة |

## قبول وتحقق

- مصدر قياس كل قرار معلوم: local/window/environment.
- layout بالـlogical pixels دون خلط DPR.
- bounded/unbounded axes وFlex parentage صحيحة.
- اختبر ضيقًا، عرضًا متوسطًا، نافذة واسعة مع panel ضيقة، ونصًا طويلًا مكبرًا.
- horizontal overflow لا يُخفى بالقص إلا إذا المحتوى غير ضروري أو UX يقصد ذلك.
- وجود LayoutBuilder وحده لا يثبت responsive behavior.

## حالة التحقق

[LayoutBuilder](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html) و
[SliverLayoutBuilder](https://api.flutter.dev/flutter/widgets/SliverLayoutBuilder-class.html)
و[Wrap](https://api.flutter.dev/flutter/widgets/Wrap-class.html) قورنت بتاريخ 2026-10-01.
اختبارات التطبيق والمنصات لم تُنفّذ هنا.
