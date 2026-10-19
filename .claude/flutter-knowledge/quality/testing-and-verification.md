# الاختبارات والتحقق المتناسب

اقرأ عند تخطيط دليل لسلوك جديد أو إصلاح race أو مراجعة tests.
اختر الاختبار الذي يكشف failure محتملة؛ لا تكتب test تكرر implementation بلا قيمة.

## المحتويات

- المصدر وحدود الادعاء
- اختيار المستوى
- اختبار async حتمي
- اختبار resize وحفظ draft
- مصفوفة تغطية
- نتيجة التحقق

## المصدر

**[مراجعة KB/توسعة]** M16 Testing BLoC and MVVM؛ لا ننسب كل اختبارات القاعدة إلى فيديوهات الكورس.
R12 Performance Considerations يتضمن refactoring/testing، وM09 يدعم حالات async.
**[إضافة]** أمثلة الاختبارات التالية ومصفوفة السيناريوهات.
[خريطة المصادر](../source-map.md).

## معنى «تحقق»

| الدليل | يثبت | لا يثبت |
|---|---|---|
| قراءة/static review | حدود ومسارات وأسباب محتملة | أن التطبيق يعمل على جهاز |
| analyzer | types/lints وفق SDK وdependencies | UX أو correctness لكل سلوك |
| unit/Cubit test | transitions/contracts/races مضبوطة | native keyboard أو deep-link configuration |
| widget test | بناء/تفاعل/layout في البيئة المحاكية | كل OS/input/nonlinear text behavior |
| integration/platform run | سلوك المسار الذي جُرّب فعليًا | جميع المنصات/الحالات |
| golden | تغير بصري في fixture محددة | قابلية وصول أو async correctness |

لا تساوِ عدم وجود exception مع صحة المحتوى والمعنى.
ولا تقل «responsive» لأن عرضين يعرضان صورة جميلة فقط.

## اختيار المستوى

| تغيير | تحقق مناسب |
|---|---|
| parsing/DTO mapping | حقول ناقصة وأنواع وفشل contract |
| async latest-wins | Completer ترتيب completion معكوس |
| ownership/create/value | close count وroute exit عند الصلة |
| refresh/empty/failure | state payload وUI المتفق |
| effect نجاح | انتقال واحد يؤدي effect واحد من owner مقصود |
| adaptive form | resize أثناء typing مع بقاء draft |
| tiny cosmetic reversible | معاينة/فحص متناسب؛ لا test جديدة شكلية |
| performance | profile measurement قبل/بعد |

استخدم أدوات المشروع المثبتة. لا تضف bloc_test/mockito/golden package لمجرد أن الكورس ذكر اختبارات.
الاختبار باستخدام Fake/Completer وflutter_test قد يكون كافيًا.

## مثال async حتمي

**[إضافة]** fragment اختبار يعتمد SearchCubit/SearchState/AppFailure/ItemsRepository
وItemSummary/ItemDetails من المراجع والمشروع؛ أضف imports.
`details` غير مستخدمة في fixture البحث، لذلك fake يرفضها بوضوح.

```dart
class ControlledItemsRepository implements ItemsRepository {
  final pending = <String, Completer<List<ItemSummary>>>{};

  @override
  Future<List<ItemSummary>> search(String query) {
    final completer = Completer<List<ItemSummary>>();
    pending[query] = completer;
    return completer.future;
  }

  @override
  Future<ItemDetails> details(String id) =>
      throw UnimplementedError('Details are outside this fixture');
}

test('a slower old query cannot replace the current result', () async {
  final repository = ControlledItemsRepository();
  final unexpected = <Object>[];
  final cubit = SearchCubit(
    repository: repository,
    reportUnexpected: (error, stack) => unexpected.add(error),
  );
  addTearDown(cubit.close);

  final oldRequest = cubit.search('A');
  final newRequest = cubit.search('B');

  repository.pending['B']!.complete([
    const ItemSummary(id: 'b', title: 'B'),
  ]);
  await newRequest;

  repository.pending['A']!.complete([
    const ItemSummary(id: 'a', title: 'A'),
  ]);
  await oldRequest;

  expect(cubit.state.query, 'B');
  expect(cubit.state.phase, SearchPhase.success);
  expect(cubit.state.items.single.id, 'b');
  expect(unexpected, isEmpty);
});
```

