# تصميم state كاملة وimmutable

اقرأ عند تصميم state أو refresh أو empty/error، أو تشخيص equality/copyWith.
ابدأ بما يجب أن يستطيع View رسمه من snapshot واحدة.

## المحتويات

- المصدر
- اكتمال state
- اختيار الشكل
- مثال SearchState
- equality وcopy semantics
- التشخيص والقبول

## المصدر

**[كورس بحسب KB]** M06 Events and States وM04 Cubit Fundamentals.
**[مراجعة KB]** TR-017 snapshot كاملة، TR-021 initial مقابل empty،
وأجزاء immutability/equality في M06.
**[إضافة]** النموذج التالي والقيم التوضيحية.
[خريطة المصادر](../source-map.md) تحفظ حدود النسبة.

## ماذا يعني complete state؟

يجب أن يحدد state المعروضة معنى المرحلة والبيانات والفشل والمدخلات المهمة دون سر خفي في Cubit.
لا تعتمد View على حقل mutable خارج state لتعرف هل المعروض query قديمة.
الـresources مثل subscriptions/controllers ليست بيانات عرض ويجوز أن تكون خارج state بعمر معلوم.

اسأل عن السيناريوهات: initial، first load، success، success-empty، failure، refresh مع بيانات،
partial failure، تغيير input، repeated command، route exit.
لا تضف كل حالة إلى كل ميزة؛ غطّ ما يحدث فعلًا.

## اختيار الشكل

| الشكل | مناسب عند | فحص |
|---|---|---|
| sealed mutually exclusive states | مراحل متمايزة ذات payload مختلفة | هل Loaded→Loading يفقد بيانات ينبغي إبقاؤها؟ |
| data + status/flags + optional failure | refresh/pagination أو بيانات تبقى ظاهرة | منع combinations غير صالحة |
| hybrid variants تحمل بيانات مشتركة | مراحل واضحة مع retained content | بقاء payload كاملة دون تكرار |
| عدة booleans بلا invariants | بداية قد تبدو سهلة | قد تسمح loading+error+empty المتناقضة |

لا تختَر sealed لمجرد حداثتها؛ تتطلب Dart 3+.
Enum مع عقد واضح قد يكون كافيًا.
Empty بعد نجاح البحث تختلف عن initial قبل أول بحث.
عدم وجود بيانات لا يساوي عدم وجود نتائج مؤكدة.

## مثال حالة بحث

**[إضافة]** نموذج fragment يستعمل ItemSummary من عقد المشروع وAppFailure من مرجع الأخطاء.
يفترض UX: البحث الجديد يمسح النتائج السابقة؛ refresh الذي يبقيها يحتاج حالة أوسع.

```dart
enum SearchPhase { initial, loading, success, failure }

class SearchState {
  SearchState({
    this.query = '',
    this.phase = SearchPhase.initial,
    List<ItemSummary> items = const [],
    this.failure,
  }) : items = List.unmodifiable(items);

  final String query;
  final SearchPhase phase;
  final List<ItemSummary> items;
  final AppFailure? failure;

  bool get isEmptyResult =>
      phase == SearchPhase.success && items.isEmpty;
}
```

المنشئ لا يتحقق وحده من كل invariant؛ طرق Cubit هي التي تنشئ snapshots المسموحة في هذا المثال.
إذا كان الإنشاء منتشرًا أو الأخطاء محتملة، استخدم constructors/factories أو assertions مناسبة.
`failure` معناها آمن للعرض ومحدود، لا raw DioException.
العناصر يجب أن تكون immutable كذلك؛ `List.unmodifiable` وحدها لا تجمد عناصر mutable.

حالات مقبولة في هذا المثال:
| phase | query | items | failure |
|---|---|---|---|
| initial | فارغة | فارغة | null |
| loading | query مقبولة | فارغة | null |
| success | query الحالية | القائمة وقد تكون فارغة | null |
| failure | query الحالية | فارغة | failure آمنة |

## refresh وpagination

إذا مطلوب إبقاء بيانات أثناء refresh:
- فرّق first-load عن refreshing.
- أبقِ بياناتها وهوية المدخل المرتبطة بها.
- عرّف هل فشل refresh يعرض banner مع البيانات أم يستبدل الشاشة.
- عند pagination، current items ليست page جديدة وحدها؛ عرّف merge/dedup ونهاية القائمة.
- لا تستنتج hasMore من طول page إلا إذا نص contract عليه.
- لا تضع refreshing/pagination flags بلا منع عمليات متعارضة.

هذه توسعات عند الحاجة **[إضافة]**، وليست requirement لكل بحث.

## equality

Cubit يتعامل مع equality أثناء emits، وSelectors يقارنون القيمة المحددة.
Default identity equality قد يسمح emit لنسخة جديدة بالقيم نفسها؛ ليس انهيارًا لكنه يحتاج وعيًا.
إذا تتطلب الميزة مساواة قيمية، نفذها بطريقة المشروع، أو اعتمد حزمة عند منفعة واضحة.

| خطأ | النتيجة |
|---|---|
| استثناء field مهم من equality | تغيّر منطقي لا يلاحظ |
| list تعدّل in-place | snapshot سابقة تتغير وselectors قد لا يلاحظون |
| props/equality تشمل موارد UI mutable | مقارنة غير مستقرة ومسؤوليات مختلطة |
| اعتبار Equatable إلزامية | dependency لا تفرضها MVVM/Cubit |

النموذج أعلاه لا يعرّف equality قيمية؛ هذه حدود المثال.
اختبر semantics التي تعتمد عليها الميزة بدل إضافة مكتبة كحل تلقائي.

## copyWith وnullable

هذا النمط لا يسمح مسح nullable:
`failure: failure ?? this.failure`.
اختر semantics واضحة:
- `clearFailure: true` مع flag مضبوط.
- sentinel يفرق «لم يُمرّر» عن «مرّر null».
- method/factory انتقال باسم واضح.
- إعادة إنشاء state كاملة عندما أبسط.

لا تجعل call sites تخمّن معنى null.
مع انتقال loading جديد، لا تبقَ failure قديمة إلا إذا UX تقصد ذلك.

## التشخيص

| العَرَض | افحص | العلاج والتحقق |
|---|---|---|
| spinner يختفي والبيانات ناقصة | state تحمل status فقط وحقل data مخفي | snapshot كاملة واختبار display |
| خطأ قديم يبقى بعد retry | copyWith null لا يمسح | semantics واضحة واختبار الانتقال |
| empty يظهر قبل تحميل | initial==empty | مرحلة ومعنى منفصلان |
| selector لا يتحدث | mutation/equality | immutable selected value واختبار |
| refresh يمسح محتوى مطلوب | اختيار mutually exclusive بلا retained payload | state تحمل القديم وسلوك الفشل |
| query على الشاشة لا تطابق النتائج | هوية input غير ممثلة | query/request identity وسياسة stale |

## معايير قبول

- حالات العرض المهمة قابلة للرسم من state مباشرة.
- combinations المسموحة والانتقالات موثقة أو مقيدة.
- لا mutation خارجية تغير snapshot قديمة.
- equality وnullable clearing يتوافقان مع سلوك الميزة.
- empty/failure/initial محددة بالمعنى لا بمجرد list.isEmpty.
- لا abstraction إضافية دون حاجة.

## تحقق الإصدار

المفاهيم من القاعدة؛ [BlocSelector API](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/BlocSelector-class.html)
في flutter_bloc 9.1.1 يؤكد ضرورة selected value immutable؛ تحقق 2026-10-01.
الأمثلة لم تُحلل باستخدام Dart analyzer هنا.
