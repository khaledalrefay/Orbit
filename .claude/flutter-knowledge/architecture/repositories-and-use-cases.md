# Repositories وUse Cases

اقرأ عند اختيار عقد بيانات أو cache أو توزيع التنسيق بين Cubit وDomain.
لا تنشئ Use Case لكل method تلقائيًا.

## المحتويات

- المصدر وحدود العقد
- ماذا يقرر Repository
- متى تستحق Use Case
- مكان العقد وأشكال النتائج
- مثال وسيناريوهات
- التشخيص والقبول

## المصدر

**[كورس بحسب KB]** M14 Repositories and Use Cases وM18 أجزاء API/ApiService وrepo في Bookly.
**[مراجعة KB]** TR-012 عقد Repository، TR-013 Either خيار، M13 Domain المتناسبة.
**[إضافة]** الجداول والعقد التوضيحي أدناه.
راجع [خريطة المصادر](../source-map.md) عند الحاجة إلى النسبة الدقيقة.

## حدود Repository

Repository يقدم عملية مفهومة للميزة، مثل searchItems أو loadDetails.
يحجب عنوان endpoint وDio وJSON عن العرض، ويحدد عقد النجاح والفشل.
قد ينسّق Remote/Local أو cache؛ ذلك يحتاج سياسة صريحة، وليس مجرد تخزين عشوائي.
Data Source يعالج مصدرًا محددًا؛ Repository يقرر كيف يستعمل مصادره وفق سياسة التطبيق.

| قرار | مكانه | سؤال يجب حسمه |
|---|---|---|
| HTTP headers وbaseURL وparsing | transport/Data Source | ما عقد الخدمة وإعداداتها؟ |
| أي مصدر يقرأ وأي نتيجة تحفظ | Repository | ما مصدر الحقيقة ومدة صلاحية البيانات؟ |
| حالة loading/refresh وإظهار القديم | Cubit + متطلبات UX | هل تبقى البيانات مرئية أثناء التحديث؟ |
| قاعدة صلاحية عملية أعمال مركبة | Use Case عند وجودها | هل القاعدة مشتركة/مستقلة عن الشاشة؟ |
| كيفية رسم error/banner/retry | UI وفق state | ما السلوك المتفق عليه؟ |

لا تجعل Repository يقرر snackbar أو route؛ لا يملك BuildContext.
ولا تجعل Cubit يختار endpoints أو يفسر response transport.

## cache ومصدر الحقيقة

عند الحاجة الفعلية، حدد:
- المفتاح: ID/query/filters والهوية اللازمة لعزل البيانات.
- الصلاحية: timestamp/version أو trigger معلوم، لا مدة اعتباطية.
- استراتيجية العرض: network-first أو cache-first أو stale-while-revalidate.
- التحديث والإبطال: بعد mutation، logout أو تبدل حساب.
- الفشل: هل يمكن عرض cached data مع warning؟ أم لا يجوز حسب المنتج؟
- التزامن: من يمنع writes قديمة من استبدال نتائج أحدث؟

هذه أمثلة خيارات **[إضافة]**؛ لا تعني اعتماد offline أو حزمة cache في كل مشروع.
الـcache العامة المشتركة تحتاج عقدًا حتى لا تصبح Cubits مالكي نسخ متعارضة.

## متى تستحق Use Case

| دليل الحاجة | توصية | مثال |
|---|---|---|
| طلب واحد وتحويل بسيط | Repository مباشرة من Cubit | قائمة عناصر |
| سلوك متكرر بقاعدة مستقلة | Use Case | حساب أهلية إجراء من أكثر من مصدر |
| workflow يجمع عمليات وفشلًا جزئيًا | Use Case أو coordinator واضح | حفظ طلب ثم تحديث رصيد مع سياسة تعويض |
| كل ما يفعله wrapper هو إعادة نفس القيمة | لا تضفه مبدئيًا | FetchItems يعيد repo.fetchItems فقط |
| المشروع اعتمد Use Cases لتنظيم واضح | اتبع القرار | لا تلغها في تغيير محدود |

تعقيد method وحده لا يكفي. حدد ما إذا كان التعقيد transport أو presentation أو business.
تنسيق تزامن search عادة Presentation؛ لا يتطلب Domain لمجرد كونه async.
حدود transaction أو atomicity تحتاج عقد الخدمة؛ لا تعد بها عند جمع calls مستقلة.

## مكان العقد

