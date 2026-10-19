# Async flows: تكرار ونتائج قديمة وإلغاء

اقرأ عند بحث/refresh/submit أو سباق requests أو debounce.
لا تجعل latest-wins سياسة عامة لكل عمليات الميزة.

## المحتويات

- المصدر والفروق
- اختيار سياسة لكل command
- مثال Cubit latest-wins
- debounce والإلغاء الحقيقي
- Bloc transformers
- الاختبارات والتشخيص

## المصدر

**[كورس بحسب KB]** M09 Async Operations in BLoC وأجزاء async في M03/M04.
**[مراجعة KB]** TR-018 يميز repeated requests وstale output وtransport cancellation.
**[إضافة]** مثال search والجدول.
[خريطة المصادر](../source-map.md) تسجل نسخ Bloc/Dio.

## أربع مسائل مختلفة

| المسألة | آلية محتملة | لا تعني |
|---|---|---|
| النقر مرتين يطلق العملية نفسها | disable/dedup/droppable | أن الخادم لا يحتاج idempotency |
| القديم ينتهي بعد الحديث | operation generation/input identity | إلغاء resource/network |
| نريد تأخير search حتى يستقر typing | debounce timer/operator | إبطال نتائج طلب قديم تلقائيًا |
| نريد وقف transport | cancellation API وowner معلوم | rollback mutation في الخادم |

Cubit methods قد تتداخل ما لم تنظمها. await داخل method واحدة لا يضع قفلًا على methods أخرى.
`isClosed` guard lifetime، وليس فحص freshness.
عند write، invalidating display لا يلغي تأثير write الذي بدأ بالفعل.

## سياسة كل command

| command | سياسة مرشحة | القرار المطلوب |
|---|---|---|
| search suggestions | latest-wins + debounce عند الحاجة | متى تقبل query وتبطل القديمة؟ |
| refresh لنفس data | dedup أو latest-wins | هل يحتفظ بالبيانات أثناءه؟ |
| login/submit | منع تكرار محلي أو sequential بحسب UX | idempotency وما بعد النجاح؟ |
| pagination | dedup page/serialize/merge | ترتيب pages ونهاية البيانات |
| عمليات مستقلة | concurrent | هل تشترك في state field/source؟ |
| عدة edits لنفس entity | سياسة version/serialize/optimistic معتمدة | الخادم وconflict resolution |

هذه توصيات سياقية؛ اعرض السبب ثم استخدم قرار المنتج/المشروع.
لا تضف مكتبة concurrency أو retry policy تلقائيًا.

## مثال latest-wins في Cubit

**[إضافة]** Dart 3+، fragment يعتمد على ItemsRepository وSearchState وAppFailure في المراجع المجاورة.
UX المثال: trim query؛ empty تمسح البحث؛ أي بحث جديد يمسح النتائج؛ لا debounce أو HTTP cancel هنا.

```dart
class SearchCubit extends Cubit<SearchState> {
  SearchCubit({
    required ItemsRepository repository,
    required void Function(Object, StackTrace) reportUnexpected,
  })  : _repository = repository,
        _reportUnexpected = reportUnexpected,
        super(SearchState());

  final ItemsRepository _repository;
  final void Function(Object, StackTrace) _reportUnexpected;
  int _generation = 0;

  Future<void> search(String rawQuery) async {
    if (isClosed) return;
    final generation = ++_generation;
    final query = rawQuery.trim();

    if (query.isEmpty) {
      emit(SearchState());
      return;
    }

    emit(SearchState(query: query, phase: SearchPhase.loading));

    try {
      final items = await _repository.search(query);
      if (!_isCurrent(generation)) return;
      emit(SearchState(
        query: query,
        phase: SearchPhase.success,
        items: items,
      ));
    } on AppFailure catch (failure) {
      if (!_isCurrent(generation)) return;
      emit(SearchState(
        query: query,
        phase: SearchPhase.failure,
        failure: failure,
      ));
    } catch (error, stack) {
      _reportUnexpected(error, stack);
      if (!_isCurrent(generation)) return;
      emit(SearchState(
        query: query,
        phase: SearchPhase.failure,
        failure: const AppFailure(
          kind: FailureKind.unexpected,
          message: 'تعذر إكمال العملية. حاول مجددًا.',
        ),
      ));
    }
  }

  bool _isCurrent(int generation) =>
      !isClosed && generation == _generation;

  @override
  Future<void> close() {
    ++_generation;
    return super.close();
  }
}
```

