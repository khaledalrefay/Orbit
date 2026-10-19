# Models وDTOs والتحويل الدفاعي

اقرأ عند ربط API أو تغيير response أو اتخاذ قرار فصل DTO/Entity.
لا تنشئ نموذجين متطابقين بلا منفعة واضحة.

## المحتويات

- المصدر والمعاني
- قرار الفصل
- parsing وعقد القيم
- مثال توضيحي
- حالات البيانات
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** M15 Data Models and DTOs وأجزاء model في M18 Bookly.
**[مراجعة KB]** TR-011 DTO/Entity، TR-023 parsing دفاعي، M10 حدود الفشل.
**[إضافة]** مثال ItemDto وجداول القبول التالية.
راجع [خريطة المصادر](../source-map.md).

## المعاني

DTO يعكس schema الخارجية: أسماء JSON، أنواع transport وnullable من الخدمة.
نموذج التطبيق يعكس ما تحتاجه الميزة ومعنى الحقول.
يمكن لنموذج بسيط واحد أداء الدورين إذا لا يسرّب schema غير مستقرة أو تفاصيل transport.
عندما توجد Domain مستقلة، يجب ألا تحتاج نماذجها إلى Flutter أو Dio.

الفصل يتيح أن تتغير API دون تغيير منطق العرض، لكنه يضيف mapping ومزيدًا من العقود.
لا تستخدم كلمات DTO/Entity كسبب مستقل لإضافة ملفات.

## قرار الفصل

| الوضع | قرار مبدئي | ما ينبغي فحصه |
|---|---|---|
| API صغيرة ومستقرة وحقولها تناسب الميزة | نموذج واحد أو DTO + نموذج بسيط حسب التنظيم | هل العرض يعتمد على أسماء transport؟ |
| عدة endpoints تمثل الكيان بتراكيب مختلفة | DTO لكل schema وتحويل لنموذج مناسب | معنى القيم عند الغياب |
| Domain مستقلة أو قواعد أعمال على النموذج | DTO في Data وDomain model مستقل | invariants دون import transport |
| تفاصيل كثيرة لا تعرضها القائمة | Summary model منفصل عند منفعة | هل هو عقد عرض أم تكرار غير مبرر؟ |
| مشروع قائم له code generation | اتبع نمطه | توافق generated files ونسخ generators |

حزم json_serializable/freezed اختيار مشروع يحتاج اعتمادًا وتحقق إصدار؛ لا تضفها تلقائيًا.

## سياسة parsing

لكل حقل صنّفه إلى required/optional وحدد نوعه المقبول.
- required ناقص أو بنوع غير صالح: فشل parsing واضح؛ لا تخفِ فساد البيانات بقيمة مزيفة.
- optional غير موجود: null أو fallback له معنى معتمد.
- optional بنوع خطأ: قرار صريح؛ غالبًا رفض القيمة/الاستجابة مع diagnostics، وليس cast أعمى.
- string فارغ قد يختلف عن null؛ لا تساوهما دون عقد.
- num قد يأتي int أو double؛ استخدم تحويلًا عدديًا مقصودًا.
- ID نصي قد يفقد معنى إذا حُوّل من رقم دون تأكيد schema.
- collections تحتاج معالجة صلاحية العناصر ومناعة من التعديل الخارجي.

مثال rating: غياب التقييم لا يعني تقييم 0؛ قد تعرض «لا يوجد تقييم».
السياسة تؤثر على UI وفرز البيانات، وليست تفصيل parsing فقط.

## مثال توضيحي

**[إضافة]** Dart 3+؛ fragment لنموذجين في Data/Application، دون مكتبة توليد:

