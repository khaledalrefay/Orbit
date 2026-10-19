---
name: flutter-feature-review
description: >-
  Review an implemented Flutter feature end to end against its requirements
  and adopted architecture: layer contracts, models, Cubit/Bloc state ownership,
  async/lifecycle/effects, navigation, adaptive UI integration, and verification.
  Use for "راجع الميزة كاملة" or cross-layer integration review. Do not use for
  responsive-only audits, small visual changes, narrow known fixes, or non-Flutter work.
---

# مراجعة تكامل ميزة Flutter

## النطاق والمدخلات

راجع flow كاملة أو حدود تكامل محددة، بحسب طلب المستخدم.
اقرأ متطلبات الميزة وقرارات المشروع وfiles/contracts/routes/state/UI/tests ذات الصلة والنسخ.
لا تقارن مشروعًا معتمدًا بـdefault لتفرض migration.
Review-only تنتج findings. إذا الإصلاح مفوض، أصلح ضمن النطاق والقرارات المعتمدة بعد التشخيص.
اطلب النقص المؤثر فقط واستمر فيما يمكن مراجعته.

## المراجع الانتقائية

المسارات بالنسبة لمجلد `SKILL.md` المثبت؛ لا cwd.
اختر مباشرة ما يحتاجه مسار الميزة؛ لا كل مكتبة المعرفة ولا تشغيل جميع Skills تلقائيًا.
أفصح عن المرجع الغائب بدل ادعاء قراءته.

| الحاجة | المرجع |
|---|---|
| معيار النتائج والمراجعة — الأساس | [Review criteria](../../flutter-knowledge/quality/review-checklists.md) |
| حدود ومسؤوليات | [MVVM](../../flutter-knowledge/architecture/mvvm-and-layers.md) |
| contract/source/usecase | [Repositories](../../flutter-knowledge/architecture/repositories-and-use-cases.md) |
| parsing/DTO/model | [Models](../../flutter-knowledge/architecture/models-and-dtos.md) |
| route/ID/direct entry | [Routing](../../flutter-knowledge/architecture/routing-and-integration.md) |
| owner/splitting/local state | [Ownership](../../flutter-knowledge/state/ownership-and-cubit-bloc.md) |
| state incomplete/equality/copy | [State](../../flutter-knowledge/state/state-design.md) |
| lifetime/create/value | [Lifecycle](../../flutter-knowledge/state/lifecycle-and-di.md) |
| race/repeated/cancel | [Async](../../flutter-knowledge/state/async-flows.md) |
| failure/result/message | [Failures](../../flutter-knowledge/state/errors-and-results.md) |
| effects/builder/selectors | [UI binding](../../flutter-knowledge/state/ui-binding-and-effects.md) |
| resize يفقد أو يغيّر state | [Adaptive layouts](../../flutter-knowledge/ui/breakpoints-and-adaptive-layouts.md) |
| constraints/scroll/text/input مشكلة فعلية | [Constraints](../../flutter-knowledge/ui/constraints-and-sizing.md)، [Scrolling](../../flutter-knowledge/ui/scrolling-and-grids.md)، [Typography](../../flutter-knowledge/ui/typography-and-scaling.md)، [Input](../../flutter-knowledge/ui/platform-accessibility-and-input.md) |
| evidence/test coverage | [Verification](../../flutter-knowledge/quality/testing-and-verification.md) |
| أداء له دليل | [Performance](../../flutter-knowledge/quality/performance-and-rebuilds.md) |
| source/version غير واضحة | [Source map](../../flutter-knowledge/source-map.md) |

## سير العمل

1. حدد acceptance وentry points وقرار architecture/dependencies، وافصل unknowns عن defects.
2. اتبع intent من View إلى Cubit ثم contract/Data والعودة:
   parsing/data absence/failure والموديل والعرض متسقة؟
3. راجع المسؤوليات والاعتماديات وDomain/Use Cases إن موجودة؛ لا wrappers جديدة بلا قيمة.
4. تتبع state owner والعمر/إغلاق الموارد وinput/ID changes وroute exit.
5. افحص transitions/immutable snapshot/empty/refresh/equality والـasync policy لكل command.
6. راجع render/effects وdirect route/deep-link requirements وback behavior بحسب الدعم.
7. افحص التكامل مع adaptive UI: owner ثابت، draft/query محفوظة عند الطلب،
   resize لا يطلق business action، النص/actions/keyboard قابلون للاستخدام.
   لا تبدأ responsive audit كاملة إن لم تظهر حاجة أو طلب.
8. قيّم tests والدليل؛ نفذ checks المتاحة المسموح بها عند الصلة.
   لا validation واسعة بلا خطر مرتبط، ولا claim platform run من static review.
9. اجمع findings بحسب السبب والأثر، بأصغر fix مناسب وخطوة تحقق.
   ميز bug المؤكد عن فرضية/suggestion وقرار بديل يحتاج المستخدم.
10. إذا أصلحت بتفويض، تحقق السلوك المتأثر ثم اشرح التغييرات وحدود verification.

## المخرجات ومعايير القبول

- findings مرتبة بالأثر، كل منها location/scenario/evidence/cause/fix/verification.
- نتيجة اتساق flow ومتطلبات الدخول والحالة والواجهة بقدر الفحص الفعلي.
- unknowns/قرارات مؤثرة واضحة، دون عدم توافق مزعوم مع default لمشروع له استثناء معتمد.
- تحقق منفذ ونتائج فعلية وحدوده، والمطلوب بعده إذا البيئة غير متاحة.
- لا تكرار نفس المشكلة لكل layer؛ لا blanket «أفضل الممارسات».
- لا تعديلات غير مفوضة أو packages/upgrades/migrations غير معتمدة.

## حدود التداخل

flutter-responsive-audit للطلب الذي يراجع تجاوب الشاشة فقط.
flutter-cubit-flow أو flutter-responsive-ui لإصلاح مفوض يتعلق بذلك الجزء.
لا تستخدم feature-planning لإعادة تخطيط كل feature أثناء مراجعتها.
ليس مطلوبًا إنشاء Subagents؛ المسؤولية هنا للمهندس نفسه وفق الأدلة.

## مثال طلب

«راجع ميزة البحث والتفاصيل كاملة: العقود، Cubit، التنقل، وحفظ الحالة عند تبدل الواجهة».
