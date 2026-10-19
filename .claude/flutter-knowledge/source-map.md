# خريطة المصادر والإصدارات

الإصدار: 1.0.0. تاريخ التحقق الخارجي: 2026-10-01 UTC.
هذه خريطة منشأ المعرفة، وليست تعليمات تُحمّل كاملة في كل مهمة.
اقرأها عند التحقق من نسبة قرار إلى الكورس، أو تحديث معلومة، أو حل تعارض.
الفهرس البشري في [index.md](index.md).

## المحتويات

- حدود المصادر وتصنيف المعرفة
- عناوين قاعدتي المعرفة
- ربط المراجع بالموضوعات
- الوثائق والإصدارات المتحقق منها
- التصحيح المعروف والمعلومات المؤجلة
- طريقة التحديث

## حدود المصادر

تمت مراجعة الملفين المرفقين كاملين. لم تُراجع فيديوهات الكورسين أو شيفرة مشاريعهما الأصلية.
قاعدتا المعرفة تتضمنان مفاهيم منسوبة للكورسين، ومراجعات تقنية وإضافات وأمثلة كتبت لإعداد القاعدتين.
لذلك لا تعني عبارة «ورد في القاعدة» بالضرورة أنه قول حرفي من المدرّس.
الأمثلة الجديدة في هذه الحزمة موسومة؛ لا تُنسب إلى مشروع Bookly الأصلي.

| المصدر | الملف | حدود التغطية |
|---|---|---|
| M — MVVM وBLoC | Flutter_Advanced_Course_BLoC_and_MVVM_Knowledge_Base(1).docx | 24 عنوانًا رئيسيًا، 22 جدولًا، المراجعات التقنية TR-001 إلى TR-026 |
| R — Responsive UI | Responsive_UI_Course_Flutter_Knowledge_Base(1).docx | 18 عنوانًا رئيسيًا، 12 جدولًا، بما فيها إضافات Platform-Adaptive UI |

بصمة SHA-256 للمصدر M:
`7329850eba6e5180cde9911e991e10fbf98acd030a2e081b2a2a4e6343666320`

بصمة SHA-256 للمصدر R:
`516fa72d40b12fdf66ebcff9f6314b9aabce7137058d5670e7249dd33f9389c4`

الإحالة إلى عنوان القسم أدق من رقم صفحة DOCX الذي قد يتغير عند العرض.
أرقام دروس الكورس الواردة داخل القاعدة بيانات منقولة عنها؛ لم نتحقق منها مستقلًا.

## تصنيف المعرفة

| الوسم | معناه | كيف تتعامل معه |
|---|---|---|
| **[كورس بحسب KB]** | مفهوم نسبته القاعدة صراحة إلى شرح الكورس | يحتفظ بسياقه؛ ليس اقتباسًا حرفيًا أو إثباتًا من الفيديو |
| **[مراجعة KB]** | تصحيح، استكمال أو توسعة تقنية داخل القاعدة | لا تنسبه تلقائيًا إلى الكورس |
| **[استنتاج]** | نتيجة هندسية استخلصناها من عدة أجزاء | اعرض الأساس وحدود الاستنتاج |
| **[إضافة]** | مثال أو تنظيم أو تحسين أُنشئ لهذه المنظومة | افصله عن المصدر، ولا تجعله قرارًا جديدًا دون سند |
| **[قرار معتمد]** | اختيار المستخدم للمنظومة العامة أو اختيار لاحق موثق للمشروع | يحكم التنفيذ في نطاقه |

«متحقق منه» و«يحتاج تحقق» حالة زمنية مستقلة عن هذه الأوسمة.
قد تكون معلومة من الكورس صحيحة تاريخيًا وتحتاج مراجعة عند تغيير SDK أو مكتبة.

## المصدر M: خريطة العناوين

