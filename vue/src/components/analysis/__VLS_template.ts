import { __VLS_internalComponent, __VLS_componentsOption, __VLS_name, startYear, endYear, selectedCountry, updateYearChart, yearChart, selectedMonthYear, selectedMonthCountry, updateMonthChart, monthChart, selectedRegionYear, updateRegionChart, regionChart } from './ProductionChart.vue';

function __VLS_template() {
let __VLS_ctx!: InstanceType<__VLS_PickNotAny<typeof __VLS_internalComponent, new () => {}>> & {};
/* Components */
let __VLS_otherComponents!: NonNullable<typeof __VLS_internalComponent extends { components: infer C; } ? C : {}> & typeof __VLS_componentsOption;
let __VLS_own!: __VLS_SelfComponent<typeof __VLS_name, typeof __VLS_internalComponent & (new () => { $slots: typeof __VLS_slots; })>;
let __VLS_localComponents!: typeof __VLS_otherComponents & Omit<typeof __VLS_own, keyof typeof __VLS_otherComponents>;
let __VLS_components!: typeof __VLS_localComponents & __VLS_GlobalComponents & typeof __VLS_ctx;
/* Style Scoped */
type __VLS_StyleScopedClasses = {} &
{ 'analysis-container'?: boolean; } &
{ 'chart-placeholder'?: boolean; } &
{ 'chart-section'?: boolean; } &
{ 'chart'?: boolean; } &
{ 'filter-group'?: boolean; } &
{ 'filter-group'?: boolean; } &
{ 'filter-group'?: boolean; } &
{ 'filter-group'?: boolean; } &
{ 'filter-group'?: boolean; } &
{ 'filter-group'?: boolean; };
let __VLS_styleScopedClasses!: __VLS_StyleScopedClasses | keyof __VLS_StyleScopedClasses | (keyof __VLS_StyleScopedClasses)[];
/* CSS variable injection */
/* CSS variable injection end */
let __VLS_resolvedLocalAndGlobalComponents!: {};
__VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div;
__VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label; __VLS_intrinsicElements.label;
__VLS_intrinsicElements.input; __VLS_intrinsicElements.input; __VLS_intrinsicElements.input; __VLS_intrinsicElements.input;
__VLS_intrinsicElements.select; __VLS_intrinsicElements.select; __VLS_intrinsicElements.select; __VLS_intrinsicElements.select;
__VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option; __VLS_intrinsicElements.option;
__VLS_intrinsicElements.button; __VLS_intrinsicElements.button; __VLS_intrinsicElements.button; __VLS_intrinsicElements.button; __VLS_intrinsicElements.button; __VLS_intrinsicElements.button;
__VLS_intrinsicElements.h3; __VLS_intrinsicElements.h3; __VLS_intrinsicElements.h3; __VLS_intrinsicElements.h3; __VLS_intrinsicElements.h3; __VLS_intrinsicElements.h3;
{
const __VLS_0 = __VLS_intrinsicElements["div"];
const __VLS_1 = __VLS_elementAsFunctionalComponent(__VLS_0);
const __VLS_2 = __VLS_1({ ...{}, class: ("analysis-container"), }, ...__VLS_functionalComponentArgsRest(__VLS_1));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_0, typeof __VLS_2> & Record<string, unknown>) => void)({ ...{}, class: ("analysis-container"), });
const __VLS_3 = __VLS_pickFunctionalComponentCtx(__VLS_0, __VLS_2)!;
let __VLS_4!: __VLS_NormalizeEmits<typeof __VLS_3.emit>;
{
const __VLS_5 = __VLS_intrinsicElements["div"];
const __VLS_6 = __VLS_elementAsFunctionalComponent(__VLS_5);
const __VLS_7 = __VLS_6({ ...{}, class: ("chart-placeholder"), }, ...__VLS_functionalComponentArgsRest(__VLS_6));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_5, typeof __VLS_7> & Record<string, unknown>) => void)({ ...{}, class: ("chart-placeholder"), });
const __VLS_8 = __VLS_pickFunctionalComponentCtx(__VLS_5, __VLS_7)!;
let __VLS_9!: __VLS_NormalizeEmits<typeof __VLS_8.emit>;
{
const __VLS_10 = __VLS_intrinsicElements["div"];
const __VLS_11 = __VLS_elementAsFunctionalComponent(__VLS_10);
const __VLS_12 = __VLS_11({ ...{}, class: ("filter-group"), }, ...__VLS_functionalComponentArgsRest(__VLS_11));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_10, typeof __VLS_12> & Record<string, unknown>) => void)({ ...{}, class: ("filter-group"), });
const __VLS_13 = __VLS_pickFunctionalComponentCtx(__VLS_10, __VLS_12)!;
let __VLS_14!: __VLS_NormalizeEmits<typeof __VLS_13.emit>;
{
const __VLS_15 = __VLS_intrinsicElements["label"];
const __VLS_16 = __VLS_elementAsFunctionalComponent(__VLS_15);
const __VLS_17 = __VLS_16({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_16));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_15, typeof __VLS_17> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_18 = __VLS_pickFunctionalComponentCtx(__VLS_15, __VLS_17)!;
let __VLS_19!: __VLS_NormalizeEmits<typeof __VLS_18.emit>;
{
const __VLS_20 = __VLS_intrinsicElements["input"];
const __VLS_21 = __VLS_elementAsFunctionalComponent(__VLS_20);
const __VLS_22 = __VLS_21({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), }, ...__VLS_functionalComponentArgsRest(__VLS_21));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_20, typeof __VLS_22> & Record<string, unknown>) => void)({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), });
const __VLS_23 = __VLS_pickFunctionalComponentCtx(__VLS_20, __VLS_22)!;
let __VLS_24!: __VLS_NormalizeEmits<typeof __VLS_23.emit>;
(__VLS_ctx.startYear);
}
(__VLS_18.slots!).default;
}
{
const __VLS_25 = __VLS_intrinsicElements["label"];
const __VLS_26 = __VLS_elementAsFunctionalComponent(__VLS_25);
const __VLS_27 = __VLS_26({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_26));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_25, typeof __VLS_27> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_28 = __VLS_pickFunctionalComponentCtx(__VLS_25, __VLS_27)!;
let __VLS_29!: __VLS_NormalizeEmits<typeof __VLS_28.emit>;
{
const __VLS_30 = __VLS_intrinsicElements["input"];
const __VLS_31 = __VLS_elementAsFunctionalComponent(__VLS_30);
const __VLS_32 = __VLS_31({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), }, ...__VLS_functionalComponentArgsRest(__VLS_31));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_30, typeof __VLS_32> & Record<string, unknown>) => void)({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), });
const __VLS_33 = __VLS_pickFunctionalComponentCtx(__VLS_30, __VLS_32)!;
let __VLS_34!: __VLS_NormalizeEmits<typeof __VLS_33.emit>;
(__VLS_ctx.endYear);
}
(__VLS_28.slots!).default;
}
{
const __VLS_35 = __VLS_intrinsicElements["label"];
const __VLS_36 = __VLS_elementAsFunctionalComponent(__VLS_35);
const __VLS_37 = __VLS_36({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_36));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_35, typeof __VLS_37> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_38 = __VLS_pickFunctionalComponentCtx(__VLS_35, __VLS_37)!;
let __VLS_39!: __VLS_NormalizeEmits<typeof __VLS_38.emit>;
{
const __VLS_40 = __VLS_intrinsicElements["select"];
const __VLS_41 = __VLS_elementAsFunctionalComponent(__VLS_40);
const __VLS_42 = __VLS_41({ ...{}, value: ((__VLS_ctx.selectedCountry)), }, ...__VLS_functionalComponentArgsRest(__VLS_41));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_40, typeof __VLS_42> & Record<string, unknown>) => void)({ ...{}, value: ((__VLS_ctx.selectedCountry)), });
const __VLS_43 = __VLS_pickFunctionalComponentCtx(__VLS_40, __VLS_42)!;
let __VLS_44!: __VLS_NormalizeEmits<typeof __VLS_43.emit>;
{
const __VLS_45 = __VLS_intrinsicElements["option"];
const __VLS_46 = __VLS_elementAsFunctionalComponent(__VLS_45);
const __VLS_47 = __VLS_46({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_46));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_45, typeof __VLS_47> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_48 = __VLS_pickFunctionalComponentCtx(__VLS_45, __VLS_47)!;
let __VLS_49!: __VLS_NormalizeEmits<typeof __VLS_48.emit>;
(__VLS_48.slots!).default;
}
{
const __VLS_50 = __VLS_intrinsicElements["option"];
const __VLS_51 = __VLS_elementAsFunctionalComponent(__VLS_50);
const __VLS_52 = __VLS_51({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_51));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_50, typeof __VLS_52> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_53 = __VLS_pickFunctionalComponentCtx(__VLS_50, __VLS_52)!;
let __VLS_54!: __VLS_NormalizeEmits<typeof __VLS_53.emit>;
(__VLS_53.slots!).default;
}
{
const __VLS_55 = __VLS_intrinsicElements["option"];
const __VLS_56 = __VLS_elementAsFunctionalComponent(__VLS_55);
const __VLS_57 = __VLS_56({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_56));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_55, typeof __VLS_57> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_58 = __VLS_pickFunctionalComponentCtx(__VLS_55, __VLS_57)!;
let __VLS_59!: __VLS_NormalizeEmits<typeof __VLS_58.emit>;
(__VLS_58.slots!).default;
}
{
const __VLS_60 = __VLS_intrinsicElements["option"];
const __VLS_61 = __VLS_elementAsFunctionalComponent(__VLS_60);
const __VLS_62 = __VLS_61({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_61));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_60, typeof __VLS_62> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_63 = __VLS_pickFunctionalComponentCtx(__VLS_60, __VLS_62)!;
let __VLS_64!: __VLS_NormalizeEmits<typeof __VLS_63.emit>;
(__VLS_63.slots!).default;
}
{
const __VLS_65 = __VLS_intrinsicElements["option"];
const __VLS_66 = __VLS_elementAsFunctionalComponent(__VLS_65);
const __VLS_67 = __VLS_66({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_66));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_65, typeof __VLS_67> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_68 = __VLS_pickFunctionalComponentCtx(__VLS_65, __VLS_67)!;
let __VLS_69!: __VLS_NormalizeEmits<typeof __VLS_68.emit>;
(__VLS_68.slots!).default;
}
(__VLS_43.slots!).default;
}
(__VLS_38.slots!).default;
}
{
const __VLS_70 = __VLS_intrinsicElements["button"];
const __VLS_71 = __VLS_elementAsFunctionalComponent(__VLS_70);
const __VLS_72 = __VLS_71({ ...{ onClick: {} as any, }, }, ...__VLS_functionalComponentArgsRest(__VLS_71));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_70, typeof __VLS_72> & Record<string, unknown>) => void)({ ...{ onClick: {} as any, }, });
const __VLS_73 = __VLS_pickFunctionalComponentCtx(__VLS_70, __VLS_72)!;
let __VLS_74!: __VLS_NormalizeEmits<typeof __VLS_73.emit>;
let __VLS_75 = { 'click': __VLS_pickEvent(__VLS_74['click'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_71, typeof __VLS_72>).onClick) };
__VLS_75 = { click: (__VLS_ctx.updateYearChart) };
(__VLS_73.slots!).default;
}
(__VLS_13.slots!).default;
}
{
const __VLS_76 = __VLS_intrinsicElements["div"];
const __VLS_77 = __VLS_elementAsFunctionalComponent(__VLS_76);
const __VLS_78 = __VLS_77({ ...{}, class: ("chart-section"), }, ...__VLS_functionalComponentArgsRest(__VLS_77));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_76, typeof __VLS_78> & Record<string, unknown>) => void)({ ...{}, class: ("chart-section"), });
const __VLS_79 = __VLS_pickFunctionalComponentCtx(__VLS_76, __VLS_78)!;
let __VLS_80!: __VLS_NormalizeEmits<typeof __VLS_79.emit>;
{
const __VLS_81 = __VLS_intrinsicElements["h3"];
const __VLS_82 = __VLS_elementAsFunctionalComponent(__VLS_81);
const __VLS_83 = __VLS_82({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_82));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_81, typeof __VLS_83> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_84 = __VLS_pickFunctionalComponentCtx(__VLS_81, __VLS_83)!;
let __VLS_85!: __VLS_NormalizeEmits<typeof __VLS_84.emit>;
(__VLS_84.slots!).default;
}
{
const __VLS_86 = __VLS_intrinsicElements["div"];
const __VLS_87 = __VLS_elementAsFunctionalComponent(__VLS_86);
const __VLS_88 = __VLS_87({ ...{}, ref: ("yearChart"), class: ("chart"), }, ...__VLS_functionalComponentArgsRest(__VLS_87));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_86, typeof __VLS_88> & Record<string, unknown>) => void)({ ...{}, ref: ("yearChart"), class: ("chart"), });
const __VLS_89 = __VLS_pickFunctionalComponentCtx(__VLS_86, __VLS_88)!;
let __VLS_90!: __VLS_NormalizeEmits<typeof __VLS_89.emit>;
// @ts-ignore
(__VLS_ctx.yearChart);
}
(__VLS_79.slots!).default;
}
{
const __VLS_91 = __VLS_intrinsicElements["div"];
const __VLS_92 = __VLS_elementAsFunctionalComponent(__VLS_91);
const __VLS_93 = __VLS_92({ ...{}, class: ("filter-group"), }, ...__VLS_functionalComponentArgsRest(__VLS_92));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_91, typeof __VLS_93> & Record<string, unknown>) => void)({ ...{}, class: ("filter-group"), });
const __VLS_94 = __VLS_pickFunctionalComponentCtx(__VLS_91, __VLS_93)!;
let __VLS_95!: __VLS_NormalizeEmits<typeof __VLS_94.emit>;
{
const __VLS_96 = __VLS_intrinsicElements["label"];
const __VLS_97 = __VLS_elementAsFunctionalComponent(__VLS_96);
const __VLS_98 = __VLS_97({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_97));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_96, typeof __VLS_98> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_99 = __VLS_pickFunctionalComponentCtx(__VLS_96, __VLS_98)!;
let __VLS_100!: __VLS_NormalizeEmits<typeof __VLS_99.emit>;
{
const __VLS_101 = __VLS_intrinsicElements["input"];
const __VLS_102 = __VLS_elementAsFunctionalComponent(__VLS_101);
const __VLS_103 = __VLS_102({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), }, ...__VLS_functionalComponentArgsRest(__VLS_102));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_101, typeof __VLS_103> & Record<string, unknown>) => void)({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), });
const __VLS_104 = __VLS_pickFunctionalComponentCtx(__VLS_101, __VLS_103)!;
let __VLS_105!: __VLS_NormalizeEmits<typeof __VLS_104.emit>;
(__VLS_ctx.selectedMonthYear);
}
(__VLS_99.slots!).default;
}
{
const __VLS_106 = __VLS_intrinsicElements["label"];
const __VLS_107 = __VLS_elementAsFunctionalComponent(__VLS_106);
const __VLS_108 = __VLS_107({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_107));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_106, typeof __VLS_108> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_109 = __VLS_pickFunctionalComponentCtx(__VLS_106, __VLS_108)!;
let __VLS_110!: __VLS_NormalizeEmits<typeof __VLS_109.emit>;
{
const __VLS_111 = __VLS_intrinsicElements["select"];
const __VLS_112 = __VLS_elementAsFunctionalComponent(__VLS_111);
const __VLS_113 = __VLS_112({ ...{}, value: ((__VLS_ctx.selectedMonthCountry)), }, ...__VLS_functionalComponentArgsRest(__VLS_112));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_111, typeof __VLS_113> & Record<string, unknown>) => void)({ ...{}, value: ((__VLS_ctx.selectedMonthCountry)), });
const __VLS_114 = __VLS_pickFunctionalComponentCtx(__VLS_111, __VLS_113)!;
let __VLS_115!: __VLS_NormalizeEmits<typeof __VLS_114.emit>;
{
const __VLS_116 = __VLS_intrinsicElements["option"];
const __VLS_117 = __VLS_elementAsFunctionalComponent(__VLS_116);
const __VLS_118 = __VLS_117({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_117));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_116, typeof __VLS_118> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_119 = __VLS_pickFunctionalComponentCtx(__VLS_116, __VLS_118)!;
let __VLS_120!: __VLS_NormalizeEmits<typeof __VLS_119.emit>;
(__VLS_119.slots!).default;
}
{
const __VLS_121 = __VLS_intrinsicElements["option"];
const __VLS_122 = __VLS_elementAsFunctionalComponent(__VLS_121);
const __VLS_123 = __VLS_122({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_122));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_121, typeof __VLS_123> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_124 = __VLS_pickFunctionalComponentCtx(__VLS_121, __VLS_123)!;
let __VLS_125!: __VLS_NormalizeEmits<typeof __VLS_124.emit>;
(__VLS_124.slots!).default;
}
{
const __VLS_126 = __VLS_intrinsicElements["option"];
const __VLS_127 = __VLS_elementAsFunctionalComponent(__VLS_126);
const __VLS_128 = __VLS_127({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_127));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_126, typeof __VLS_128> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_129 = __VLS_pickFunctionalComponentCtx(__VLS_126, __VLS_128)!;
let __VLS_130!: __VLS_NormalizeEmits<typeof __VLS_129.emit>;
(__VLS_129.slots!).default;
}
{
const __VLS_131 = __VLS_intrinsicElements["option"];
const __VLS_132 = __VLS_elementAsFunctionalComponent(__VLS_131);
const __VLS_133 = __VLS_132({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_132));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_131, typeof __VLS_133> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_134 = __VLS_pickFunctionalComponentCtx(__VLS_131, __VLS_133)!;
let __VLS_135!: __VLS_NormalizeEmits<typeof __VLS_134.emit>;
(__VLS_134.slots!).default;
}
{
const __VLS_136 = __VLS_intrinsicElements["option"];
const __VLS_137 = __VLS_elementAsFunctionalComponent(__VLS_136);
const __VLS_138 = __VLS_137({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_137));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_136, typeof __VLS_138> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_139 = __VLS_pickFunctionalComponentCtx(__VLS_136, __VLS_138)!;
let __VLS_140!: __VLS_NormalizeEmits<typeof __VLS_139.emit>;
(__VLS_139.slots!).default;
}
(__VLS_114.slots!).default;
}
(__VLS_109.slots!).default;
}
{
const __VLS_141 = __VLS_intrinsicElements["button"];
const __VLS_142 = __VLS_elementAsFunctionalComponent(__VLS_141);
const __VLS_143 = __VLS_142({ ...{ onClick: {} as any, }, }, ...__VLS_functionalComponentArgsRest(__VLS_142));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_141, typeof __VLS_143> & Record<string, unknown>) => void)({ ...{ onClick: {} as any, }, });
const __VLS_144 = __VLS_pickFunctionalComponentCtx(__VLS_141, __VLS_143)!;
let __VLS_145!: __VLS_NormalizeEmits<typeof __VLS_144.emit>;
let __VLS_146 = { 'click': __VLS_pickEvent(__VLS_145['click'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_142, typeof __VLS_143>).onClick) };
__VLS_146 = { click: (__VLS_ctx.updateMonthChart) };
(__VLS_144.slots!).default;
}
(__VLS_94.slots!).default;
}
{
const __VLS_147 = __VLS_intrinsicElements["div"];
const __VLS_148 = __VLS_elementAsFunctionalComponent(__VLS_147);
const __VLS_149 = __VLS_148({ ...{}, class: ("chart-section"), }, ...__VLS_functionalComponentArgsRest(__VLS_148));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_147, typeof __VLS_149> & Record<string, unknown>) => void)({ ...{}, class: ("chart-section"), });
const __VLS_150 = __VLS_pickFunctionalComponentCtx(__VLS_147, __VLS_149)!;
let __VLS_151!: __VLS_NormalizeEmits<typeof __VLS_150.emit>;
{
const __VLS_152 = __VLS_intrinsicElements["h3"];
const __VLS_153 = __VLS_elementAsFunctionalComponent(__VLS_152);
const __VLS_154 = __VLS_153({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_153));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_152, typeof __VLS_154> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_155 = __VLS_pickFunctionalComponentCtx(__VLS_152, __VLS_154)!;
let __VLS_156!: __VLS_NormalizeEmits<typeof __VLS_155.emit>;
(__VLS_155.slots!).default;
}
{
const __VLS_157 = __VLS_intrinsicElements["div"];
const __VLS_158 = __VLS_elementAsFunctionalComponent(__VLS_157);
const __VLS_159 = __VLS_158({ ...{}, ref: ("monthChart"), class: ("chart"), }, ...__VLS_functionalComponentArgsRest(__VLS_158));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_157, typeof __VLS_159> & Record<string, unknown>) => void)({ ...{}, ref: ("monthChart"), class: ("chart"), });
const __VLS_160 = __VLS_pickFunctionalComponentCtx(__VLS_157, __VLS_159)!;
let __VLS_161!: __VLS_NormalizeEmits<typeof __VLS_160.emit>;
// @ts-ignore
(__VLS_ctx.monthChart);
}
(__VLS_150.slots!).default;
}
{
const __VLS_162 = __VLS_intrinsicElements["div"];
const __VLS_163 = __VLS_elementAsFunctionalComponent(__VLS_162);
const __VLS_164 = __VLS_163({ ...{}, class: ("filter-group"), }, ...__VLS_functionalComponentArgsRest(__VLS_163));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_162, typeof __VLS_164> & Record<string, unknown>) => void)({ ...{}, class: ("filter-group"), });
const __VLS_165 = __VLS_pickFunctionalComponentCtx(__VLS_162, __VLS_164)!;
let __VLS_166!: __VLS_NormalizeEmits<typeof __VLS_165.emit>;
{
const __VLS_167 = __VLS_intrinsicElements["label"];
const __VLS_168 = __VLS_elementAsFunctionalComponent(__VLS_167);
const __VLS_169 = __VLS_168({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_168));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_167, typeof __VLS_169> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_170 = __VLS_pickFunctionalComponentCtx(__VLS_167, __VLS_169)!;
let __VLS_171!: __VLS_NormalizeEmits<typeof __VLS_170.emit>;
{
const __VLS_172 = __VLS_intrinsicElements["input"];
const __VLS_173 = __VLS_elementAsFunctionalComponent(__VLS_172);
const __VLS_174 = __VLS_173({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), }, ...__VLS_functionalComponentArgsRest(__VLS_173));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_172, typeof __VLS_174> & Record<string, unknown>) => void)({ ...{}, type: ("number"), min: ("2000"), max: ("2025"), });
const __VLS_175 = __VLS_pickFunctionalComponentCtx(__VLS_172, __VLS_174)!;
let __VLS_176!: __VLS_NormalizeEmits<typeof __VLS_175.emit>;
(__VLS_ctx.selectedRegionYear);
}
(__VLS_170.slots!).default;
}
{
const __VLS_177 = __VLS_intrinsicElements["button"];
const __VLS_178 = __VLS_elementAsFunctionalComponent(__VLS_177);
const __VLS_179 = __VLS_178({ ...{ onClick: {} as any, }, }, ...__VLS_functionalComponentArgsRest(__VLS_178));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_177, typeof __VLS_179> & Record<string, unknown>) => void)({ ...{ onClick: {} as any, }, });
const __VLS_180 = __VLS_pickFunctionalComponentCtx(__VLS_177, __VLS_179)!;
let __VLS_181!: __VLS_NormalizeEmits<typeof __VLS_180.emit>;
let __VLS_182 = { 'click': __VLS_pickEvent(__VLS_181['click'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_178, typeof __VLS_179>).onClick) };
__VLS_182 = { click: (__VLS_ctx.updateRegionChart) };
(__VLS_180.slots!).default;
}
(__VLS_165.slots!).default;
}
{
const __VLS_183 = __VLS_intrinsicElements["div"];
const __VLS_184 = __VLS_elementAsFunctionalComponent(__VLS_183);
const __VLS_185 = __VLS_184({ ...{}, class: ("chart-section"), }, ...__VLS_functionalComponentArgsRest(__VLS_184));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_183, typeof __VLS_185> & Record<string, unknown>) => void)({ ...{}, class: ("chart-section"), });
const __VLS_186 = __VLS_pickFunctionalComponentCtx(__VLS_183, __VLS_185)!;
let __VLS_187!: __VLS_NormalizeEmits<typeof __VLS_186.emit>;
{
const __VLS_188 = __VLS_intrinsicElements["h3"];
const __VLS_189 = __VLS_elementAsFunctionalComponent(__VLS_188);
const __VLS_190 = __VLS_189({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_189));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_188, typeof __VLS_190> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_191 = __VLS_pickFunctionalComponentCtx(__VLS_188, __VLS_190)!;
let __VLS_192!: __VLS_NormalizeEmits<typeof __VLS_191.emit>;
(__VLS_191.slots!).default;
}
{
const __VLS_193 = __VLS_intrinsicElements["div"];
const __VLS_194 = __VLS_elementAsFunctionalComponent(__VLS_193);
const __VLS_195 = __VLS_194({ ...{}, ref: ("regionChart"), class: ("chart"), }, ...__VLS_functionalComponentArgsRest(__VLS_194));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_193, typeof __VLS_195> & Record<string, unknown>) => void)({ ...{}, ref: ("regionChart"), class: ("chart"), });
const __VLS_196 = __VLS_pickFunctionalComponentCtx(__VLS_193, __VLS_195)!;
let __VLS_197!: __VLS_NormalizeEmits<typeof __VLS_196.emit>;
// @ts-ignore
(__VLS_ctx.regionChart);
}
(__VLS_186.slots!).default;
}
(__VLS_8.slots!).default;
}
(__VLS_3.slots!).default;
}
if (typeof __VLS_styleScopedClasses === 'object' && !Array.isArray(__VLS_styleScopedClasses)) {
__VLS_styleScopedClasses["analysis-container"];
__VLS_styleScopedClasses["chart-placeholder"];
__VLS_styleScopedClasses["filter-group"];
__VLS_styleScopedClasses["chart-section"];
__VLS_styleScopedClasses["chart"];
__VLS_styleScopedClasses["filter-group"];
__VLS_styleScopedClasses["chart-section"];
__VLS_styleScopedClasses["chart"];
__VLS_styleScopedClasses["filter-group"];
__VLS_styleScopedClasses["chart-section"];
__VLS_styleScopedClasses["chart"];
}
var __VLS_slots!: {};
// @ts-ignore
[startYear, endYear, selectedCountry, selectedCountry, updateYearChart, yearChart, selectedMonthYear, selectedMonthCountry, selectedMonthCountry, updateMonthChart, monthChart, selectedRegionYear, updateRegionChart, regionChart,];
return __VLS_slots;
}
