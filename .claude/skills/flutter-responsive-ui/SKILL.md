---
name: flutter-responsive-ui
description: >-
  Build or adapt a Flutter screen or component from a design or requirements
  using local constraints, content-driven layout changes, scrolling, text scaling,
  supported inputs/locales, and state preservation. Use for "ابن شاشة متجاوبة"
  or substantive responsive/adaptive implementation. Do not use for review-only
  audits, data-only work, small color/spacing edits, or every Widget change.
---

# تنفيذ Responsive/Adaptive UI

## النطاق والمدخلات

ابنِ أو كيّف UI وفق التصميم والمتطلبات المتاحة وبنية المشروع.
اقرأ screen/components/state scope والـTheme/assets والقرارات والمنصات/اللغات ونسخة SDK المرتبطة.
اسأل عن نقص يغير UX/layout فقط؛ تقدم في الأجزاء التي لا تعتمد عليه.
لا تختلق design/platform support أو universal breakpoints أو package sizing.
لو المطلوب مراجعة فقط استخدم flutter-responsive-audit.

## المراجع الانتقائية

الروابط من مجلد `SKILL.md` المثبت؛ حُلها بالنسبة إليه، لا cwd.
المراجع معرفة عادية تُقرأ عند الحاجة؛ لا تُحمّل المكتبة كلها.
أي ملف غير متاح يذكر بوضوح.

| الحاجة | المرجع |
|---|---|
| مصدر القيود والمحاور — الأساس | [Constraints](../../flutter-knowledge/ui/constraints-and-sizing.md) |
| تركيب/threshold/preservation | [Adaptive layout](../../flutter-knowledge/ui/breakpoints-and-adaptive-layouts.md) |
| List/Grid/Sliver/viewport | [Scrolling](../../flutter-knowledge/ui/scrolling-and-grids.md) |
| text/Theme/scale/overflow | [Typography](../../flutter-knowledge/ui/typography-and-scaling.md) |
| صورة/media/fit/loading/error | [Media](../../flutter-knowledge/ui/images-and-media.md) |
| RTL/input/focus/keyboard/SafeArea | [Platform and input](../../flutter-knowledge/ui/platform-accessibility-and-input.md) |
| Provider/owner يعاد عند resize | [Lifecycle](../../flutter-knowledge/state/lifecycle-and-di.md) |
| verification cases | [Testing](../../flutter-knowledge/quality/testing-and-verification.md) |
| API/version/source ambiguity | [Source map](../../flutter-knowledge/source-map.md) |

## سير العمل

1. حدد المعلومات والأفعال الضرورية وflows وحالات data/loading/empty/error ذات الصلة.
2. تتبع constraints من viewport إلى المكوّن: local/window/environment، bounded axes وscroll owner.
3. اختر composition حسب المحتوى: flex/wrap/list/grid/slivers، max content width عند مبرر.
   إن احتاج structural change، اختر threshold ذات سبب واختبر طرفيها؛ لا device labels وحدها.
   ابدأ بحدود تصميم بسيطة قابلة للتجربة. لا تبنِ قياس نص runtime أو helper ديناميكية
   حول جملة افتراضية لمجرد تجنب رقم breakpoint؛ يلزم مطلب ومنفعة وتكلفة مبررة.
4. حافظ على حقيقة واحدة للمحتوى والسلوك بين layouts.
   حدد ما يجب حفظه: draft/query/selection/scroll/focus؛ owner/resources في scope ثابتة عند الحاجة.
5. استخدم Theme/readability/wrapping؛ احترم TextScaler ولا double-scale أو globally disable.
   راجع الصور geometry/fit ومعنى crop والـloading/error.
6. طبق دعم المنصة/input/RTL/keyboard/SafeArea الفعلي؛ لا double insets أو actions محجوبة.
7. نفذ داخل حدود MVVM: View للعرض/موارد UI، Cubit لتنسيق حالة الميزة، Data للtransport.
   لا request/navigation business effect من build أو resize.
8. تحقق بمصفوفة متناسبة: narrow/wide/local panel، threshold boundaries،
   short height، long text/scale/RTL، keyboard أو input عند الصلة.
   أثناء typing/loading/scroll غيّر المساحة وافحص preservation المطلوب.
9. شغّل checks/test/platform run المتاحة؛ صنّف review أو simulated test أو native evidence بدقة.
   نفذ optimization فقط عند تكلفة ملموسة، مع قياس إن ادعيت performance تحسنًا.

## المخرجات ومعايير القبول

- UI قابلة للاستخدام حسب السيناريوهات المدعومة، مع layout decision وسبب threshold إن وجدت.
- تغييرات متناسبة لا business logic مكررة في narrow/wide.
- نص وأفعال ضرورية reachable؛ لا overflow مخفية أو shrink-to-fit مضللة.
- state محفوظة وفق requirement، دون طلب جديد/submit/effect بسبب resize.
- matrix ونتائج verification وحدودها؛ screenshot وحدها لا تثبت keyboard/ownership.
- لا dependency أو platform style جديدة دون قرار معتمد.

## حدود التداخل

لا تعيد تصميم Cubit صحيحة لأجل layout فقط.
إذا state flow تحتاج تنفيذًا فعلًا، استخدم flutter-cubit-flow لذلك الجزء.
لا تطلق responsive-audit كاملة على كل تعديل؛ هي طلب مراجعة مستقل.
إذا feature requirements/architecture مؤثرة وغير واضحة، استخدم تخطيطًا متناسبًا دون تحويله لتعقيد غير لازم.

## مثال طلب

«نفّذ هذا النموذج بعمود واحد أو عمودين حسب المساحة، واحفظ البيانات عند resize وراعِ الكيبورد والنص الكبير».