| الرمز | العنوان داخل المصدر | الاستخدام الأساسي |
|---|---|---|
| M00 | مقدمة وطريقة استخدام المرجع | حدود الأمثلة والإضافات والمراجعات |
| M01 | State Management Fundamentals | ملكية الحالة ومدخلات ومخرجات التدفق |
| M02 | setState vs BLoC vs Cubit | الحالة المحلية مقابل حالة الميزة |
| M03 | BLoC Fundamentals | الأحداث والمعالجات والانتقالات |
| M04 | Cubit Fundamentals | أوامر methods وانبعاث الحالة |
| M05 | BLoC vs Cubit | اختيار الأسلوب حسب التدفق |
| M06 | Events and States | حالات العرض والمساواة والتعامل مع الأحداث |
| M07 | BlocProvider and Dependency Injection | الإنشاء والملكية والإغلاق والاعتماديات |
| M08 | BlocBuilder BlocListener and BlocConsumer | العرض والتأثيرات وفلاتر التحديث |
| M09 | Async Operations in BLoC | التزامن والتكرار والإلغاء والنتائج القديمة |
| M10 | Error Handling and Failure States | حدود الأخطاء وتصنيفها ورسائلها |
| M11 | MVVM Fundamentals | مسؤوليات View وViewModel وModel |
| M12 | MVVM with BLoC | Cubit/Bloc في دور ViewModel |
| M13 | Clean Architecture Layers | اتجاه الاعتماديات وDomain الاختيارية |
| M14 | Repositories and Use Cases | العقود ومصادر البيانات ومنطق الاستخدام |
| M15 | Data Models and DTOs | parsing وDTO/Entity والتحويل |
| M16 | Testing BLoC and MVVM | توسعة الاختبارات ومعايير السلوك |
| M17 | Performance and Rebuild Optimization | نطاق التحديث والقياس |
| M18 | تطبيق المفاهيم في Bookly والواجهات المساندة | الربط والتنقل والخدمات والواجهات |
| M19 | Common Problems and Solutions | التشخيص وأعراض التكامل |
| M20 | Decision Guides | المفاضلات |
| M21 | مراجع الكورس والتحديثات التقنية | مصدر النسبة إلى الدروس والمراجعات TR |
| M22 | Quick Reference | الوصول المختصر |
| M23 | Final Best Practices Checklist | فحص ختامي مشروط بالسياق |

المراجعات الأكثر تأثيرًا في الحزمة:
TR-002 فصل العرض عن التأثيرات؛ TR-003 ملكية Provider؛ TR-008 طبقات متناسبة؛
TR-010 التنقل بالمعرّفات؛ TR-011 DTO/Entity؛ TR-012 العقود؛
TR-013 وTR-014 الأخطاء وEither؛ TR-015 Cubit بوصفه ViewModel؛
TR-016 تنسيق الحالة وأعمارها؛ TR-017 اكتمال الحالة؛ TR-018 التكرار والنتائج القديمة والإلغاء؛
TR-019 وTR-020 عمر الاعتماديات وconstructor injection؛
TR-021 initial/empty؛ TR-022 دقة رسائل الفشل؛ TR-023 parsing دفاعي؛
TR-024 دورة تحميل التفاصيل وتغيّر ID؛ TR-025 وTR-026 التكامل الخارجي وawait/mounted.

## المصدر R: خريطة العناوين

| الرمز | العنوان داخل المصدر | الاستخدام الأساسي |
|---|---|---|
| R00 | مقدمة وطريقة الاستخدام | حدود الكورس والتوسعات |
| R01 | Core Concepts of Responsive UI | logical pixels والتجاوب والتكيّف |
| R02 | Layout System in Flutter | القيود والحجم والتموضع |
| R03 | MediaQuery vs LayoutBuilder | نافذة التطبيق مقابل مساحة المكوّن |
| R04 | Constraints and Sizing | الأبعاد المحدودة والنسب والقياسات |
| R05 | Flexible Layout Widgets | Expanded/Flexible وWrap وتوسعة Flow |
| R06 | Scrolling and Slivers | القوائم والشبكات والتمرير |
| R07 | Responsive Typography | Theme وتغليف النص وTextScaler |
| R08 | Responsive Images and Media | AspectRatio وBoxFit وحالات الوسائط |
| R09 | Adaptive Layouts and Breakpoints | التغيير الهيكلي والعتبات |
| R10 | Platform-Adaptive UI | توسعة التكيّف مع المنصة والمدخلات |
| R11 | Accessibility and Usability | RTL والنص والفوكس والمناطق الآمنة |
| R12 | Performance Considerations | القياس وإعادة الاستخدام والتحقق |
| R13 | Common Problems and Solutions | أعراض القيود والنص والتمرير |
| R14 | Decision Guides | المفاضلات |
| R15 | Quick Reference | الوصول المختصر |
| R16 | Final Best Practices Checklist | فحص ختامي حسب الدعم |
| R17 | Course References and Technical Sources | إحالات الدروس والوثائق والتوسعات |

