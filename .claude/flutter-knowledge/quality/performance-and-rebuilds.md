# الأداء وrebuilds: تشخيص قبل تحسين

اقرأ عند jank أو تكلفة layout/build/decode أو نقاش selector/const.
لا تدّع تحسن الأداء بسبب نقل Widget إلى ملف.

## المحتويات

- المصدر
- تحديد نوع المشكلة
- build وlayout/render
- optimizations متناسبة
- async وCPU
- القياس والقبول

## المصدر

**[مراجعة KB]** M17 Performance and Rebuild Optimization، R12 Performance Considerations،
TR-009 extraction ليست دليل أداء.
**[كورس بحسب KB]** أجزاء واجهات Bookly تؤسس إعادة استخدام مكوّنات؛ لا نعممها كقياس performance.
**[إضافة]** ترتيب diagnosis والقياس.
[خريطة المصادر](../source-map.md).

## صنّف المشكلة

| المظهر | احتمال | دليل مناسب |
|---|---|---|
| jank أثناء scroll | layout/render/media/eager work | profile/timeline وعناصر حقيقية |
| build كثير | subscriptions/parent/environment | rebuild tracing ونطاق widgets |
| request متكرر | lifecycle/trigger | request counters لا FPS فقط |
| memory عالية | media/resources/cache | profiler/owner lifetime |
| UI تتجمد في حساب | CPU synchronous على UI isolate | timeline ومعطيات عملية |
| overflow | correctness constraints | layout trace؛ ليست performance fix أولًا |

قارن بحالة قابلة للإعادة على platform مستهدفة.
Debug أو DevicePreview وحدهما لا يثبتان الأداء النهائي.

## rebuild ليس repaint

build يقرر tree، layout يحسب geometry، paint/render يرسمان.
تقليل عدد build قد لا يعالج decode كبيرة أو expensive layout.
وثّق bottleneck بدل اختيار const/selectors كجواب مسبق.

Builder/Selector:
- اجعل readers على القدر الذي يحتاجونه.
- selected value immutable بمساواة مناسبة.
- buildWhen يمنع بعض stream-driven updates، لا parent/environment rebuild.
- لا تقطع payload مترابطة على نحو يضر correctness.

## خيارات متناسبة

| اختيار | منفعة محتملة | حد |
|---|---|---|
| const عند إمكانها | instance مستقرة والعمل أقل في مواضع | لا تمنع كل rebuild/paint |
| widget extraction | وضوح ومسؤولية وإعادة استخدام | ملف جديد ليس قياس سرعة |
| lazy List/Grid/Slivers | بناء/عرض مناسب للبيانات الطويلة | viewport/extent/pagination ما زالت مهمة |
| أقل intrinsic/shrinkWrap غير مبررة | عمل sizing أقل | ليست محظورة في محتوى محدود |
| media dimensions مناسبة | decode/memory أقل | API/server/cache يلزم تحققًا |
| Selector narrow | updates أقل لمستهلك | equality/immutability/cost |
| cache | تقليل transport/calculation | policy/writes/memory ومصدر حقيقة |

لا تضف framework أو memoization أو isolate قبل ملاحظة تكلفة فعلية أو requirement واضحة.

## async لا يساوي CPU خارج UI

Future/await ينظمان الانتظار؛ حساب synchronous قبل/بعد await ما زال قد يحجب isolate الحالية.
Parsing صغير عادة لا يحتاج isolate.
إذا dataset كبيرة والقياس يثبت bottleneck:
- اختبر كمية العمل/algorithm/تقليل البيانات أولًا.
- انظر إلى compute/isolate وفق Flutter/Dart platform APIs.
- تحقق transfer/copy cost والقيود ودعم المنصة.
- لا تنقل resources UI أو BuildContext.
- API native/web behavior حساس للإصدار؛ راجع الوثيقة قبل implementation.

هذه إمكانية **[إضافة]** وليست اعتماد optimization عامة.

## Observer وdiagnostics

BlocObserver قد يساعد تتبع changes/transitions/errors وفق hooks ونسخة الحزمة.
لا يعني telemetry product كاملة، ولا يقيس layout/render وحده.
استخدم logging محددًا غير حساس؛ لا tokens/full payload.
تجنب إضافة monitoring service كجزء من مراجعة صغيرة بلا حاجة واعتماد.

## خطة قياس

1. حدد السيناريو والبيانات والجهاز/المنصة والmode.
2. سجل baseline: الزمن أو frames أو requests/memory المناسب للمشكلة.
3. حدد فرضية واحدة لها سبب ملموس.
4. غيّر الموضع المرتبط بها.
5. أعد السيناريو نفسه وقارن metric relevant.
6. افحص correctness/accessibility/state preservation بعد التعديل.
7. إذا لا توجد بيئة profile، سجّل اقتراحًا لا تحسنًا مثبتًا.

المقارنة يجب أن تكون على إعدادات comparable؛ لا تقارن debug قديم بـprofile جديد وتستنتج الكود السبب.

## التشخيص

| العَرَض | التحقيق | اتجاه علاج |
|---|---|---|
| List بطيئة رغم const | viewport/lazy/media | bottleneck الحقيقي |
| كل page تتحدث لقيمة واحدة | subscription واسعة | consumer أضيق عند عدم كسر coherence |
| card جديدة الملف ولم تتحسن | extraction فقط | measurement لا وعود |
| form تتجمد في validation | sync CPU/data | algorithm ثم isolate عند قياس |
| cache تخفف network لكن stale | source truth/invalidation | correctness قبل metric |
| resize يرسل requests | lifecycle لا rendercost | owner/trigger الصحيح |

## معايير قبول

- سبب الأداء محدد بدليل أو مصنف كفرضية.
- metric وظروف before/after معلومة عند ادعاء تحسين.
- لا optimizations تضر state/المعنى/قابلية الوصول.
- لا packages أو معماريات جديدة لمجرد احتمال مشكلة مستقبلية.
- لم يُجر profile؟ يقال ذلك بوضوح.

## حالة الإصدار

المفاهيم من M17/R12.
أدوات DevTools/isolate/image APIs تحتاج التحقق من وثائق SDK/المنصة الفعلية عند التنفيذ.
هذه الحزمة لم تتضمن قياسًا لتطبيق Flutter؛ لا تُنسب إليها أرقام performance.
