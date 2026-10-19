# مراجع Flutter عند الحاجة

الإصدار 1.0.0 — منظومة عامة لمشاريع Flutter المستقبلية.
هذا المجلد Markdown عادي؛ لا يكتشفه Cursor كنوع Rule أو Skill خاص.
Skills تقرأ موضوعاتها مباشرة عبر روابط نسبية من مجلد كل Skill.
الفهرس للتصفح؛ ليس خطوة واجبة قبل كل مهمة.

## الخيارات المعتمدة

MVVM؛ Cubit يؤدي دور ViewModel؛ تنظيم feature-first؛ Cubit وgo_router وDio خيارات البداية.
Domain وUse Cases تُضافان عندما تحلان حاجة فعلية.
قرارات مشروع معتمدة أو تعليمات المستخدم في المهمة قد تخصص هذه البداية.
لا ترحّل مشروعًا قائمًا، ولا تضف حزمًا اختيارية لمجرد ظهورها في مرجع.

## المعمارية

| المرجع | اقرأه عند |
|---|---|
| [MVVM والطبقات](architecture/mvvm-and-layers.md) | تخطيط ميزة أو توزيع مسؤوليات أو تقييم فصل الطبقات |
| [Repositories وUse Cases](architecture/repositories-and-use-cases.md) | تحديد عقد بيانات، سياسة cache أو تنسيق عمليات |
| [Models وDTOs](architecture/models-and-dtos.md) | parsing أو model mapping أو تغير عقد API |
| [Routing والتكامل](architecture/routing-and-integration.md) | go_router، تفاصيل بالمعرّف، دخول مباشر أو تغيّر نطاق الحالة |

## الحالة

| المرجع | اقرأه عند |
|---|---|
| [الملكية وCubit/Bloc](state/ownership-and-cubit-bloc.md) | تحديد مالك الحالة أو اختيار أسلوب تدفقها |
| [تصميم الحالة](state/state-design.md) | حالات ناقصة أو refresh/empty أو copy/equality |
| [Lifecycle وDI](state/lifecycle-and-di.md) | إنشاء Cubit وإغلاقه أو اختيار scope للاعتماديات |
| [Async flows](state/async-flows.md) | بحث، تكرار طلب، race، إلغاء أو mutations |
| [الأخطاء والنتائج](state/errors-and-results.md) | mapping للفشل أو رسالة خاطئة أو معالجة expected/unexpected errors |
| [UI binding والتأثيرات](state/ui-binding-and-effects.md) | Builder/Listener/Selector أو navigation/toast يتكرر |

## الواجهة

| المرجع | اقرأه عند |
|---|---|
| [Constraints والقياسات](ui/constraints-and-sizing.md) | overflow أو محاور غير محدودة أو اختيار local/window size |
| [Scrolling والشبكات](ui/scrolling-and-grids.md) | قوائم وشبكات وSlivers أو تعارض scroll owners |
| [Breakpoints والتكيّف](ui/breakpoints-and-adaptive-layouts.md) | تغير هيكل الشاشة أو حفظ الحالة عند resize |
| [Typography وscaling](ui/typography-and-scaling.md) | نص طويل أو TextScaler أو أحجام خط متجاوبة |
| [Images وmedia](ui/images-and-media.md) | fit/crop ونسب الصور وحالات التحميل والخطأ |
| [المنصة والوصول والإدخال](ui/platform-accessibility-and-input.md) | RTL، keyboard، focus، SafeArea أو منصة مختلفة |

## الجودة

| المرجع | اقرأه عند |
|---|---|
| [الاختبارات والتحقق](quality/testing-and-verification.md) | تحديد دليل سلوكي أو اختبارات async/widget/integration |
| [الأداء والتحديثات](quality/performance-and-rebuilds.md) | مشكلة أداء قابلة للقياس أو rebuild/layout غير مناسب |
| [قوائم المراجعة](quality/review-checklists.md) | responsive audit أو مراجعة تكامل ميزة |

## كيف تقرأ مثالًا

الأمثلة موسومة بمصدرها وافتراضاتها.
Snippet ليس مشروعًا كاملًا إلا إذا صرّح المرجع بذلك؛ اربطه بعقود مشروعك.
القيم العددية والأسماء مثل Item وSearch أمثلة توضيحية، وليست متطلبات منتج.
لا يتساوى «مراجع وفق الوثائق» مع «compiled» أو «متحقق على الجهاز».
تفاصيل المنشأ والإصدارات والتصحيح المعروف في [خريطة المصادر](source-map.md).

## تحديث المعرفة

حدث المرجع الذي تغير، ثم سجل السبب والنسخة في خريطة المصادر.
تظل Skills تشير إلى مسار ثابت؛ لا تكرر المعرفة داخلها.
إذا تغير قرار مشروع، وثقه في `docs/ai/project-decisions.md` لذلك المشروع.
إذا تغير سلوك Cursor أو صيغته، افحص الوثائق الحالية وأعد سيناريو تفعيل حقيقي.