لا نحول قيمًا تعليمية مثل 400/700/1000 أو أي تقسيم Tablet/Desktop إلى عتبات عامة للمشاريع.
لا نحول هيكل شاشة تعليمية أو أسماء ملفات Bookly إلى قالب إلزامي.

## ربط المراجع بالمصدر

| المرجع | أساسه في المصدر | الإضافات أو الاستنتاجات في الحزمة |
|---|---|---|
| architecture/mvvm-and-layers.md | M11–M14، M18، TR-008/015 | جدول مسؤوليات ومثال feature-first متناسب |
| architecture/repositories-and-use-cases.md | M14، TR-012/013 | مفاضلات العقود وسياسة cache والتنسيق |
| architecture/models-and-dtos.md | M15، TR-011/023 | مثال parsing مع فشل واضح وحالات تحقق |
| architecture/routing-and-integration.md | M18، TR-010/024–026، R09 | أمثلة بحث وتفاصيل ونموذج متكيّف |
| state/ownership-and-cubit-bloc.md | M01–M06، TR-016 | شجرة قرار الملكية ومنع تضخم التقسيم |
| state/state-design.md | M06، TR-017/021 | مثال حالة كاملة دون حزمة equality إضافية |
| state/lifecycle-and-di.md | M07، TR-003/019/020، R09 | فحص أعمار routes والمكوّنات المتبدلة |
| state/async-flows.md | M09، TR-018، M03 | مثال latest-wins، جدول سياسات لكل عملية |
| state/errors-and-results.md | M10، TR-013/014/022 | تصحيح Dio الحالي وسياسة تشخيص آمنة |
| state/ui-binding-and-effects.md | M08، TR-002، M17 | منع التأثير المكرر وفحص initial/rebuild |
| ui/constraints-and-sizing.md | R01–R05 | تتبع constraint path ومثال local width |
| ui/scrolling-and-grids.md | R06، R12–R13 | تشخيص ownership وfinite viewport |
| ui/breakpoints-and-adaptive-layouts.md | R09، R03، R11 | بروتوكول اختيار عتبة وحفظ بيانات النموذج |
| ui/typography-and-scaling.md | R07، R11 | فصل design scaling عن system scaling |
| ui/images-and-media.md | R08، R11 | سياسة crop وتأثير الخطأ والتحميل |
| ui/platform-accessibility-and-input.md | R10–R11، R03 | مصفوفة input/focus/keyboard/RTL |
| quality/testing-and-verification.md | M16، R12، M09 | أمثلة تحقق حتمية ومصفوفة حدود متناسبة |
| quality/performance-and-rebuilds.md | M17، R12، TR-009 | التشخيص قبل التحسين |
| quality/review-checklists.md | M19–M23، R13–R16 | نموذج دليل ونتيجة مراجعة موحد |

## الوثائق والإصدارات المتحقق منها

هذه لقطة تحقق، وليست متطلبات dependency pins.
افحص `pubspec.yaml` و`pubspec.lock` ونسخة SDK الفعلية قبل نسخ API حساس للإصدار.

