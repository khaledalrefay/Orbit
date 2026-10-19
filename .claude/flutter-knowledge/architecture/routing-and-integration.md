# Routing والتكامل عبر عمر الحالة

اقرأ عند إنشاء routes أو فتح تفاصيل أو ربط list/detail أو حفظ state مع adaptive layout.
go_router خيار البداية المعتمد؛ تفاصيل URL والمنصات تُحسم للمشروع.

## المحتويات

- المصدر والقرار
- المعرّف وعقد الدخول
- عمر Router وCubit
- أمثلة التكامل الثلاثة
- الأخطاء والتشخيص
- التحقق والإصدارات

## المصدر والقرار

**[كورس بحسب KB]** M18 Bookly وأجزاء navigation وurl_launcher.
**[مراجعة KB]** TR-010 ID للتنقل، TR-024 تغير ID والعمر، TR-025/026 التكامل الخارجي وawait/mounted.
**[استنتاج]** R09 adaptive layouts مع M07 lifetime: تغير العرض لا ينبغي أن يعيد ملكية بيانات الميزة دون مطلب.
**[إضافة]** أمثلة list/search وdetails/form أدناه.
**[قرار معتمد]** go_router default؛ لا هجرة تلقائية أو pin إلى نسخة المرجع.
المصدر التفصيلي في [source-map.md](../source-map.md).

## عقد الدخول إلى التفاصيل

| مدخل | استخدام مناسب | حدوده |
|---|---|---|
| path ID | هوية دائمة لصفحة تفاصيل | تحقق صلاحيته وnot-found عند تحميله |
| query parameters | بحث/فلترة/خيارات يمكن تمثيلها في URL | parsing ومعنى default والغياب |
| extra object | بيانات مريحة أو seed عند انتقال داخلي | لا تعتمد وحدها على بقائها عند reload/deep link |
| shared in-memory state | تنسيق تجربة داخل session | ليس مصدرًا دائمًا لمعرف URL |

يدخل المستخدم مباشرة إلى `/items/:id` دون المرور بالقائمة.
لذلك يجب أن تعمل التفاصيل من ID والعقد، حتى إذا لم توجد extra.
إذا كان extra اختياريًا، استخدمه seed فقط وفق freshness policy معلومة.
لا تستنتج هوية العنصر من index في قائمة قد يتغير ترتيبها.

## Router وعمر الاعتماديات

أنشئ Router/config في scope مستقر وفق التطبيق؛ لا تنشئه داخل build المتكرر.
أغلق الموارد التي يملكها ذلك scope عند نهايته، ولا تغلق borrowed dependencies.
حدد أين تنشأ DetailsCubit: route owner، parent مشترك، أو shell عند تنسيق فعلي.
`go` و`push` يغيران بنية history/navigator بشكل مختلف؛ اختر بحسب UX وback behavior.
لا تستنتج عمر Cubit من كلمة push وحدها: shell/nesting/key قد يغير البقاء.

الحاجة ليست تخزين Router كـglobal static دائم؛ الحاجة عمر مقصود ومستقر وقابل للاختبار.
تفاصيل DI في [lifecycle-and-di.md](../state/lifecycle-and-di.md).

## تغير ID

إذا بقي Widget/owner بينما تغير route parameter:
| اختيار | مناسب عند | كيفية التحقق |
|---|---|---|
| owner جديد keyed بالـID | نحتاج state جديدة بالكامل لكل عنصر | old owner يغلق مرة، الجديد يحمل مرة |
| owner مستمر مع load(id) | موارد مستمرة أو تعديل refresh متعمد | didUpdate/route input trigger يغيّر ID ويفرض سياسة stale |
| shared details cache | إعادة استخدام بيانات ذات عقد واضح | عزل IDs وfreshness وعدم overwrite متأخر |

Keys قد تفرض replacement مقصودًا؛ لا تحمي العنصر إذا أزيل أصلًا من الشجرة.
لا تعتمد على initState وحدها إذا يمكن أن يتغير id مع بقاء نفس instance.
الـID الحالي جزء من هوية الطلب حتى لا تعرض استجابة العنصر السابق.

## مثال 1: قائمة وبحث

**[إضافة]** سيناريو عمل، وليس نقلًا من الكورس:
1. route قائمة تملك SearchCubit وquery الحالية حسب عمر مطلوب.
2. input UI يستدعي search عند قبول query، ويملك controller محليًا.
3. latest-wins للبحث، مع empty/clear/failure policy معلومة.
4. النتيجة تحمل IDs مستقرة.
5. tap يفتح تفاصيل ذلك ID.
6. العودة تحفظ query/scroll فقط إذا تقرر ذلك في تجربة المنتج وبقاء owner مناسب.
7. تغيير العرض أثناء البحث لا ينشئ Cubit جديدة أو يفقد query.

