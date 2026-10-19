# ملكية الحالة واختيار Cubit أو Bloc

اقرأ عند تحديد أين تعيش قيمة، أو اختيار state flow، أو تشخيص مالكين متعارضين.
Cubit default للميزة، وليس شرطًا لكل قيمة في UI.

## المحتويات

- المصدر والقرار
- تعريف الملكية
- اختيار owner وأسلوب إدارة الحالة
- حدود التقسيم
- مثال بحث وتفاصيل
- التشخيص والتحقق

## المصدر والقرار

**[كورس بحسب KB]** M01–M06: State Management Fundamentals، setState vs BLoC vs Cubit،
BLoC/Cubit Fundamentals، BLoC vs Cubit، Events and States.
**[مراجعة KB]** TR-015 Cubit كـViewModel، TR-016 التقسيم وفق التنسيق والعمر.
**[قرار معتمد]** Cubit بداية المشاريع الجديدة؛ تغيير الخيار يحتاج مبررًا واعتمادًا.
**[استنتاج]** الفصل حسب lifetime وحقيقة مشتركة أوضح من Cubit لكل Widget.
الأصل والإصدارات في [source-map.md](../source-map.md).

## تعريف الملكية

مالك القيمة هو من يقرر تحديثها وعمرها ويقدم snapshot الموثوقة لمن يحتاجها.
وجود نسخ للعرض لا يعني مالكين مستقلين. إذا يمكن لنسختين أن تتغيرا منفردتين، حدد أيهما الحقيقة.
لكل قيمة مهمة اسأل:
1. من ينتجها ومن يعدلها؟
2. من يقرأها، وفي أي routes/components؟
3. ما الحدث الذي يعيد ضبطها؟
4. هل يجب أن تبقى عند resize أو العودة أو تغيير account؟
5. هل هي نتيجة بيانات، اختيار مستخدم، أم مورد UI محلي؟

## اختيار owner

| القيمة | بداية مناسبة | شرط أو استثناء |
|---|---|---|
| expansion مؤقت داخل Widget | setState/StatefulWidget | إذا لا توجد مشاركة أو قواعد ميزة |
| focus/controller/animation | UI state | dispose وفق عمر Widget |
| loading/results/failure/retry | Cubit الميزة | snapshot كاملة وأوامر معلومة |
| form draft | UI أو presentation state حسب المشاركة | مصدر حقيقة واحد؛ لا synchronize بلا عقد |
| selected ID في list/detail | owner يحيط بمن يحتاجه | عمر selection وURL يحددان scope |
| بيانات مشتركة/cached | Repository أو مصدر موثوق | policy واضحة، لا نسخ Cubits بلا تنسيق |
| width/keyboard/textScaler | UI environment | لا تضع قياسات البيئة في business state تلقائيًا |
| auth/session | scope تطبيق معتمد | لا تعمم كل الحالات الأخرى بسبب مشاركة auth |

يمكن للـcontroller أن يعكس state، لكن اتجاه الربط واضح لتجنب feedback loop.
ولا ينبغي لكل keystroke أن يحدث network أو حفظًا إلا إذا UX تتطلب ذلك.

## Cubit مقابل Bloc

| الحالة | Cubit مناسب | سبب النظر في Bloc |
|---|---|---|
| أوامر مباشرة وبسيطة للميزة | methods مثل load/retry/submit | ليس ضروريًا إضافة Events شكلية |
| workflows متعددة مع سياسة async | ممكن بسياسة صريحة لكل method | إذا جعل تنظيم event handlers التدفق أوضح |
| أحداث من مصادر كثيرة | ممكن subscriptions بعمر واضح | event model قد يوضح المصادر والتركيب |
| debounce/restartable/etc | يحتاج implementation أو abstraction معتمدة | transformers تساعد عند اعتمادها وإصدارها |
| مشروع قائم يعمل بـBloc | لا تهاجر تلقائيًا | اتبع النظام القائم وتحقق إصلاحه |
| حالة محلية شكلية | غالبًا لا حاجة | لا Cubit ولا Bloc شرط لها |

