# التمرير والقوائم والشبكات وSlivers

اقرأ عند قوائم طويلة أو mixed content أو viewport errors أو scroll conflicts.
حدد scroll owner والقيود قبل اختيار shrinkWrap.

## المحتويات

- المصدر
- اختيار scroll composition
- bounded viewport وSlivers
- Grid strategy وPageView
- حالة التمرير
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** R06 Scrolling and Slivers؛ أمثلة lists/grids/Slivers في القاعدة.
**[مراجعة KB]** حدود shrinkWrap/Intrinsic/viewport وتوسعة grid/refactoring في R06/R12.
**[إضافة]** جدول scroll ownership وحالات التحقق.
[خريطة المصادر](../source-map.md).

## اختيار composition

| المحتوى | بداية مناسبة | ما نفحصه |
|---|---|---|
| عناصر قليلة ثابتة في form | SingleChildScrollView + Column عند حاجة | لا Expanded في محور unbounded |
| قائمة طويلة | ListView.builder | finite viewport وlazy children |
| grid طويلة | GridView.builder/SliverGrid | قيود tile والمحتوى وlazy بناء |
| header + قائمة + footer في تمرير واحد | CustomScrollView مع slivers | adapters صحيحة وowner واحد |
| مناطق تمرير مستقلة فعلًا | scrollables بعرض/ارتفاع محدودين | gesture/controller behavior |
| nested scrolling منسق | تركيب Flutter ملائم للمتطلبات | لا تُركّب بلا تجربة header/scroll فعلية |

لا تضع ListView طويلة في SingleChildScrollView ثم shrinkWrap=true كحل عام.
ذلك قد يزيد تكاليف sizing ويغير lazy behavior ويخلق owners غير لازمين.
قائمة صغيرة داخل محتوى محدود قد تبرر shrinkWrap؛ سجل السبب وقِس إن ظهرت مشكلة.

## viewport finite

List/Grid تحتاج viewport مناسبة في المحور الذي تعرضه.
داخل Column في body finite، يمكن `Expanded(child: ListView.builder(...))`.
داخل Column unbounded في ScrollView، Expanded ليست viewport.
أصلح القيود أو اجعل القائمة sliver ضمن scroll owner الأساسي.

Cross axis مهمة أيضًا: horizontal ListView تحتاج height مقصودة،
vertical viewport تحتاج عرضًا معلومًا.
لا تختَر ارتفاعًا من full screen تلقائيًا إذا جزء الصفحة داخل shell/panel.

## Box مقابل Sliver

CustomScrollView.slivers يتوقع Slivers.
- `SliverToBoxAdapter` يربط box content قصيرًا بتركيب sliver.
- `SliverList`/`SliverGrid` يعرضان عناصر lazy.
- `SliverPadding` للـsliver، وليس Padding box داخل قائمة slivers.
- `SliverFillRemaining` سلوك sliver ضمن viewport؛ ليس Expanded يمكن وضعه في كل مكان.
- `SliverLayoutBuilder` يعطي SliverConstraints ويبني sliver؛ ليس BoxConstraints.

لا تلف ListView كاملة في SliverToBoxAdapter دون سبب؛ قد تحتفظ بتعارض owner أو viewport.
العبرة بالتركيب والقيود الفعلية.

## مثال تركيب

**[إضافة]** fragment يفترض ItemTile/Header وitems من مشروعك:

```dart
CustomScrollView(
  slivers: [
    const SliverToBoxAdapter(child: CatalogHeader()),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ItemTile(item: items[index]),
        childCount: items.length,
      ),
    ),
  ],
)
```

لا يثبت المثال state/restoration أو semantics أو pagination.
إذا Header له scroll/pinned behavior، تحتاج sliver مناسبة بدل box adapter فقط.

## Grid strategy

| الاختيار | مناسب | قيد |
|---|---|---|
| fixed column count لكل layout | عدد معلوم يحقق UX | tile width تتغير؛ جرب long text/scale |
| max cross-axis extent | حد أقصى لحجم tile | لا يضمن حدًا أدنى دائمًا |
| حساب columns من local min tile width | cards تحتاج حدًا أدنى وظيفيًا | تأكد من width صغيرة وعدد لا يقل عن 1 |
| fixed childAspectRatio | media/cards بسيطة | لا يضمن احتواء نص متغير/مكبر |
| mainAxisExtent | height معتمدة وثابتة وظيفيًا | غير مناسب للمحتوى المتغير دون دليل |

حساب مثال **[إضافة]**:
`columns = floor((availableWidth + gap) / (minTileWidth + gap))` ثم حد أدنى 1.
كل الأرقام design/content choices؛ اختبر tile بعد padding/spaces، ولا تنس height.
لا تخلط max extent مع min tile width في تفسير delegate.

## PageView والارتفاع

PageView تحتاج viewport finite.
اختيار ارتفاع ثابت يناسب محتوى ثابتًا قد يفشل مع نص طويل/scale.
اختيار expandable_page_view من القاعدة ليس default dependency معتمدة؛
تحقق نسخة الحزمة والسلوك والقيود فقط إذا توجد حاجة واختيار مقبول.
بديل المحتوى variable قد يكون scroll composition آخر أبسط.

## scroll state

من يملك ScrollController ومَن يغلقه؟ هل الصفحة تبقى في tree؟
قرر حفظ offset عند back/resize/filter:
- نفس البيانات: قد يكون حفظ offset مطلوبًا.
- filter جديدة: قد يكون reset مقصودًا.
- إعادة ترتيب/حذف عناصر: offset قد يحتاج تعديلًا أو item identity.
- wide/narrow تبدّل scroll owner: استعادة offset تحتاج عقدًا لا مجرد key.

Keys وPageStorage ليست ضمانًا عامًا لبقاء كل حالة.
لا تضف restoration architecture دون requirement.

## التشخيص

| العَرَض | افحص | التصحيح |
|---|---|---|
| vertical viewport unbounded | parent height وnested owners | finite viewport أو sliver composition |
| jank في list طويلة | shrinkWrap/children eager/layout/media | lazy composition ثم profile |
| scroll لا يعمل أو gestures متعارضة | nested direction/controllers/physics | owner مناسب لا physics patches عمياء |
| card text clipped | extent/aspectratio وscale | content-driven height/layout |
| فارغ يأخذ مساحة غير مناسبة | SliverFillRemaining constraints | اختيار sliver وفق السلوك المطلوب |
| offset يضيع عند resize | controller/branch ownership | preservation مقصود ومختبر |

## مصفوفة التحقق

- 0/1/عدد كبير من العناصر؛ loading/error/empty.
- ضيق/واسع وheight قصيرة؛ headers/footer reachable.
- نص طويل وTextScaler كبير داخل grid.
- scroll مع touch/mouse/keyboard إذا مدعوم.
- resize أثناء scroll وعند تغير البيانات.
- إعادة البناء لا تعيد offset إلا وفق المتطلبات.
- profile في مشروع حقيقي قبل ادعاء تحسين أداء.

## حالة الإصدار

[SliverLayoutBuilder API](https://api.flutter.dev/flutter/widgets/SliverLayoutBuilder-class.html)
راجعناه بتاريخ 2026-10-01.
أي package اختيارية أو API أحدث في delegates يحتاج SDK المشروع.
المثال fragment لم يُبنَ هنا.