التأخير debounce وإلغاء HTTP وسياسة تجاهل stale ثلاثة أشياء مختلفة.
لا تعد بأن هذا السيناريو يحتفظ بكل حالة route إذا هيكل التنقل لا يفعل ذلك.

## مثال 2: تفاصيل ID

**[إضافة]** مسار بيانات من ID:
- validate input؛ تعامل مع missing/not-found وفق UX.
- load من Repository؛ لا تشترط object من القائمة.
- initial/loading/failure/loaded تكون complete.
- retry يعيد current ID.
- ID جديد يبطل صلاحية النتيجة القديمة قبل إصدارها.
- responsive list/detail split قد يشارك selection دون دمج كل حالة البحث والتفاصيل.

يمكن أن يكون split view View تركيبًا لمالكين لهما أعمار مختلفة؛
حدد من يقرر selection ومن يعالج missing item كي لا توجد حقيقتان مستقلتان.

## مثال 3: نموذج متكيّف يحفظ البيانات

**[إضافة]** form يستخدم عمودًا واحدًا في الضيق وعمودين عندما يسمح المحتوى:
- owner/controllers فوق فرع LayoutBuilder إذا مطلوب بقاء المدخلات.
- submit Cubit ينسّق الإرسال؛ focus/selection موارد UI.
- تغيير layout لا يعيد init أو يرسل submit.
- text scaling/keyboard/RTL قد يقلل المساحة المفيدة؛ قرار العرض محلي.
- pending submit: سياسة تكرار واضحة، وnavigation بعد نجاح من effect owner واحد.
- route exit أثناء submit يحتاج قرارًا: هل العملية تستمر وهل يمكن إلغاؤها؟
- لا تفترض إلغاء write في الخادم لأن المستخدم خرج من route.

تفاصيل الحفظ في [breakpoints-and-adaptive-layouts.md](../ui/breakpoints-and-adaptive-layouts.md)
والعمليات في [async-flows.md](../state/async-flows.md).

## الربط بالخدمات الخارجية

إذا استعمل المشروع url_launcher أو خدمة منصة:
- افحص نسخة الحزمة وإعداد كل منصة فعليًا.
- انتظر Future وتعامل مع النتيجة والفشل؛ لا تفترض فتح URL.
- إذا استخدمت BuildContext بعد await، افحص mounted في موضع UI المناسب.
- لا تجعل Repository يقرر فتح تطبيق خارجي.
- لا تظهر URL/خطأ خام أو credentials في diagnostics للمستخدم.

هذا ليس اعتمادًا للحزمة أو لإعدادات platform مجهولة؛ يضاف عند طلب فعلي.

## التشخيص

| العَرَض | افحص | التصحيح والتحقق |
|---|---|---|
| تفاصيل لا تعمل بعد reload | dependence على extra فقط | ID contract واختبار direct URL |
| العنصر القديم يظهر لحظيًا أو نهائيًا | input identity/stale policy | ID في owner/request واختبار completion معكوس |
| resize يمسح form أو query | owner تحت adaptive branch | رفع الملكية واختبار resize أثناء إدخال |
| network يعاد عند كل rebuild | load في build أو Router/Provider غير مستقر | trigger وعمر واضحان |
| success يفتح صفحة مرتين | effect owners مكررون | owner واحد واختبار transition واحد |
| back يفقد حالة متوقعة | اختيار go/push/shell غير مطابق لـUX | تثبيت السلوك المطلوب واختباره |

## معايير قبول وتحقق

- route contract موثق ويدعم نقاط الدخول المطلوبة.
- ID/current input وتغيرهما جزء من اختبار lifecycle/async.
- عمر Router/Cubit ومَن يغلقهما معلوم.
- resize يحفظ فقط الحالة التي اتفق المنتج على حفظها.
- error/not-found/retry/back حالات مقصودة.
- tests لا تفترض browser reload أو deep-link setup من مجرد نجاح navigation داخل التطبيق.

## حالة الإصدار

قورن `go` و`push` وعمر config مع [GoRouter API](https://pub.dev/documentation/go_router/latest/go_router/GoRouter-class.html)
و[صفحة الحزمة](https://pub.dev/packages/go_router) — go_router 18.0.2، بتاريخ 2026-10-01.
لا توجد هنا إعدادات منصة نهائية أو شيفرة Router كاملة؛ يلزم التحقق في مشروع فعلي.