| البنية | مكان مناسب | قيد |
|---|---|---|
| Presentation/Data بسيطة | contract في data أو موضع عقود متفق | لا يسرّب Dio للعرض |
| Domain مستقلة | abstract contract في Domain؛ implementation في Data | Domain لا تستورد Flutter/Dio |
| مستودع قائم | الموقع المعتمد | لا تنقل العقود دون إذن لتغيير المعمارية |

لا تفرض `RepositoryImpl` أو suffix محدد لمجرد الاسم.
اختيار naming قابل للتكييف؛ وضوح التنفيذ والعقد أهم.

## مثال عقد

**[إضافة]** مقطع لعقد بحث؛ مشروعك يحدد نموذجًا نهائيًا وشكل الفشل:

```dart
abstract interface class ItemsRepository {
  Future<List<ItemSummary>> search(String query);
  Future<ItemDetails> details(String id);
}
```

يتطلب `abstract interface class` Dart 3+.
`ItemSummary` و`ItemDetails` نماذج مشروع، غير معرّفة في هذا المقطع.
العقد بهذا الشكل يحتاج أن يوثق expected failure كنوع exception محدد أو أن يُغيّر إلى Result.
ليس مسموحًا أن ترمي كل implementations أي شيء بلا سياسة لأن التوقيع قصير.

بدائل الفشل:
| البديل | مناسب عندما | كلفته |
|---|---|---|
| typed expected exception | أسلوب المشروع المعتمد وبسيط | يجب توثيقه والتمييز عن unexpected |
| Result واضح | نحتاج إجبار معالجة نجاح/فشل في العقد | نموذج/نمط مشترك وصيانة |
| Either من حزمة | موجود ومعتمد في المشروع | dependency واصطلاحات الفريق |
| throw raw DioException | داخل Data فقط غالبًا | يسرب transport إن عبر إلى Presentation |

Dartz ليس جزءًا لازمًا من MVVM. لا تضفه دون اختيار مبرر ومعتمد.
التفصيل في [الأخطاء والنتائج](../state/errors-and-results.md).

## حالتا تكامل

**[إضافة] — قائمة وبحث:** يستخدم SearchCubit عقد البحث؛ يملك سياسة latest-wins للعرض.
Repository يعيد بيانات أو فشلًا ولا يقرر أي query يجب عرضه.
إذا كان cache يُحدّث بالتوازي، يجب ألا تُستخدم سياسة العرض وحدها كحماية لكتابة cache.

**[إضافة] — تفاصيل ID:** يطلب DetailsCubit تفاصيل ID من contract.
المعرف ليس DTO كاملة من صفحة القائمة؛ الدخول المباشر قد لا يملك نموذج القائمة.
يمكن للـRepository الاستفادة من seed/cached data وفق عقد واضح مع refresh عند الحاجة.

## التشخيص

| العَرَض | افحص | إصلاح مناسب |
|---|---|---|
| أكثر من Cubit يحمّل المصدر نفسه بنسخ متعارضة | هل توجد حقيقة مشتركة وسياسة cache؟ | مصدر مشترك أو invalidation معلوم، لا دمج كل Cubits |
| Use Case يحوي DioException وheaders | هل يقوم بدور Data؟ | إبقاء transport في Data |
| Repository يحوي loading flags وsnackbar | هل تسربت Presentation؟ | عقد نتائج وسلوك عرض في Cubit/UI |
| stale cache بعد save | سياسة invalidation/write version | ربط mutation بالتحديث وتحقق من سيناريو العودة |
| wrapper layers تجعل كل تعديل يمر بعشرة ملفات | ما المسؤولية المستقلة لكل wrapper؟ | فصل متناسب مع قرار المشروع |

## معايير قبول

- contract يعرّف معنى النجاح، الفشل، وغياب البيانات.
- parsing وtransport لا يعبران إلى View.
- cache إن وجدت تحمل سياسة معلومة قابلة للتحقق.
- Use Case تحقق استقلالًا أو تنسيقًا ذا قيمة.
- لا افتراض network/offline أو atomicity دون متطلبات.
- اختبار contract يثبت mapping وسلوك المصدر المهم، واختبار Cubit يستخدم fake مناسبًا.

## تحقق الإصدار

المبادئ راجعتها مقابل [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
بتاريخ 2026-10-01. API لأي Result/DI/cache library تبقى خاصة بالمشروع وتحتاج تحققًا.
الأمثلة عقدية وتفسيرية؛ لا تثبت تشغيل مشروع.
