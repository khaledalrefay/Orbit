---
name: flutter-feature-planning
description: >-
  Plan a substantial Flutter feature or architectural refactor before coding
  when requirements, MVVM responsibilities, state ownership, async behavior,
  or responsive strategy need decisions. Use for requests such as "خطط الميزة
  قبل التنفيذ". Produce a proportional plan. Do not use for tiny cosmetic
  changes, a narrow bug with a known cause, review-only requests, or non-Flutter work.
---

# تخطيط ميزة Flutter

## النطاق

حوّل متطلبات الميزة إلى خطة قابلة للتنفيذ وفق قرارات المشروع.
لا تعدل ملفات التنفيذ أثناء التخطيط.
إذا فوّض المستخدم التنفيذ أيضًا، أكمله بعد التخطيط ضمن الخيارات المعتمدة؛
لا تطلب موافقة جديدة على تفاصيل روتينية أو قرار سبق اعتماده.
لا تحوّل التخطيط إلى اعتماد تلقائي لحزمة أو تغيير stack أو نطاق منتج.

## المدخلات

اقرأ المتطلبات/التصميم المتاح، أجزاء المستودع المتأثرة، `pubspec.yaml` ونسخ relevant dependencies،
والأجزاء المرتبطة من `docs/ai/project-decisions.md` إن وجدت.
في مشروع جديد أو قبل وجود repo، سجل versions/platforms غير المعروفة؛ لا تختلقها.
اسأل عن نقص يغيّر الخطة فقط، واستمر في الأجزاء المستقلة.

## المراجع الانتقائية

المسارات التالية محسوبة من مجلد هذا `SKILL.md`، لا من cwd المشروع.
حدد مسار Skill المثبتة ثم حُل الروابط بالنسبة إليه.
إذا مرجع غير موجود، صرّح بذلك ولا تدّع قراءته أو نسب قرار إليه.
لا تقرأ الفهرس أو جميع المراجع تلقائيًا.

| الحاجة | المرجع المباشر |
|---|---|
| توزيع الطبقات — الأساس | [MVVM](../../flutter-knowledge/architecture/mvvm-and-layers.md) |
| ملكية الحالة — الأساس | [Ownership](../../flutter-knowledge/state/ownership-and-cubit-bloc.md) |
| اختيار contract/Use Case/cache | [Repositories](../../flutter-knowledge/architecture/repositories-and-use-cases.md) |
| DTO/schema جديدة | [Models](../../flutter-knowledge/architecture/models-and-dtos.md) |
| requests متداخلة أو submit | [Async](../../flutter-knowledge/state/async-flows.md) |
| routes/ID/direct entry | [Routing](../../flutter-knowledge/architecture/routing-and-integration.md) |
| UI تغير تركيبها | [Adaptive layouts](../../flutter-knowledge/ui/breakpoints-and-adaptive-layouts.md) |
| خطة تحقق غير واضحة | [Testing](../../flutter-knowledge/quality/testing-and-verification.md) |
| نسبة معلومة أو اختلاف إصدار | [Source map](../../flutter-knowledge/source-map.md) |

## سير العمل

1. لخّص goal والـflows وacceptance المهمة؛ افصل المؤكد عن السؤال/الافتراض.
   trigger البحث وسياسة التكرار/hفظ back ليست قرارات معتمدة إن لم تُذكر؛
   قدم توصية ومفاضلتها ووسمها، ولا تخلطها بمعايير قبول مؤكدة.
2. افحص الموجود لإعادة استخدام مسؤولية مستقرة، لا لإنشاء shared abstractions استباقية.
3. وزع View/Cubit/Repository وData؛ لا ViewModel ثانية لنفس state.
   ضع Domain/Use Case فقط إذا تضيف قاعدة مستقلة أو تنسيقًا أو إعادة استخدام ذات قيمة.
4. عرّف owner وreaders وreset/lifetime لكل حالة مهمة؛ ميز controllers/layout عن business state.
5. إذا async مؤثرة، حدد سياسة كل command: duplicate/stale/cancel/error/retry حسب contract.
6. إذا توجد UI، حدد مصدر القيود، scroll owner، تغير التركيب وحفظ draft/selection عند resize.
   لا تفرض breakpoint أو package sizing من أمثلة تعليمية.
7. حدد contract/model/failure/navigation عند صلتها؛ اذكر تغير ID أو direct entry إن مطلوبين.
8. رتّب تنفيذًا وverification يكشفان المخاطر الفعلية، مع ملفات مقترحة تتبع بنية repo.
9. اعرض القرار الجديد المؤثر مع البديل والمفاضلة والتوصية؛ اطلب الحسم إذا لم يكن مفوضًا.
   إن لم توجد قرارات مؤثرة، قدم الخطة ولا تختلق approval gate.

## المخرجات ومعايير القبول

قدم بقدر حجم الميزة:
- goal وacceptance والحالات المهمة.
- جدول مسؤوليات وowners/dependencies/lifetimes عند الحاجة.
- عقود البيانات/state/async/layout التي تحكم التنفيذ.
- خطوات تنفيذ وملفات متأثرة وverification سلوكي.
- unknowns والقرارات المؤثرة فقط.

الخطة مقبولة إذا كل layer إضافية مبررة، والقرارات المعتمدة محفوظة،
ولا raw transport في View، ولا state مالكان متنافسان،
والتحقق يرتبط بسلوك مطلوب لا بأسماء ملفات.
صرّح أن الكود لم يُنفّذ إذا المخرج خطة فقط.

## علاقة المهارات

هذه Skill تخطط؛ flutter-cubit-flow وflutter-responsive-ui تنفذان الجزء المناسب عند تفويض التنفيذ.
لا تستدعِ بقية Skills لمجرد ورود كلمة Cubit أو شاشة في الخطة.
flutter-feature-review لمراجعة تكامل موجودة، لا بديل دائم عن التخطيط.
flutter-responsive-audit لمراجعة responsive UI موجودة فقط.

## مثال طلب

«خطط ميزة بحث عن منتجات مع تفاصيل بالمعرّف وشاشة تتكيف مع المساحة، قبل كتابة الكود».
