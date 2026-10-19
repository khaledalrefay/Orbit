---
name: flutter-cubit-flow
description: >-
  Design, implement, modify, or diagnose a Flutter Cubit state flow, including
  immutable display state, commands, async races, lifecycle, failure handling,
  and UI binding. Use for "نفذ تدفق Cubit" or stale-result, duplicate-submit,
  or state-ownership bugs. Do not use for visual-only changes, trivial widget-local
  toggles, review-only whole-feature audits, or automatic migration of existing Bloc.
---

# تدفق Cubit وتكامله

## النطاق والمدخلات

اعمل على تدفق حالة له requirement أو عطل محدد.
اقرأ Cubit/state/Repository/widgets المتأثرة وtests والقرارات ونسخ الحزم ذات الصلة.
ميّز مطلوب التنفيذ عن التشخيص/المراجعة فقط؛ لا تعدل دون تفويض إصلاح.
Cubit default جديد؛ لا ترحّل Bloc قائمة أو تضف equality/concurrency/DI package تلقائيًا.
لو طلب إصلاح Bloc قائمة، حافظ على convention المشروع واستخدم معرفتها المناسبة.

## المراجع الانتقائية

المسارات من مجلد `SKILL.md` المثبت، لا cwd المشروع.
اقرأ المرجع المرتبط بالمشكلة، وأفصح عن أي مرجع غير متاح بدل ادعاء قراءته.

| الحاجة | المرجع |
|---|---|
| owner أو Cubit/Bloc/local state | [Ownership](../../flutter-knowledge/state/ownership-and-cubit-bloc.md) |
| snapshot/empty/refresh/equality — الأساس | [State design](../../flutter-knowledge/state/state-design.md) |
| Provider/close/dependencies | [Lifecycle](../../flutter-knowledge/state/lifecycle-and-di.md) |
| requests/repeated/stale/cancel/debounce | [Async](../../flutter-knowledge/state/async-flows.md) |
| expected/unexpected/result/message | [Failures](../../flutter-knowledge/state/errors-and-results.md) |
| builder/listener/selector/effects | [UI binding](../../flutter-knowledge/state/ui-binding-and-effects.md) |
| boundary/contract/usecase | [Repositories](../../flutter-knowledge/architecture/repositories-and-use-cases.md) |
| ID/route input أو exit | [Routing](../../flutter-knowledge/architecture/routing-and-integration.md) |
| اختبار behavior | [Testing](../../flutter-knowledge/quality/testing-and-verification.md) |
| API أو نسبة يحتاج تحققًا | [Source map](../../flutter-knowledge/source-map.md) |

## سير العمل

1. حدد intent الحالي، input، success/empty/failure/retry وما يجب حفظه؛ لا تضف جميع حالات نموذج عام.
2. ثبت owner/lifetime وcontract. احقن dependencies عبر constructor؛ لا BuildContext أو Dio في Cubit.
3. صمم state كاملة وimmutable. حدد equality وnullable clearing إن اعتمد السلوك عليهما.
4. عرّف commands والانتقالات. لكل عملية async حدد duplicate/stale/cancel/retry independently.
   عند input جديد أو clear، أبطل الطلب السابق في الوقت الذي تختاره UX، لا بعده عرضًا.
   `isClosed` لا يعالج freshness ولا يلغي HTTP.
5. حدد expected failure boundary وdiagnostics آمنة للـunexpected؛ لا ترد [] على أي error.
   في رقعة الكود المقترحة نفسها، استعمل رسالة آمنة وعقد diagnostics واضحًا؛
   لا تبقِ raw `error.toString()` للعرض أو catch صامتة وتكتفِ بملاحظة خارج المقطع.
   إذا آلية المشروع غير معروفة، بيّن اعتمادها المطلوب بدل اختلاق logger أو حزمة.
6. اربط الإنشاء/load/close بمكان وعمر مقصودين؛ create owned وvalue borrowed.
   لا trigger load في build ولا أكثر من trigger للتحميل نفسه دون قصد.
7. ارسم في builder؛ effects في owner واحد مع transition مؤهلة.
   لا تعتمد listener لإعادة initial state، ولا filter لإخفاء state ناقصة.
8. إذا مفوض بالتنفيذ، نفذ أصغر تغيير متسق مع المشروع. حافظ على owner فوق adaptive branch عند حفظ state.
9. اختبر السيناريو الذي قد يفشل: completion معكوس، clear/close، repeated command، empty/error/refresh،
   أو أثر واحد لكل transition وفق حاجة الميزة.
10. شغّل analyzer/tests المناسبة إن متاحة، وأبلغ بدقة ما نفذ وما لم ينفذ.
    لا تضف package أو تغير convention المشروع كتفصيل روتيني.

## المخرجات ومعايير القبول

في التنفيذ: state/commands والعقد والربط المعدل، شرح سياسة async والعمر، ونتيجة verification.
في التشخيص فقط: السبب والدليل والتعديل المقترح وخطوات تثبيته.
القبول:
- snapshot تكفي View، immutable بالقيم التي يعتمد عليها العرض.
- لا نتائج stale ولا تكرار يخالف policy المتفق عليها.
- ملكية create/value/resources والإغلاق صحيحة.
- error/empty/initial مفهومة وeffects لا تتكرر بلا قصد.
- تحقق behavior مرتبط بالتغيير؛ لا claims compiled إذا SDK غير متاحة.

## حدود التداخل

لا تخطط feature كاملة لعطل محدود. flutter-feature-planning إذا بقي قرار معماري مؤثر.
لا تعيد بناء layout لمجرد وجود Widget؛ flutter-responsive-ui عندما المهمة تتضمن تكيفًا فعليًا.
flutter-feature-review للمراجعة الشاملة، وflutter-responsive-audit للواجهة فقط.

## مثال طلب

«أصلح SearchCubit: نتيجة البحث القديمة أحيانًا تستبدل الجديدة، والمسح أثناء الطلب يعيد النتائج».
