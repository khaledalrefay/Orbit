# المرحلة 3 — تهيئة بيئة المشروع

**الحالة:** ⬜ · **تعتمد على:** 1، 2 (الاسم ضروري لاسم المستودع والحزمة) · **نوعها:** إعداد

## الهدف
مستودع جديد بمشروع Flutter نظيف، يعمل عليه أي مطوّر أو إيجنت من أول يوم: أوامر واضحة، وفحوص آلية، ووثائق سياق.

## المدخلات
- الاسم (هِمّة / HIMMA) ونتيجة فحص توفّره من المرحلة 1. اسم المستودع المقترح `himma`، ومعرّف الحزمة يُبنى على
  الدومين المعتمد (مثلًا `app.himma` أو `com.<domain>.himma`).
- قرار المنصات وطريقة بناء iOS من المرحلة 1.

## المهام

### أ. المستودع
- [ ] إنشاء المستودع الجديد، ونقل `docs/plan/` إليه من Orbit.
- [ ] إضافة tag `web-v1` على مستودع Orbit، وتسجيل Orbit وحركة كمراجع في `docs/PROJECT_CONTEXT.md` (روابط وأهم الملفات).
- [ ] الرخصة، و `.gitignore`، و `README.md`، وقالب PR، وقواعد حماية الفرع الرئيسي.

### ب. مشروع Flutter
- [ ] `flutter create` بالمنصات المقررة (Android و iOS) ومعرّف الحزمة، مع تثبيت إصدار Flutter (FVM أو `.tool-versions`).
- [ ] اختيار الحزم الأساسية وتثبيت إصداراتها (المقترح، ويُراجع وقتها):
  - إدارة الحالة: `flutter_bloc` (Cubit بدور ViewModel، حسب `.claude/flutter-knowledge`)، والحقن عبر constructor و `RepositoryProvider`.
  - التنقّل: `go_router`.
  - قاعدة البيانات: `drift` و `sqlite3_flutter_libs`.
  - الإعدادات: `shared_preferences`.
  - الإشعارات: `flutter_local_notifications` و `timezone` و `flutter_timezone`.
  - الصوت: `audioplayers` أو `just_audio`.
  - الشاشة والاهتزاز: `wakelock_plus`، وخدمة HapticFeedback المدمجة.
  - الترجمة: `flutter_localizations` و `intl` و gen-l10n.
  - النماذج: `freezed` و `json_serializable`، أو نماذج يدوية (يُقرّر).
- [ ] هيكل المجلدات حسب الميزة:
  ```
  lib/
    app/            التركيب والتنقّل والثيم
    core/           المحرّكات (Dart صافي)، والوقت، والأدوات
    data/           قاعدة البيانات، والمستودعات، والمحتوى
    features/
      today/  focus/  programs/  library/  progress/  onboarding/  settings/
        (داخل كل ميزة: presentation/{cubit,views,widgets} و data/ عند الحاجة)
    l10n/
  assets/content/   assets/images/   assets/sounds/   assets/fonts/
  test/   integration_test/   tool/
  ```
- [ ] `analysis_options.yaml` بقواعد صارمة (`very_good_analysis` أو `flutter_lints` مع إضافات)، و `dart format`.
- [ ] قاعدة حدود الاعتماد: `core/` لا يستورد Flutter، و `features/` لا يستورد بعضها مباشرة.
      تُفحص بسكربت في `tool/`، على غرار `check-architecture.py` في حركة.

### ج. CI/CD
- [ ] GitHub Actions: format، ثم analyze، ثم test، ثم build apk (debug) على كل PR.
- [ ] بناء iOS (Codemagic أو GitHub macOS runner) بلا توقيع في هذه المرحلة.
- [ ] تخزين مفاتيح التوقيع لاحقًا كأسرار (لا مفاتيح داخل المستودع).

### د. وثائق العمل وملف الإيجنت
- [ ] `CLAUDE.md` (وإن لزم `AGENTS.md` يشير إليه)، ويتضمن:
  - ملخص المشروع في 5 أسطر، مع رابط `PROJECT_CONTEXT.md`.
  - أوامر التشغيل والفحص والاختبار وتوليد الكود.
  - القواعد: هيكل المجلدات، وحدود الاعتماد، ولا نصوص ثابتة في الواجهة (كلها من l10n)، و RTL أولًا، وحالات الاختبار المطلوبة.
  - طريقة العمل على المراحل: قراءة ملف المرحلة، وتحديث المربعات، وتسجيل القرارات، وكتابة ملخص الإنجاز.
  - ما لا يُفعل: لا تعديل ملفات مولّدة يدويًا، ولا حزم جديدة بلا قرار، ولا ادعاءات صحية في النصوص.
- [ ] `docs/PROJECT_CONTEXT.md`: الفكرة والجمهور والهوية والقرارات المحسومة والمراجع (من `PRODUCT.md` و `BRAND.md`).
- [ ] `docs/ARCHITECTURE.md`: نسخة أولى بالطبقات والحزم وتدفّق البيانات.
- [ ] `docs/ai/project-decisions.md`: نقل D1 إلى D6 وقرارات المرحلتين 1 و2.
- [ ] نقل `.claude/skills/` و `.claude/flutter-knowledge/` من Orbit إلى المستودع الجديد، وذكرهما في `CLAUDE.md`
      (متى يُستدعى كل skill).
- [ ] قاعدة في `CLAUDE.md`: عند اختيار حزمة، نفضّل ما يدعم الويب إن تساوت الخيارات (الويب مؤجّل لا ملغى).
- [ ] Hook لبداية الجلسة (SessionStart) يثبّت Flutter في بيئة السحابة، إن احتجنا جلسات Claude Code على الويب.

## المخرجات
مستودع جديد فيه: تطبيق Flutter فارغ يعمل على المنصتين، و CI أخضر، ووثائق `CLAUDE.md` و `PROJECT_CONTEXT.md`
و `ARCHITECTURE.md` و `docs/ai/project-decisions.md`.

## معايير الإنهاء
- [ ] `flutter run` يعمل على محاكي Android و iOS (أو بناء iOS ناجح على CI).
- [ ] CI أخضر على PR تجريبي.
- [ ] جلسة إيجنت جديدة تستطيع، بالاعتماد على `CLAUDE.md` وحده، تشغيل الفحوص والاختبارات بنجاح.

## ملخص الإنجاز
_يُكتب عند الإنهاء._
