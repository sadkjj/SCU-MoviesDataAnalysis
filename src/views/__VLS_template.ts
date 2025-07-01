import { __VLS_internalComponent, __VLS_componentsOption, __VLS_name, handleLogin, username, password } from './Login.vue';

function __VLS_template() {
let __VLS_ctx!: InstanceType<__VLS_PickNotAny<typeof __VLS_internalComponent, new () => {}>> & {};
/* Components */
let __VLS_otherComponents!: NonNullable<typeof __VLS_internalComponent extends { components: infer C; } ? C : {}> & typeof __VLS_componentsOption;
let __VLS_own!: __VLS_SelfComponent<typeof __VLS_name, typeof __VLS_internalComponent & (new () => { $slots: typeof __VLS_slots; })>;
let __VLS_localComponents!: typeof __VLS_otherComponents & Omit<typeof __VLS_own, keyof typeof __VLS_otherComponents>;
let __VLS_components!: typeof __VLS_localComponents & __VLS_GlobalComponents & typeof __VLS_ctx;
/* Style Scoped */
type __VLS_StyleScopedClasses = {} &
{ 'auth-container'?: boolean; } &
{ 'switch'?: boolean; } &
{ 'switch'?: boolean; } &
{ 'switch'?: boolean; };
let __VLS_styleScopedClasses!: __VLS_StyleScopedClasses | keyof __VLS_StyleScopedClasses | (keyof __VLS_StyleScopedClasses)[];
/* CSS variable injection */
/* CSS variable injection end */
let __VLS_resolvedLocalAndGlobalComponents!: {} &
__VLS_WithComponent<'RouterLink', typeof __VLS_localComponents, "RouterLink", "routerLink", "router-link">;
__VLS_intrinsicElements.div; __VLS_intrinsicElements.div;
__VLS_intrinsicElements.h2; __VLS_intrinsicElements.h2;
__VLS_intrinsicElements.form; __VLS_intrinsicElements.form;
__VLS_intrinsicElements.input; __VLS_intrinsicElements.input;
__VLS_intrinsicElements.button; __VLS_intrinsicElements.button;
__VLS_intrinsicElements.p; __VLS_intrinsicElements.p; __VLS_intrinsicElements.p; __VLS_intrinsicElements.p;
__VLS_components.RouterLink; __VLS_components.RouterLink; __VLS_components.routerLink; __VLS_components.routerLink; __VLS_components["router-link"]; __VLS_components["router-link"];
// @ts-ignore
[RouterLink, RouterLink,];
{
const __VLS_0 = __VLS_intrinsicElements["div"];
const __VLS_1 = __VLS_elementAsFunctionalComponent(__VLS_0);
const __VLS_2 = __VLS_1({ ...{}, class: ("auth-container"), }, ...__VLS_functionalComponentArgsRest(__VLS_1));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_0, typeof __VLS_2> & Record<string, unknown>) => void)({ ...{}, class: ("auth-container"), });
const __VLS_3 = __VLS_pickFunctionalComponentCtx(__VLS_0, __VLS_2)!;
let __VLS_4!: __VLS_NormalizeEmits<typeof __VLS_3.emit>;
{
const __VLS_5 = __VLS_intrinsicElements["h2"];
const __VLS_6 = __VLS_elementAsFunctionalComponent(__VLS_5);
const __VLS_7 = __VLS_6({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_6));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_5, typeof __VLS_7> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_8 = __VLS_pickFunctionalComponentCtx(__VLS_5, __VLS_7)!;
let __VLS_9!: __VLS_NormalizeEmits<typeof __VLS_8.emit>;
(__VLS_8.slots!).default;
}
{
const __VLS_10 = __VLS_intrinsicElements["form"];
const __VLS_11 = __VLS_elementAsFunctionalComponent(__VLS_10);
const __VLS_12 = __VLS_11({ ...{ onSubmit: {} as any, }, }, ...__VLS_functionalComponentArgsRest(__VLS_11));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_10, typeof __VLS_12> & Record<string, unknown>) => void)({ ...{ onSubmit: {} as any, }, });
const __VLS_13 = __VLS_pickFunctionalComponentCtx(__VLS_10, __VLS_12)!;
let __VLS_14!: __VLS_NormalizeEmits<typeof __VLS_13.emit>;
let __VLS_15 = { 'submit': __VLS_pickEvent(__VLS_14['submit'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_11, typeof __VLS_12>).onSubmit) };
__VLS_15 = { submit: (__VLS_ctx.handleLogin) };
{
const __VLS_16 = __VLS_intrinsicElements["input"];
const __VLS_17 = __VLS_elementAsFunctionalComponent(__VLS_16);
const __VLS_18 = __VLS_17({ ...{}, value: ((__VLS_ctx.username)), type: ("text"), placeholder: ("用户名"), required: (true), }, ...__VLS_functionalComponentArgsRest(__VLS_17));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_16, typeof __VLS_18> & Record<string, unknown>) => void)({ ...{}, value: ((__VLS_ctx.username)), type: ("text"), placeholder: ("用户名"), required: (true), });
const __VLS_19 = __VLS_pickFunctionalComponentCtx(__VLS_16, __VLS_18)!;
let __VLS_20!: __VLS_NormalizeEmits<typeof __VLS_19.emit>;
}
{
const __VLS_21 = __VLS_intrinsicElements["input"];
const __VLS_22 = __VLS_elementAsFunctionalComponent(__VLS_21);
const __VLS_23 = __VLS_22({ ...{}, type: ("password"), placeholder: ("密码"), required: (true), }, ...__VLS_functionalComponentArgsRest(__VLS_22));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_21, typeof __VLS_23> & Record<string, unknown>) => void)({ ...{}, type: ("password"), placeholder: ("密码"), required: (true), });
const __VLS_24 = __VLS_pickFunctionalComponentCtx(__VLS_21, __VLS_23)!;
let __VLS_25!: __VLS_NormalizeEmits<typeof __VLS_24.emit>;
(__VLS_ctx.password);
}
{
const __VLS_26 = __VLS_intrinsicElements["button"];
const __VLS_27 = __VLS_elementAsFunctionalComponent(__VLS_26);
const __VLS_28 = __VLS_27({ ...{}, type: ("submit"), }, ...__VLS_functionalComponentArgsRest(__VLS_27));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_26, typeof __VLS_28> & Record<string, unknown>) => void)({ ...{}, type: ("submit"), });
const __VLS_29 = __VLS_pickFunctionalComponentCtx(__VLS_26, __VLS_28)!;
let __VLS_30!: __VLS_NormalizeEmits<typeof __VLS_29.emit>;
(__VLS_29.slots!).default;
}
if (__VLS_ctx.errorMessage) {
{
const __VLS_31 = __VLS_intrinsicElements["p"];
const __VLS_32 = __VLS_elementAsFunctionalComponent(__VLS_31);
const __VLS_33 = __VLS_32({ ...{}, class: ("error"), }, ...__VLS_functionalComponentArgsRest(__VLS_32));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_31, typeof __VLS_33> & Record<string, unknown>) => void)({ ...{}, class: ("error"), });
const __VLS_34 = __VLS_pickFunctionalComponentCtx(__VLS_31, __VLS_33)!;
let __VLS_35!: __VLS_NormalizeEmits<typeof __VLS_34.emit>;
(__VLS_ctx.errorMessage);
(__VLS_34.slots!).default;
}
// @ts-ignore
[handleLogin, username, username, password, errorMessage, errorMessage,];
}
{
const __VLS_36 = __VLS_intrinsicElements["p"];
const __VLS_37 = __VLS_elementAsFunctionalComponent(__VLS_36);
const __VLS_38 = __VLS_37({ ...{}, class: ("switch"), }, ...__VLS_functionalComponentArgsRest(__VLS_37));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_36, typeof __VLS_38> & Record<string, unknown>) => void)({ ...{}, class: ("switch"), });
const __VLS_39 = __VLS_pickFunctionalComponentCtx(__VLS_36, __VLS_38)!;
let __VLS_40!: __VLS_NormalizeEmits<typeof __VLS_39.emit>;
{
const __VLS_41 = ({} as 'RouterLink' extends keyof typeof __VLS_ctx ? { 'RouterLink': typeof __VLS_ctx.RouterLink; } : 'routerLink' extends keyof typeof __VLS_ctx ? { 'RouterLink': typeof __VLS_ctx.routerLink; } : 'router-link' extends keyof typeof __VLS_ctx ? { 'RouterLink': (typeof __VLS_ctx)["router-link"]; } : typeof __VLS_resolvedLocalAndGlobalComponents).RouterLink;
const __VLS_42 = __VLS_asFunctionalComponent(__VLS_41, new __VLS_41({ ...{}, to: ("/register"), }));
({} as { RouterLink: typeof __VLS_41; }).RouterLink;
({} as { RouterLink: typeof __VLS_41; }).RouterLink;
const __VLS_43 = __VLS_42({ ...{}, to: ("/register"), }, ...__VLS_functionalComponentArgsRest(__VLS_42));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_41, typeof __VLS_43> & Record<string, unknown>) => void)({ ...{}, to: ("/register"), });
const __VLS_44 = __VLS_pickFunctionalComponentCtx(__VLS_41, __VLS_43)!;
let __VLS_45!: __VLS_NormalizeEmits<typeof __VLS_44.emit>;
(__VLS_44.slots!).default;
}
(__VLS_39.slots!).default;
}
(__VLS_13.slots!).default;
}
(__VLS_3.slots!).default;
}
if (typeof __VLS_styleScopedClasses === 'object' && !Array.isArray(__VLS_styleScopedClasses)) {
__VLS_styleScopedClasses["auth-container"];
__VLS_styleScopedClasses["error"];
__VLS_styleScopedClasses["switch"];
}
var __VLS_slots!: {};
return __VLS_slots;
}
