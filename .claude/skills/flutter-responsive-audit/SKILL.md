---
name: flutter-responsive-audit
description: >-
  Review or diagnose the responsive/adaptive behavior of an existing Flutter
  screen: constraints, overflow, scroll ownership, text scaling, breakpoints,
  media, RTL, keyboard/focus, and resize state preservation. Use for
  "راجع تجاوب الشاشة" or a focused responsive audit. Do not use to build
  a new screen, for architecture-only reviews, tiny cosmetics, or a narrow known fix.
---

# مراجعة Responsive/Adaptive UI

## النطاق والمدخلات

راجع الشاشة الموجودة ونطاق التجاوب المطلوب.
المدخلات: source والـancestors/scroll/controller/Provider عند الصلة، المتطلبات،
المنصات/اللغات/Theme والنسخ، وأي screenshots أو runtime evidence.
الصورة وحدها تسمح بملاحظات ظاهرية؛ لا تثبت ownership/keyboard/async.
مراجعة فقط لا تعني تعديلًا. إذا طلب المستخدم إصلاحًا أيضًا، نفذه ضمن نطاقه بعد التشخيص.

## المراجع الانتقائية

المسارات من مجلد `SKILL.md` المثبت. اقرأ فقط ما يظهر في الشاشة أو العطل.
إذا غابت المعرفة المرجعية صرّح بذلك؛ لا تستنتج أنها قُرئت.

| الحاجة | المرجع |
|---|---|
| صياغة الملاحظات والدليل — الأساس | [Review criteria](../../flutter-knowledge/quality/review-checklists.md) |
| overflow/bounded axes/local size | [Constraints](../../flutter-knowledge/ui/constraints-and-sizing.md) |
| scroll/grid/page viewport | [Scrolling](../../flutter-knowledge/ui/scrolling-and-grids.md) |
| thresholds/resize/preservation | [Adaptive layouts](../../flutter-knowledge/ui/breakpoints-and-adaptive-layouts.md) |
| long text/scaler/readability | [Typography](../../flutter-knowledge/ui/typography-and-scaling.md) |
| crop/media/loading geometry | [Media](../../flutter-knowledge/ui/images-and-media.md) |
| RTL/focus/keyboard/SafeArea/input | [Platform and input](../../flutter-knowledge/ui/platform-accessibility-and-input.md) |
| owner/Provider يعاد | [Lifecycle](../../flutter-knowledge/state/lifecycle-and-di.md) |
| scenario/test لا يكفي | [Verification](../../flutter-knowledge/quality/testing-and-verification.md) |
| performance complaint مقاسة | [Performance](../../flutter-knowledge/quality/performance-and-rebuilds.md) |
| نسبة/version بحاجة مراجعة | [Source map](../../flutter-knowledge/source-map.md) |

## سير العمل

1. ثبّت نطاق الشاشة ومتطلبات الدعم وما الدليل المتاح؛ لا تفترض كل المنصات.
2. تتبع constraint/scroll path؛ ابحث عن local/window mix، unbounded axes،
   fixed sizes للمحتوى المتغير، shrinkWrap/Intrinsic بلا مبرر.
3. افحص strategy: threshold سببها المحتوى؟ shell والمكونات متسقة؟
   long text/scaler/RTL/media fit/actions reachable؟
4. افحص preservation عند structural change: owner/controller/focus/scroll وtrigger load.
   لا تكفي Keys وحدها ولا مجرد وجود LayoutBuilder.
5. اختَر scenario matrix حسب الخطر:
   ضيق وواسع وpanel ضيقة؛ عند/حول threshold؛ height قصيرة؛
   نص طويل/scale/RTL؛ keyboard/input؛ resize أثناء typing/loading/scroll.
6. نفذ المعاينة/tests المسموح بها إذا الأدوات متاحة.
   لا تدّع platform behavior من widget simulation أو static code فقط.
7. سجّل findings بالأثر والموقع والسيناريو والدليل والسبب والإصلاح والتحقق.
   صنف confirmed/probable/needs runtime verification؛ رتّب الأثر، واجمع السبب المشترك.
8. إذا الإصلاح مفوض، استخدم تنفيذًا متناسبًا وverification للحالة المتأثرة.
   إذا مراجعة فقط، سلّم findings وخطة تحقق دون edits.

## المخرجات ومعايير القبول

- matrix محددة مع ما نُفذ وما بقي.
- findings قابلة لإعادة الإنتاج أو دليل source مشروط واضح.
- fixes تحافظ على المعمارية وتفضيلات النص/input المطلوبة.
- لا «كل شيء ممتاز» اعتمادًا على screenshots قليلة.
- suggestions منفصلة عن bugs؛ لا universal breakpoints أو package جديدة كحل افتراضي.
- إن لم توجد مشكلة مؤثرة، اذكر نطاق الفحص وحدوده بإيجاز.

## حدود التداخل

هذا audit للشاشة. flutter-feature-review عندما الطلب مراجعة العقود والطبقات وتكامل الميزة أيضًا.
استعن بمعرفة lifetime حين تؤثر على resize، دون تحويل كل audit إلى architecture migration.
flutter-responsive-ui للتنفيذ عند تفويضه، لا تتطلب تشغيلها لمجرد قراءة findings.

## مثال طلب

«راجع هذه الشاشة عند تغيير حجم النافذة، والنص الكبير والكيبورد، وحدد المشاكل بأدلة وخطة إصلاح».