يلزم `dart:async` و`flutter_test` مع imports المشروع.
الـFake keyed بالـquery لا تصلح لاختبار repeated query متزامنة؛ استخدم قائمة requests/IDs لذلك.
لا تستعمل Future.delayed لتخمين ترتيب الشبكة.
امتدادات مهمة بحسب الخطر:
- A تفشل بعد نجاح B: لا تتحول state إلى failure A.
- clear ثم إكمال A: تبقى initial/empty input وفق policy.
- close ثم إكمال A: لا emit أو unhandled error.
- repeated submit/pagination: تطابق السياسة المختارة.
- cache write races: اختبار Repository مستقل إن موجودة.

## مثال resize وحفظ draft

**[إضافة]** fragment يستهدف DraftPage حقيقية في مشروعك.
أضف `ValueKey('draft-title')` للحقل/fixture عند الحاجة وبدّل الصفحة وفق الكود.

```dart
testWidgets('draft survives a layout-width change', (tester) async {
  tester.view.devicePixelRatio = 1;
  tester.view.physicalSize = const Size(600, 900);
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);

  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(body: DraftPage()),
    ),
  );

  final field = find.byKey(const ValueKey('draft-title'));
  await tester.enterText(field, 'مسودة محفوظة');

  tester.view.physicalSize = const Size(900, 900);
  await tester.pump();

  final widget = tester.widget<TextField>(field);
  expect(widget.controller!.text, 'مسودة محفوظة');
  expect(tester.takeException(), isNull);
});
```

DPR=1 في fixture، لذلك الأبعاد physical المختارة تساوي logical؛ هذا قرار الاختبار فقط.
`DraftPage` وimports غير موجودة في المرجع كملفات تنفيذ؛ أكملها في المشروع.
إذا controller ليست public على TextField، افحص EditableText/القيمة الظاهرة بطريقة مناسبة.
هذا يثبت draft في transition محددة، لا focus/scroll/keyboard/validation أو كل widths.
أضف assertion للتركيب/الفعل المطلوب أيضًا؛ no exception وحدها غير كافية.

## نص وkeyboard وRTL

- TextScaler.linear محاكاة خطية، لا proof لنظام non-linear الأصلي.
- Directionality/locale fixture بحسب resources المشروع.
- keyboard focus لا يعني OS keyboard insets؛ حاك geometry عند الحاجة وجرّب النظام عند الأهمية.
- افحص reachability والفعل والنص الضروري لا screenshot فقط.
- reset أي overrides للview/platform/MediaQuery بين tests.

## مصفوفة متناسبة

اختر representative cases بدل حاصل ضرب ضخم:
| المحور | بداية تغطية |
|---|---|
| state | initial/loading/success-empty/success/failure وما تضيفه الميزة |
| async | old/new completion، clear/close، repeated operation |
| space | narrow/wide/local panel، threshold−1/at/+1، short height |
| text | طويل وscale كبير، اللغات المدعومة |
| interaction | typing ثم resize، keyboard/scroll/input عند الصلة |
| route | direct ID/IDchange/back/exit إذا موجودة |

إذا راجعت source فقط، اكتب «تغطية مقترحة» لا «مُختبرة».

## نتيجة التحقق

لكل تحقق سجّل: الأمر أو السيناريو، البيئة/النسخة، النتيجة، الدليل، والحدود.
إذا لا توجد الأدوات:
- قدم scenario/code adaptée وخطوات التشغيل.
- صرّح أن التشغيل مؤجل.
- لا تحول المراجعة النظرية إلى pass.

لا تعاود suite واسعة بعد نجاحها إلا إذا تغيرت الشيفرة أو ظهرت مشكلة تبرر ذلك.

## حالة API

[WidgetTester](https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html)
و[TestFlutterView](https://api.flutter.dev/flutter/flutter_test/TestFlutterView-class.html)
تدعم view overrides/reset؛ تحقق 2026-10-01.
أمثلة المرجع لم تُشغّل باستخدام Flutter/Dart؛ تحقق SDK المشروع قبل التنفيذ.
