# الأخطاء ونتائج العمليات

اقرأ عند mapping للفشل أو اختيار Result أو رسالة UX أو handling غير متوقع.
لا تجعل كل failure «لا يوجد إنترنت».

## المحتويات

- المصدر وحدود الفشل
- نموذج failure وخيارات النتائج
- مثال Dio الحالي
- التشخيص والرسائل
- retry والتحقق
- الإصدارات والتصحيح

## المصدر

**[كورس بحسب KB]** M10 Error Handling and Failure States وأجزاء Either/Dio في M18.
**[مراجعة KB]** TR-013 Either خيار، TR-014 التصنيف، TR-022 فشل لا يساوي No Internet.
**[إضافة]** AppFailure والـmapping المحدث.
**[تصحيح موثق]** KNOWN-DIO-01 في [source-map.md](../source-map.md).

## حدود الفشل

| الحد | ما يعرفه | ما يسلمه |
|---|---|---|
| Data/transport | DioException/status/parsing/schema | failure ذات معنى آمن وفق contract |
| Repository/Application | معنى العملية وعدم وجود بيانات | success/failure/not-found وفق سياسة |
| Cubit | حالة العرض/retry/current input | snapshot كاملة وتأثير معلن عند الحاجة |
| UI | localization/عرض ورسالة وفوكس | feedback ملائم، دون raw exception |

فشل expected مثل not-found أو validation يختلف عن unexpected bug.
سجّل unexpected مع stack عبر آلية المشروع؛ لا catch صامتة ثم ادعاء أن كل شيء network.
الـlogging لا يعرض tokens/payload حساسة ولا يظهر stack للمستخدم.

## نموذج توضيحي

**[إضافة]** يستخدمه مثال SearchCubit؛ ليس معيار taxonomy لكل مشروع:

```dart
enum FailureKind {
  timeout,
  connection,
  rejected,
  certificate,
  cancelled,
  invalidData,
  unexpected,
}

class AppFailure implements Exception {
  const AppFailure({
    required this.kind,
    required this.message,
  });

  final FailureKind kind;
  final String message;
}
```

`message` هنا آمنة توضيحية. في مشروع متعدد اللغات قد يكون الأنسب code/message key في state
وlocalization في View؛ لا تربط Domain بـBuildContext.
النوع لا يقرر snackbar/route.
`rejected` مثال مختصر؛ المشروع قد يفصل unauthorized/forbidden/notFound/validation/server.

## نتيجة أم exception؟

| النمط | فائدة | قيد |
|---|---|---|
| success value + typed expected exception | قليل البنية | contract يعلن expected failures بوضوح |
| sealed Result | handling واضح في types | يحتاج نموذجًا واتساقًا، Dart 3+ إن sealed |
| Either | مناسب إذا الفريق والحزمة اعتمداه | لا default adoption لـdartz |
| raw transport exception إلى UI | سريع مبدئيًا | coupling ورسالة غير آمنة |

لا تغير convention مشروع كامل في إصلاح ضيق.
لا تستخدم `catch (_){return [];}` لأن failure تتحول إلى success-empty مضللة.

## مثال mapping Dio 5.11.1

**[إضافة/تصحيح]** fragment يتطلب import Dio وAppFailure.
يغطي enum الحالي؛ ليس كافيًا وحده لتصنيف HTTP statuses/business responses.

```dart
AppFailure mapDioFailure(DioException error) {
  return switch (error.type) {
    DioExceptionType.connectionTimeout ||
    DioExceptionType.sendTimeout ||
    DioExceptionType.receiveTimeout =>
      const AppFailure(
        kind: FailureKind.timeout,
        message: 'استغرقت العملية وقتًا أطول من المتوقع.',
      ),
    DioExceptionType.transformTimeout => const AppFailure(
        kind: FailureKind.timeout,
        message: 'تعذر معالجة الاستجابة في الوقت المحدد.',
      ),
    DioExceptionType.badCertificate => const AppFailure(
        kind: FailureKind.certificate,
        message: 'تعذر إنشاء اتصال آمن.',
      ),
    DioExceptionType.badResponse => const AppFailure(
        kind: FailureKind.rejected,
        message: 'تعذر إكمال الطلب من الخدمة.',
      ),
    DioExceptionType.cancel => const AppFailure(
        kind: FailureKind.cancelled,
        message: 'أُلغيت العملية.',
      ),
    DioExceptionType.connectionError => const AppFailure(
        kind: FailureKind.connection,
        message: 'تعذر الاتصال بالخدمة.',
      ),
    DioExceptionType.unknown => const AppFailure(
        kind: FailureKind.unexpected,
        message: 'حدث خطأ غير متوقع.',
      ),
  };
}
```