| الموضوع | الوثيقة الرسمية | النسخة/حد التحقق |
|---|---|---|
| Cursor Rules | [Rules](https://cursor.com/docs/rules) | وثائق Cursor بتاريخ 2026-10-01؛ توافق واجهة 3.22.12 يحتاج اختبارًا محليًا |
| Cursor Skills | [Skills](https://cursor.com/docs/skills) | المسار العام ~/.cursor/skills، SKILL.md وname/description والاستدعاء / |
| بنية Skill | [Agent Skills specification](https://agentskills.io/specification) | اسم مطابق للمجلد، وصف موجز، معرفة عند الحاجة |
| معمارية Flutter | [Architecture guide](https://docs.flutter.dev/app-architecture/guide) | للتحقق من المسؤوليات، لا لفرض قالب إضافي |
| التجاوب | [Adaptive and responsive general approach](https://docs.flutter.dev/ui/adaptive-responsive/general) | الوثائق المعروضة تشير إلى Flutter 3.47؛ مشروعك قد يستخدم غيرها |
| القيود المحلية | [LayoutBuilder](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html) | BoxConstraints؛ صفحة API لا تثبت SDK مثبتًا عند المستخدم |
| TextScaler | [Migration](https://docs.flutter.dev/release/breaking-changes/deprecate-textscalefactor) و[getter](https://api.flutter.dev/flutter/widgets/MediaQueryData/textScaler.html) | TextScaler مستقر منذ Flutter 3.16؛ النظام قد يستخدم scaling غير خطي |
| ملكية Provider | [BlocProvider](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocProvider-class.html) | flutter_bloc 9.1.1 |
| التأثيرات والاختيار | [BlocListener](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocListener-class.html) و[BlocSelector](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocSelector-class.html) | flutter_bloc 9.1.1 |
| معالجة الأحداث | [Bloc.on](https://pub.dev/documentation/bloc/latest/bloc/Bloc/on.html) | bloc 9.2.1؛ التزامن الافتراضي داخل معالج نوع الحدث |
| restartable | [bloc_concurrency](https://pub.dev/documentation/bloc_concurrency/latest/bloc_concurrency/restartable.html) | bloc_concurrency 0.3.0؛ إلغاء معالج ليس ضمانًا لإلغاء HTTP |
| Dio errors | [DioExceptionType](https://pub.dev/documentation/dio/latest/dio/DioExceptionType.html) و[changelog](https://pub.dev/packages/dio/changelog) | Dio 5.11.1؛ transformTimeout أضيف في 5.10.0 |
| إلغاء Dio | [CancelToken](https://pub.dev/documentation/dio/latest/dio/CancelToken-class.html) | Dio 5.11.1 |
| التنقل | [go_router](https://pub.dev/packages/go_router) و[GoRouter](https://pub.dev/documentation/go_router/latest/go_router/GoRouter-class.html) | go_router 18.0.2 |
| أدوات widget tests | [WidgetTester](https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html) | API tester.view؛ أمثلة الاختبار لم تُشغّل هنا |

## تصحيح معروف

**KNOWN-DIO-01 — switch قديم لا يغطي enum الحالي.**

قسم M10 يتضمن مثال mapDioFailure مع ثمانية أنواع؛ Dio 5.11.1 يتضمن أيضًا
`DioExceptionType.transformTimeout`. أضافته المكتبة في 5.10.0.
الاستنتاج: switch expression exhaustive بالأنواع الثمانية لا يغطي enum في هذه النسخة.
السند: تعريف enum وchangelog و[قواعد switch في Dart](https://dart.dev/language/branches).
هذا استنتاج من الشيفرة والوثائق؛ لم يُثبت بتشغيل analyzer هنا.
النسخة المصححة موجودة في [مرجع الأخطاء](state/errors-and-results.md).
لم تُعدّل ملفات المصدر الأصلية.

## ما يحتاج تحقق عند الاستخدام

- Flutter/Dart ونسخ الحزم الفعلية لكل مشروع؛ أمثلة sealed class تتطلب Dart 3+.
- وجود Skills في واجهة Cursor المثبتة، وقراءة مسارات المراجع المشتركة منها عمليًا.
- أي API لحزم اختيارية مثل get_it وinjectable وdartz وScreenUtil وflutter_svg وurl_launcher وexpandable_page_view.
- إعدادات المنصات والروابط الخارجية والويب وdeep links وأذونات التطبيق.
- سلوك platform-adaptive widgets المحدد؛ كلمة adaptive لا تثبت تكيّف كل خصائص Widget.
- دعم المنصات واللغات وحجم النص ونوع الإدخال ومتطلبات الوصول في المشروع.

لا تضف تلك الحزم أو تُحدّثها استنادًا إلى وجود اسمها في الكورس أو المرجع.
الأمثلة هنا لم تُبنَ أو تُشغّل باستخدام Flutter/Dart في بيئة إعداد الحزمة.

## طريقة التحديث

1. حدد الموضوع المتغير، نسخة المشروع، ومصدرًا رسميًا ملائمًا لها.
2. حدث المرجع المتأثر، لا جميع Skills التي تشير إليه.
3. احتفظ بوسم المنشأ، وأضف نسخة/تاريخ التحقق وسبب التصحيح هنا.
4. افحص أثر التغيير على أمثلة المرجع وعلى القرارات المعتمدة؛ اطلب قرارًا فقط إذا غيّرها.
5. أعد فحص الروابط والسيناريو المتأثر في Cursor والمشروع.
6. ارفع إصدار الحزمة عند التسليم، مع وصف مختصر للتغيير؛ لا تعلن تشغيلًا لم يحدث.