يلزم import Cubit من flutter_bloc وعقود المشروع عند التجميع.
callback diagnostics يجب أن يكون آمنًا وألا يرمي؛ يحدد التطبيق implementation.
generation يزيد عند قبول input، بما فيها clear؛ يمنع النتيجة القديمة بعد مسح query.
لا يتحكم المثال بـcache writes داخل Repository ولا يوقف request.
أمثلة العرض والتشخيص يمكن تعديلها للمشروع؛ لا تدخل literals عربية في تطبيق دون خطة localization.

## debounce مع طلب جارٍ

إذا قبلت query B لكن debounce لم يشغّل request B بعد، قد ينتهي request A خلالها.
حدد هل تريد السماح بعرض A أم إبطالها منذ استقبال B.
إذا تريد أحدث input فقط، زد input generation عند القبول، وليس عند بدء HTTP المتأخر فقط.
ألغ timer السابق، وألغِ timer عند close؛ check current generation عند الإطلاق والإكمال.
لا تفترض أن وضع delay داخل search يحقق debounce؛ قد تؤخر كل requests وتشغلها جميعًا.

## الإلغاء الحقيقي

Dio CancelToken متعلق بـtransport في Data.
مرّر معنى الإلغاء عبر contract مناسب، ولا تجعل View/Cubit تفهم DioException الخام.
عند اختيار cancellation contract، حدد:
- من يخلق token/handle ومَن يملك إنهاءه؟
- هل الطلب cancelable أصلًا؟
- هل cancellation failure تظهر للمستخدم أم silent في سياق استبدال request؟
- هل يبقى stale guard مطلوبًا؟ نعم عندما completion/callback يمكن أن يصل رغم الإلغاء.
- هل عملية write بدأت على الخادم؟ لا تعد بإرجاعها تلقائيًا.

التصميم لا يلزم API موحدة لكل مشروع؛ يحتاج قرارًا عند مطلب فعلي.

## Bloc transformers

في bloc 9.2.1، معالجات on تعمل concurrently افتراضيًا.
transformer في `on<EventA>` يطبق على مسار ذلك النوع؛ لا يضمن ترتيبًا شاملًا مع EventB.

| transformer | نية | حد |
|---|---|---|
| concurrent | معالجة متوازية | احمِ state/shared source من races |
| sequential | انتظار السابق في نفس registration | قد يؤخر intent أحدث؛ لا global serialization |
| droppable | تجاهل events جديدة أثناء الحالي | قد يفقد طلبًا مهمًا |
| restartable | إنهاء معالجة السابقة والتركيز على الجديدة | لا يثبت إلغاء HTTP أو الخادم |

داخل handler انتظر futures اللازمة قبل انتهاء handler؛ لا emit من callback مؤجل خارج عمر Emitter.
افحص `emit.isDone` أو APIs المعتمدة عند إلغاء handler وفق نسخة المشروع.
أضف debounce/throttle إذا يلائم intent، لا لجميع الأحداث.
bloc_concurrency ليست default package معتمدة؛ افحص الحاجة قبل إضافتها.

## تحقق حتمي

استخدم fake Repository وCompleter للتحكم في completion، دون sleep/network حقيقي:
1. A يبدأ؛ B يبدأ؛ B ينجح؛ A ينجح/يفشل.
2. يجب أن تبقى نتيجة B دون انتقال فشل A.
3. clear أثناء A ثم completion A لا يعيد data.
4. close أثناء request لا يصدر إلى owner منتهٍ.
5. repeated submit يطابق السياسة المختارة.
6. إذا cache مشتركة، اختبر writes أيضًا؛ اختبار state وحده لا يثبت صحتها.

مثال عملي في [testing-and-verification.md](../quality/testing-and-verification.md).

## التشخيص

| العَرَض | دليل محتمل | المعالجة |
|---|---|---|
| search تقفز إلى query قديمة | ترتيب requests/completions | generation عند قبول input |
| submit مرتان رغم spinner | handler بلا guard أو UI يسمح فقط | سياسة محلية + server contract |
| cancel يسبب رسالة فشل مزعجة | cancellation مصنفة generic error | mapping وسياق replace/exit |
| pagination تتكرر | page key/inflight policy | dedup/serialize حسب العقد |
| debounce لا يمنع requests | delay لكل call أو timers باقية | cancel previous timer وعمر واضح |

## حالة التحقق

[Bloc.on](https://pub.dev/documentation/bloc/latest/bloc/Bloc/on.html): bloc 9.2.1.
[restartable](https://pub.dev/documentation/bloc_concurrency/latest/bloc_concurrency/restartable.html): 0.3.0.
[CancelToken](https://pub.dev/documentation/dio/latest/dio/CancelToken-class.html): Dio 5.11.1.
تحقق 2026-10-01. مثال Cubit لم يُشغّل هنا؛ يلزم analyzer واختبار المشروع.
