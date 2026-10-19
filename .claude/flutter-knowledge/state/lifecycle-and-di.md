# Lifecycle وDI وملكية الإغلاق

اقرأ عند إنشاء Provider أو مشاركة instance أو تشخيص requests/resources باقية.
DI أسلوب لتوضيح الاعتماديات؛ لا يوجب get_it أو injectable.

## المحتويات

- المصدر
- create مقابل value
- الأعمار وتركيب الاعتماديات
- triggers ودورة async
- التكيّف والتنقل
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** M07 BlocProvider and Dependency Injection وM18 service locator في Bookly.
**[مراجعة KB]** TR-003 Provider ownership، TR-019 lifetime، TR-020 constructor/composition،
TR-024 input changes، TR-026 await/mounted.
**[استنتاج]** R09 حفظ owner فوق تغيّر layout.
**[إضافة]** الجداول وأمثلة العقود.
[خريطة المصادر](../source-map.md).

## BlocProvider: create وvalue

| النمط | الملكية | السلوك والتحقق |
|---|---|---|
| `BlocProvider(create: ...)` | Provider يملك instance الذي أنشأه | يغلقه عند انتهاء scope؛ الإنشاء lazy افتراضيًا |
| `BlocProvider.value(value: existing)` | مستعير لinstance موجودة | لا يغلقها؛ owner الأصلي مسؤول |
| إنشاء instance جديدة داخل value | ملكية مبهمة | تجنبه؛ create مناسب للملكية الجديدة |
| borrowed instance من scope انتهى | value لا يمدد عمرها | إصلاح owner الحقيقي، لا مجرد تغيير constructor |

`lazy: false` يغيّر وقت الإنشاء؛ لا يعالج scope خاطئة.
عدد Providers ليس عدد state owners بالضرورة؛ قد تعيد نشر نفس instance.
افحص أين أنشئت ومَن يغلقها، لا مكان context.read وحده.

## حقن constructor

**[إضافة]** fragment:
```dart
class DetailsCubit extends Cubit<DetailsState> {
  DetailsCubit({required ItemsRepository repository})
      : _repository = repository,
        super(DetailsState.initial());

  final ItemsRepository _repository;
}
```

`DetailsState` هنا عقد مشروع غير معرّف في المقطع.
المغزى: dependency مرئية ويمكن fake في اختبار؛ لا استدعاء locator مخفي في method.
الـcomposition root ينشئ implementation ويمرره.
اختيار container أو factory أو singleton مبني على الحاجة والعمر؛ أسماء التسجيل ليست قواعد عامة.

## جدول الأعمار

| المورد | عمر محتمل | سؤال حاسم |
|---|---|---|
| Dio configured client | app/session أو feature خاص | من يغلقه وما إعداد العزل المطلوبة؟ |
| Repository/cache | بحسب حقيقة البيانات والحساب | هل data تتغير عند logout؟ |
| SearchCubit | route/feature | هل query تبقى عند back؟ |
| DetailsCubit | ID/route | هل ID يتغير مع نفس instance؟ |
| controller/focus | Widget owner | هل يبقى عند adaptive branch؟ |
| subscription/timer | owner الذي بدأه | هل cancel عند close/replace؟ |

Singleton ليست أداء أفضل تلقائيًا، وfactory ليست دائمًا scope صحيحة.
لا تغلق dependency مشتركة من Cubit لمجرد أنها تستخدمها.
المورد المنشأ خارجيًا يظل مملوكًا للخارج ما لم عقد النقل واضح.

## بدء التحميل

اختر trigger معلومًا:
- عند إنشاء Cubit المملوكة إن هذا عقد الميزة.
- initState أو route input hook في UI حين يناسب التكوين.
- user command أو subscription معلومة.
- تغيير ID/query الذي يقبل كمدخل جديد.

لا تشغله داخل build؛ ولا من initState ثم constructor معًا.
`create: (_) => cubit..load()` fragment شائع، لكن إذا lazy ولم تُقرأ Cubit قد يتأخر التحميل.
هذا لا يثبت bug إلا إذا مطلوب بدء الحمل قبل أي reader.

## async بعد نهاية scope

- ألغِ timers/subscriptions التي يملكها owner.
- أبطل صلاحية النتائج المتأخرة وفق operation identity.
- `isClosed` يمنع إصدارًا إلى owner مغلق؛ لا يلغي HTTP ولا يحدد آخر query.
- عند awaited UI action، تحقق mounted قبل استعمال context/resources بعد gap.
- يُقرَر استمرار mutation بعد خروج route بناء على contract، لا افتراض إلغاء عمل الخادم.

تفصيل الفرق بين stale/cancel في [async-flows.md](async-flows.md).

## التكيّف والتنقل

إذا branch narrow/wide تنشئ Provider مستقلة لكل واحد، قد تعاد state عند resize.
ارفع owner المشترك إلى ancestor ثابت إذا preservation مطلوب.
لا ترفع كل حالة إلى app root لمجرد حل فقدان قيمة محلية.

عند نشر instance إلى route جديد بـvalue:
- هل سيبقى owner الأصلي حيًا؟
- من يغلقه عندما تخرج route؟
- هل route الجديدة قد تتجاوز عمر route الأصلية؟
- هل أصلًا نحتاج shared owner أم Repo/ID contract أوضح؟

راجع [routing-and-integration.md](../architecture/routing-and-integration.md).

## التشخيص

| العَرَض | الدليل | التصحيح |
|---|---|---|
| emit after close | request/timer callback بعد disposal | lifecycle guard + cancellation/identity بحسب العملية |
| load مرتان | triggers متعددة أو إعادة إنشاء scope | owner وtrigger واحد مقصود |
| data تختفي عند resize | Provider/controller تحت branch | owner ثابت مع اختبار حفظ |
| memory/subscription باقية | owner لم يلغِ ما أنشأه | close/dispose واختبار إنهاء |
| route يستعمل Cubit مغلقة | value استعار من scope انتهى | عمر حقيقي مناسب |
| اختبار Cubit يحتاج global locator | dependency خفية | constructor injection |
| logout يعرض بيانات حساب سابق | Repository/cache بعمر خاطئ | عزل/إبطال حسب هوية الحساب |

## معايير قبول

- لكل resource owner وعمر وإغلاق معلوم.
- create/value مستخدمان وفق الملكية الحقيقية.
- من يملك dependency يغلقها، دون double-close أو تسرب.
- trigger load لا يتكرر مع rebuild/resize بلا مطلب.
- IDchange وroute exit وasync completion حالات مختبرة عند صلتها.
- لا locator/container جديد دون قرار واعٍ.

## تحقق الإصدار

[BlocProvider API](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocProvider-class.html)
— flutter_bloc 9.1.1، تحقق 2026-10-01: create owned/lazy مقابل value borrowed.
أي get_it/injectable API أو توليد كود يحتاج نسخة المشروع وتحقيقًا مستقلًا.