وجود transformer لا يعني أن Cubit غير قادر على التزامن.
ولا يعني استخدام Bloc أن كل الأحداث أصبحت sequential.
مقارنة المكتبات قرار هندسي حسب متطلبات واضحة، وليس منافسة أسماء.

## حدود التقسيم

افصل owner عندما تختلف:
- مسؤولية مستقرة، أو مصدر حقيقة، أو عمر.
- سياسة تحميل/تزامن يمكن عزلها بوضوح.
- مشاركة أو إعادة استخدام مثبتة.
- استجابة لمدخل مستقل لا يحتاج transaction مشتركة مع الآخر.

احتفظ بالتنسيق أو owner واحد عندما:
- الحقول يجب أن تتغير معًا كي تبقى snapshot صحيحة.
- تقسيمها يخلق subscriptions متبادلة أو duplication.
- لا يمكن للمستخدم التعامل مع جزء دون معرفة الجزء الآخر.
- الكلفة الجديدة أعلى من الفائدة في ميزة صغيرة.

حجم الملف أو عدد Widgets إشارات للفحص، وليسا معيار ملكية.

## مثال: قائمة وبحث وتفاصيل

**[إضافة]** SearchCubit يملك query والنتائج والتحميل؛ DetailsCubit يملك ID وبياناته.
Selection قد يأتي من route أو parent owner؛ حدد حقيقة واحدة له.
في عرض ضيق، التفاصيل route؛ في عرض واسع، قد تظهر beside list.
هذا لا يفرض مالكًا ضخمًا لكل حالات البحث والتفاصيل.
ولا ينبغي لنقل موضع list في layout أن يعيد SearchCubit إذا مطلوب بقاء query.

إذا إضافة favorites تغير القائمة والتفاصيل معًا، حدد عقد repository/invalidation أو owner مشترك مناسب.
لا تُزامن state copies بسلسلة listeners عشوائية.

## مثال local state

**[إضافة]** إظهار كلمة المرور واختيار tab مؤقت لا يستحقان Cubit إضافية تلقائيًا.
إذا tab جزء من URL/restore أو يحدد fetch/filter مشتركة، تصبح الملكية أوسع من Toggle محلي.
القرار يتبع المعنى والعمر، لا نوع القيمة bool/int.

## التشخيص

| العَرَض | الدليل المطلوب | اتجاه العلاج |
|---|---|---|
| نتائج تعود إلى قيمة قديمة | trace أوامر وowners وrequest identity | توحيد الحقيقة وسياسة async |
| resize يمسح draft | مكان إنشاء owner/controller | scope فوق branch المتغير |
| Cubits تستمع لبعضها بحلقة | اتجاه تنسيق وتبعيات | contract/coordinator أو owner واحد |
| كل Widget لها Cubit | منفعة فصل كل owner | حذف الفصل غير المبرر |
| state عالمية تحتفظ ببيانات route منتهية | scope ومَن يغلقها | تقليل العمر وإعادة الضبط المطلوبة |
| setState ينسق requests مشتركة معقدة | races ومشاركة وحالات failure | presentation state flow واضح |

## التحقق والقبول

- جدول القيم المهمة يوضح owner/readers/reset/lifetime.
- لا توجد حقيقتان مستقلتان دون synchronization contract مقصود.
- تغيّر العرض لا يغيّر العمر بلا requirement.
- كل اختيار Cubit/Bloc/local state له سبب مرتبط بالمهمة.
- لا package جديدة ولا migration بلا اعتماد مناسب.
- الاختبارات تثبت التنسيق المهم، لا مجرد وجود Cubit أو أسماء حالات.

## تحقق الإصدار

اختيار الأسلوب مفهوم؛ APIs الخاصة بـtransformers تتبع نسخ الحزم.
[Bloc.on](https://pub.dev/documentation/bloc/latest/bloc/Bloc/on.html) في bloc 9.2.1
يوضح التزامن الافتراضي للمعالجات؛ تحقق بتاريخ 2026-10-01.
تفصيل التزامن في [async-flows.md](async-flows.md).
