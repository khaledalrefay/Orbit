# مراجعة قائمة على الدليل

اقرأ عند flutter-responsive-audit أو flutter-feature-review.
اختر checklist المناسبة للنطاق؛ لا تفحص كل موضوع في تعديل بسيط.

## المحتويات

- المصدر ونمط النتيجة
- مراجعة الحالة
- مراجعة الشاشة
- مراجعة التكامل
- شدة الملاحظة
- حدود الأدلة والمتابعة

## المصدر

**[مراجعة KB/تلخيص]** M19 Common Problems، M20 Decision Guides، M23 Checklist،
R13 Common Problems، R14 Decision Guides، R16 Checklist.
**[إضافة]** نموذج findings ودرجات الشدة والأولوية.
لا تجعل بندًا في checklist قرارًا هندسيًا جديدًا.
[خريطة المصادر](../source-map.md).

## قبل المراجعة

حدد requirements، نطاق الملفات/المسار، قرارات المشروع، النسخ، والمنصات المدعومة.
Review-only يعني findings؛ لا تعدل الكود إلا إذا الطلب أو تعليمات لاحقة تفوض الإصلاح.
لا تطلب جميع بيانات المشروع upfront؛ اطلب المفقود المؤثر فقط واستمر في الفحص المستقل.
إذا المشروع يخالف default لكنه يتبع قرارًا معتمدًا، قيّم اتساقه لا قربه من القالب.

## نموذج الملاحظة

```text
العنوان: مشكلة ملموسة وسيناريو ظهورها
الشدة: blocker / major / minor / suggestion
الموضع: الملف + الموضع أو الرمز المرتبط
السيناريو: input/state/viewport/route الذي يكشفها
الدليل: ما شوهد أو شُغّل أو يمكن إثباته من source
الأثر: ما يحدث للمستخدم/البيانات/التكامل
السبب: سلسلة واضحة؛ إذا فرضية تُوسم كذلك
الإصلاح المقترح: أصغر تغيير يحافظ على القرار المعتمد
التحقق: assertion أو خطوات تعيد الحالة وتثبت المعالجة
الحالة: confirmed / probable / needs runtime verification
```

لا تقدم تحسين تفضيلي على أنه bug.
ولا تنسب compile/runtime failure دون تنفيذ أو دليل source كاف، مع بيان نوع الدليل.

## مراجعة state flow

| محور | أسئلة |
|---|---|
| completeness | هل View تستطيع الرسم من snapshot؟ initial وempty والفشل مميزون؟ |
| immutability | هل lists/elements/copy semantics سليمة؟ |
| owner | من يخلق/يقرأ/يعيد ضبط state؟ |
| lifecycle | create/value وclose/dependencies وعمر route صحيح؟ |
| async | repeated/stale/cancel/debounce سياسة منفصلة لكل command؟ |
| errors | expected/unexpected وآمنة، لا كل خطأ No Internet؟ |
| binding | builder بلا آثار، effect owner واحد، initial timing واضح؟ |
| behavior tests | races/close/empty/retry المهمة لها دليل؟ |

لتفصيل المشكلة اقرأ المرجع المختص مباشرة؛ لا تنسخ قائمة state كلها إلى findings.

## مراجعة شاشة Responsive

| محور | أسئلة |
|---|---|
| constraints | local/window size والمحاور finite/ParentData صحيحة؟ |
| layout strategy | thresholds مبنية على المحتوى؟ shell/component متسقان؟ |
| text | طويلة وscale وRTL دون فقد ضروري؟ |
| scroll | owner/viewport/lazy content والأفعال reachable؟ |
| media | ratio/fit/loading/error/crop مع معنى واضح؟ |
| input | keyboard/focus/touch/mouse حسب الدعم؟ |
| preservation | draft/query/scroll/selection تبقى حسب المطلوب بعد resize؟ |
| performance | هل توجد تكلفة مثبتة لا افتراض من أسماء Widgets؟ |

في image-only review يمكن رصد تركيب ظاهر؛ لا تثبت source ownership أو stale policy أو keyboard behavior.

## مراجعة تكامل ميزة

| محور | أسئلة |
|---|---|
| المتطلبات | هل flows وacceptance والحالات المهمة معلومة ومتحققة؟ |
| المسؤوليات | UI/Cubit/Repository وDomain إن وجدت بحدود المعتمدة؟ |
| contract | parsing/DTO/data absence/failure semantics متسقة عبر الطبقات؟ |
| navigation | durable ID وdirect entry وIDchange/back/route exit حسب النطاق؟ |
| الحالة والواجهة | widthchange لا تعيد business action أو تفقد مطلوبًا؟ |
| effects | نفس intent لا يتكرر في route/listener مختلفة؟ |
| dependencies | لا حزم/upgrade/migration غير معتمدة؟ |
| tests | دليل behavior/interface/platform ضمن المخاطر الفعلية؟ |

اجمع الملاحظات من العقود إلى النتائج للمستخدم.
إذا سبب واحد يولّد ثلاثة أعراض، اكتب finding واحدة مع آثارها بدل تكرارها لكل طبقة.

## شدة وأولوية

| الشدة | معنى عملي |
|---|---|
| blocker | يمنع flow أساسية أو يسبب فسادًا/تعطلًا جوهريًا مثبتًا |
| major | سلوك خاطئ مؤثر أو فقد input أو عدم وصول إلى فعل أساسي |
| minor | خلل محدود بوظيفة/عرض مع استمرار المسار الأساسي |
| suggestion | تحسين له مفاضلة؛ لا requirement أو bug مثبت |

استخدم أثرًا ملموسًا لتبرير الشدة.
ضع المؤكد المؤثر أولًا، وافصل unknowns والتحسينات.
لا تضف تحذيرات نظرية عن كل خطر محتمل دون ارتباط بالمهمة.

## الأدلة والنتيجة

- source review: أشر للرمز/الطريق والأثر المشروط.
- executed test: اسم الاختبار/الأمر والنتيجة والبيئة.
- screenshot: observations بحدود الصورة.
- unavailable runtime: scenario مطلوب وماذا سيحسم.
- no material findings: اذكر ما فُحص وما بقي دون ادعاء خلو كامل.

مخرج مختصر:
1. findings مرتبة.
2. أسئلة/قرارات مؤثرة فقط.
3. تحقق منفذ وحدوده وتحقق مطلوب.
4. عند تفويض الإصلاح: نطاق التغييرات ونتيجة verification.

## فضّ التعارض

متطلبات المستخدم والقرار المعتمد للمشروع تحكم اختيار البدائل.
Rules عامة تحدد baseline؛ references تشرح الأدلة والخيارات.
إذا قراران معتمدان يتعارضان فعلًا، اعرض مثال التعارض والبديل الموصى به واطلب الحسم.
لا تختر رأيًا اعتمادًا على ترتيب ملفات .mdc، ولا تكتب override جديدًا لإخفاء التعارض.
إذا المعطى unknown لكنه غير مؤثر، لا توقف المهمة.