Dart 3+ مطلوب للـswitch expression وOR patterns.
`transformTimeout` موجود منذ Dio 5.10.0؛ المثال غير مناسب للنسخ الأقدم دون تعديل.
لا تستخدم wildcard فقط لإخفاء نوع جديد أثناء upgrade؛ راجع المعنى والتغطية.
إذا كانت نسخة المشروع أقدم، استعمل enum فيها، ولا تحدّث الحزمة لمجرد نسخ المثال.

## beyond enum

| الحالة | دليل التصنيف | ما لا تستنتجه |
|---|---|---|
| badResponse 404 | endpoint/contract | كل 404 تعني route not-found UI بنفس المعنى |
| 401/403 | auth/access contract | retry تلقائي بلا refresh policy |
| validation response | schema وأسماء fields | عرض raw backend message آمن دائمًا |
| parsing FormatException | schema/decoder | المستخدم offline |
| cancellation | owner/request intent | failure يجب عرضها دائمًا |
| connectionError | transport cause | تشخيص مؤكد لانقطاع الإنترنت المحلي |
| unknown | error/error stack وboundary | تجاهل bug لأنها networking |

عدم وجود نتائج valid يختلف عن malformed payload.
نجاح HTTP قد يحتوي business failure يحتاج mapping.
خطأ transport قد يحتاج retain data عند refresh بدل مسحها.

## diagnostics

- context محدد غير حساس: operation name، correlation إذا معتمد، failure category.
- stack للـunexpected بحسب آلية المشروع.
- لا credentials/full payload افتراضيًا.
- لا تتوقف العملية بسبب reporter إلا إذا contract يقصد ذلك؛ اجعل reporter آمنًا.
- تجنب double reporting لنفس failure من كل طبقة.
- عند عدم إمكان تأكيد السبب، استخدم صياغة محدودة بدل «أكيد الشبكة».

## retry

قرر retry وفق طبيعة العملية:
- read قد يسمح retry يدوي أو policy معلومة.
- write قد يكرر side effect؛ يحتاج idempotency/contract.
- cancelled replacement لا يستحق error banner غالبًا.
- validation تحتاج تغيير input، لا تكرارًا أعمى.
- unauthorized قد يحتاج auth workflow معتمد.

لا تضف exponential retry أو offline recovery لأنها «مهنية» فقط.
والـtimeout لا يثبت أن الخادم لم ينفذ write.

## التشخيص والقبول

| العَرَض | افحص | تحقق مطلوب |
|---|---|---|
| كل الأخطاء No Internet | catch/mapping | حالات parsing/HTTP/cancel/unexpected مختلفة |
| فارغ بدل error | return [] من catch | فشل وempty منفصلان |
| stack أو payload يظهر للمستخدم | message boundary | safe message/localization |
| cancel يحدث snackbar | intent classification | replacement/exit silent حسب UX |
| switch يكسر upgrade | enum/version | تغطية أنواع النسخة الفعلية |
| retry يكرر save | write contract | dedup/idempotency كما يقرر المشروع |

القبول: contract متسق، failure آمنة، expected/unexpected مميزتان،
ولا سياسة retry أو package أو taxonomy جديدة مفروضة بلا حاجة.

## تحقق الإصدار

[DioExceptionType](https://pub.dev/documentation/dio/latest/dio/DioExceptionType.html)
— Dio 5.11.1، و[changelog](https://pub.dev/packages/dio/changelog) إضافة transformTimeout في 5.10.0.
[Dart switch](https://dart.dev/language/branches) يشرح exhaustive switch.
تحقق 2026-10-01 بالوثائق؛ لم يُشغّل analyzer أو network test هنا.