```dart
class ItemSummary {
  const ItemSummary({
    required this.id,
    required this.title,
    this.rating,
  });

  final String id;
  final String title;
  final double? rating;
}

class ItemDto {
  const ItemDto({
    required this.id,
    required this.title,
    this.rating,
  });

  final String id;
  final String title;
  final double? rating;

  factory ItemDto.fromJson(Map<String, dynamic> json) {
    final id = json['id'];
    final title = json['title'];
    final rating = json['rating'];

    if (id is! String || id.trim().isEmpty) {
      throw const FormatException('Invalid item id');
    }
    if (title is! String || title.trim().isEmpty) {
      throw const FormatException('Invalid item title');
    }
    if (rating != null && rating is! num) {
      throw const FormatException('Invalid rating type');
    }

    return ItemDto(
      id: id,
      title: title,
      rating: (rating as num?)?.toDouble(),
    );
  }

  ItemSummary toModel() => ItemSummary(
        id: id,
        title: title,
        rating: rating,
      );
}
```

هذه الافتراضات تخص المثال: id/title غير فارغين، rating اختيارية وعددية.
لا يفترض المثال مدى rating؛ يضاف range validation إذا نص عقد الخدمة عليه.
سبب FormatException داخلي؛ يحوله Data boundary إلى failure آمنة ولا يظهر raw payload للمستخدم.
وجود نموذجين هنا لشرح حد التحويل، لا توصية باثنين لكل response.
إذا كانت القاعدة التجارية تمنع عنوانًا فارغًا، يجب التحقق كذلك عند الإنشاء المحلي المناسب.

## قائمة وعناصر غير صالحة

اختر سياسة معلنة:
| سياسة | فائدتها | خطرها |
|---|---|---|
| رفض response كلها | يحافظ على عقد قائمة متكاملة | عنصر واحد قد يمنع عرض الباقي |
| إسقاط invalid items مع diagnostics | يحافظ على بيانات صالحة | قد يخفي نقصًا مهمًا إن لم يُفصح عنه |
| عرض partial result مع warning | يجعل النقص مفهومًا | state وUX أكثر تعقيدًا |

لا تستخدم try/catch صامتة حول كل عنصر كحل عام.
إذا كان العدد يؤثر على قرار المستخدم، فإن dropping قد يضلل؛ ارجع إلى متطلبات المنتج.

## immutability وmapping

- `final` يمنع استبدال مرجع القائمة، لا تعديل محتوياتها.
- استخدم نسخة غير قابلة للتعديل عند تسليم قائمة كـstate snapshot.
- العناصر نفسها يجب أن تكون immutable إذا تعتمد المقارنة/selectors عليها.
- لا تحول DTO إلى View model مع BuildContext أو لون Theme داخل Data.
- اجعل formatting المرتبط باللغة في Presentation، والمعنى domain-specific في موقعه المعتمد.
- لا تحتفظ بنسختين متناقضتين من الحقل الخام والمنسق دون حاجة.

## حالات تحقق

| البيانات | النتيجة المطلوب تثبيتها |
|---|---|
| required موجود وصالح | parsing وmapping دون فقد |
| required غائب/نوع خاطئ | failure واضحة وآمنة عند boundary |
| rating غائبة | تبقى null، لا 0 مختلقة |
| rating int ثم double | كلاهما يعالج حسب العقد |
| قائمة مختلطة الصلاحية | تطبيق السياسة المعلنة بالضبط |
| field إضافي جديد | لا يكسر parsing ما لم يغير العقد |
| بيانات cache من schema قديمة | migration/invalidation عند الحاجة |

## التشخيص

| العَرَض | السبب المحتمل | المعالجة |
|---|---|---|
| crash عند cast | افتراض نوع transport | فحص النوع وboundary failure |
| UI يعرض قيمًا مضللة | default بلا معنى | nullable ومعنى عرض متفق |
| تغيير endpoint يغيّر Widgets كثيرة | schema تتسرب إلى UI | mapping وحد مناسب |
| تحديث state لا يظهر | قائمة/عنصر mutable أو مساواة ناقصة | snapshot ومقارنة تعتمد على القيم |
| DTO وEntity copies بلا اختلاف | فصل شكلي | تبسيط إذا يسمح قرار المشروع |

## تحقق الإصدار

نوع `abstract interface`/sealed أو pattern matching في مراجع أخرى يحتاج Dart 3+.
المثال يستخدم parsing يدويًا؛ تحقق أي generator أو annotation وفق نسخته إذا اختاره المشروع.
لم يُشغّل analyzer على المثال هنا.
