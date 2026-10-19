# Breakpoints والتكيّف وحفظ الحالة

اقرأ عند تغير ترتيب/عدد أعمدة/تنقل أو فقد state بعد resize.
العتبة نتيجة محتوى وتجربة، لا اسم جهاز.

## المحتويات

- المصدر والتمييز
- اختيار العتبة
- shell مقابل component
- حفظ state وموارد UI
- مثال form متكيّف
- التشخيص والتحقق

## المصدر

**[كورس بحسب KB]** R09 Adaptive Layouts and Breakpoints، R03 القيود المحلية.
**[مراجعة KB]** R09 حفظ state وحدود Keys، R10 تكيّف المنصة توسعة.
**[استنتاج]** ربط layout بالعمر في M07/TR-016/019.
**[إضافة]** protocol العتبة ومثال form.
[خريطة المصادر](../source-map.md).

## Responsive وAdaptive

Responsive يعدّل geometry داخل تركيب مناسب للمساحة.
Adaptive يغيّر تركيبًا/تفاعلًا عندما يبرر السياق ذلك، مثل list/detail أو navigation rail.
الحجمان ليسا device/platform detection.
قد يكون هاتف في نافذة صغيرة أو desktop panel ضيقة؛ القرار المحلي يرى المساحة المتاحة.

المنصة ونوع input بعدان مستقلان عن width، كما في [مرجع الإدخال](platform-accessibility-and-input.md).

## اختيار العتبة

1. حدد المحتوى الأدنى الوظيفي: نص/actions/media وما يجب أن يبقى مرئيًا.
2. حدد max width عند الحاجة كي لا يمتد نص/form بلا فائدة.
3. احسب المساحة بعد padding/sidebar/gaps، ثم جرّب نصًا طويلًا وscale.
4. عندما لا يتسع التركيب، غيّر layout بدل تصغير كل شيء.
5. سجل سبب threshold واختبر تحته/عنده/فوقه.
6. راجع height/insets؛ width وحدها قد لا تكفي.

**[إضافة]** إذا panel رئيسية تحتاج 320 وaside تحتاج 280 وgap=24،
فالتركيب يحتاج 624 logical px محليًا قبل outer padding.
هذه أرقام تعليمية لشرح الجمع، وليست default breakpoint.

## shell وcomponent

| القرار | مصدره | اتساق |
|---|---|---|
| navigation/shell عام | المساحة التي يملكها shell | قرار واحد للمناطق التي يجب أن تتغير معًا |
| بطاقة/toolbar/form داخل panel | local constraints | يجوز أن تختار narrow داخل shell واسع |
| keyboard/scale/direction | environment بالسياق | يؤثر على المساحة/القراءة/input |
| platform-specific interaction | منصة/input معتمدان | لا يستنتج من width |

لا تسمح لنصف shell أن يقرأ window ونصفه panel width بلا قصد.
ولا تفرض breakpoint shell على كل component مستقل.

## حفظ state

عند تبديل branch، Flutter قد يزيل subtree ويخلق أخرى.
Keys تساعد matching ضمن قواعد tree؛ لا تحفظ state لعنصر أزيل نهائيًا.
المطلوب الذي يجب أن يبقى يكون لدى owner ثابت:
- Cubit/Repository فوق branch وفق العمر.
- controller/focus/scroll resource في UI owner مناسب.
- draft أو selection ذات حقيقة واحدة.

رفع owner ليس رفع كل state إلى app root.
قد يقرر المنتج إعادة ضبط selection أو offset في transition محددة؛ وثّق ذلك بدل افتراض الحفظ دائمًا.

## مثال form

**[إضافة]** fragment من داخل State مستقرة. draft في controller واحدة، save state في Cubit مستقلة عند الحاجة:

```dart
final titleController = TextEditingController();

@override
void dispose() {
  titleController.dispose();
  super.dispose();
}

Widget buildFormBody(BuildContext context) {
  return LayoutBuilder(
    builder: (context, constraints) {
      final input = TextField(
        controller: titleController,
        decoration: const InputDecoration(labelText: 'العنوان'),
      );

      if (constraints.maxWidth < 624) {
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            input,
            const SizedBox(height: 24),
            const DraftHelp(),
          ],
        );
      }

      return Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(child: input),
          const SizedBox(width: 24),
          const SizedBox(width: 280, child: DraftHelp()),
        ],
      );
    },
  );
}
```

`DraftHelp` مكوّن المشروع؛ 624/280 افتراضات المثال.
ضع body في composition يسمح بالتمرير وheight المناسبة؛ snippet لا يعالج keyboard كاملًا.
controller تبقى لأن State المالكة فوق layout؛ النص يبقى عند التبديل.
هذا لا يثبت بقاء focus/selection أو validation state لكل subtree؛ اختبرها وحدد عقدها.
لا تنشئ controller داخل builder ولا تبقِ نسختين narrow/wide كل منهما draft مختلفة.
للتوطين، استبدل literals بموارد المشروع.

## محتوى مشترك وتنظيم

شارك المحتوى والسلوك المستقرين بين layouts.
اجعل differences في composition؛ لا تنسخ business logic أو effects.
لا تبنِ framework عام لصفحتين بسيطتين قبل وجود pattern ثابت.
الـhelpers هي وسائل لتوضيح المسؤولية، وليست شواهد تحسين أداء بحد ذاتها.

## التشخيص

| العَرَض | افحص | التصحيح |
|---|---|---|
| فقد form/query بعد resize | owner داخل branch | owner فوق transition |
| wide layout ينهار في split window | full-window size/device label | قيد المنطقة الفعلي |
| عناصر shell متناقضة | مصادر thresholds | توحيد قرار shell |
| النص صغير كي «يتسع» | scaling حل محل layout | wrapping/تركيب مناسب |
| wide form ممتدة بلا فائدة | max content width | حد مقصود/تموضع مناسب |
| request يعاد بعد orientation | owner/load triggers | lifecycle مستقرة |

## مصفوفة قبول

- W−1، W، W+1 للعتبة المعتمدة؛ ليست كلها screens واسعة منفصلة فقط.
- نافذة واسعة مع panel ضيقة؛ portrait/landscape وheight قصيرة.
- نص طويل وscale/RTL؛ actions قابلة للوصول.
- resize أثناء typing/loading/scroll، دون فقد مطلوب أو طلب جديد غير مقصود.
- same content/same behavior في layouts؛ differences مفهومة.
- لا branch مخفية تواصل effect/requests دون قصد.

## تحقق الإصدار

[Flutter adaptive-responsive guide](https://docs.flutter.dev/ui/adaptive-responsive/general)
راجعناه بتاريخ 2026-10-01؛ أي عتبة في الوثائق مثال لتجربة محددة، ليست قاعدة عامة.
لم تُشغّل form أعلاه على جهاز؛ Preservation المذكور مبني على ownership ويحتاج widget/runtime tests.
