import UserProfile from '@/components/admin/UserProfile.vue';
import UserEditDialog from '@/components/admin/UserEditDialog.vue';
import { currentUser } from '@/stores/user';
import { __VLS_internalComponent, __VLS_componentsOption, __VLS_name, userList, roleLabel, openEdit, showDialog, selectedUser, handleUpdate } from './UserAdmin.vue';

function __VLS_template() {
let __VLS_ctx!: InstanceType<__VLS_PickNotAny<typeof __VLS_internalComponent, new () => {}>> & {};
/* Components */
let __VLS_otherComponents!: NonNullable<typeof __VLS_internalComponent extends { components: infer C; } ? C : {}> & typeof __VLS_componentsOption;
let __VLS_own!: __VLS_SelfComponent<typeof __VLS_name, typeof __VLS_internalComponent & (new () => { $slots: typeof __VLS_slots; })>;
let __VLS_localComponents!: typeof __VLS_otherComponents & Omit<typeof __VLS_own, keyof typeof __VLS_otherComponents>;
let __VLS_components!: typeof __VLS_localComponents & __VLS_GlobalComponents & typeof __VLS_ctx;
/* Style Scoped */
type __VLS_StyleScopedClasses = {} &
{ 'user-admin'?: boolean; } &
{ 'user-table'?: boolean; } &
{ 'user-table'?: boolean; } &
{ 'user-table'?: boolean; } &
{ 'user-table'?: boolean; };
let __VLS_styleScopedClasses!: __VLS_StyleScopedClasses | keyof __VLS_StyleScopedClasses | (keyof __VLS_StyleScopedClasses)[];
/* CSS variable injection */
/* CSS variable injection end */
let __VLS_resolvedLocalAndGlobalComponents!: {} &
__VLS_WithComponent<'UserProfile', typeof __VLS_localComponents, "UserProfile", "UserProfile", "UserProfile"> &
__VLS_WithComponent<'UserEditDialog', typeof __VLS_localComponents, "UserEditDialog", "UserEditDialog", "UserEditDialog">;
__VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div; __VLS_intrinsicElements.div;
__VLS_intrinsicElements.h2; __VLS_intrinsicElements.h2;
__VLS_components.UserProfile;
// @ts-ignore
[UserProfile,];
__VLS_intrinsicElements.table; __VLS_intrinsicElements.table;
__VLS_intrinsicElements.thead; __VLS_intrinsicElements.thead;
__VLS_intrinsicElements.tr; __VLS_intrinsicElements.tr; __VLS_intrinsicElements.tr; __VLS_intrinsicElements.tr;
__VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th; __VLS_intrinsicElements.th;
__VLS_intrinsicElements.tbody; __VLS_intrinsicElements.tbody;
__VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td; __VLS_intrinsicElements.td;
__VLS_intrinsicElements.button; __VLS_intrinsicElements.button;
__VLS_components.UserEditDialog;
// @ts-ignore
[UserEditDialog,];
{
const __VLS_0 = __VLS_intrinsicElements["div"];
const __VLS_1 = __VLS_elementAsFunctionalComponent(__VLS_0);
const __VLS_2 = __VLS_1({ ...{}, class: ("user-admin"), }, ...__VLS_functionalComponentArgsRest(__VLS_1));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_0, typeof __VLS_2> & Record<string, unknown>) => void)({ ...{}, class: ("user-admin"), });
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
if (__VLS_ctx.currentUser?.role_type !== 1) {
{
const __VLS_10 = ({} as 'UserProfile' extends keyof typeof __VLS_ctx ? { 'UserProfile': typeof __VLS_ctx.UserProfile; } : typeof __VLS_resolvedLocalAndGlobalComponents).UserProfile;
const __VLS_11 = __VLS_asFunctionalComponent(__VLS_10, new __VLS_10({ ...{}, user: ((__VLS_ctx.currentUser)), }));
({} as { UserProfile: typeof __VLS_10; }).UserProfile;
const __VLS_12 = __VLS_11({ ...{}, user: ((__VLS_ctx.currentUser)), }, ...__VLS_functionalComponentArgsRest(__VLS_11));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_10, typeof __VLS_12> & Record<string, unknown>) => void)({ ...{}, user: ((__VLS_ctx.currentUser)), });
const __VLS_13 = __VLS_pickFunctionalComponentCtx(__VLS_10, __VLS_12)!;
let __VLS_14!: __VLS_NormalizeEmits<typeof __VLS_13.emit>;
}
// @ts-ignore
[currentUser, currentUser, currentUser, currentUser,];
}
else {
{
const __VLS_15 = __VLS_intrinsicElements["div"];
const __VLS_16 = __VLS_elementAsFunctionalComponent(__VLS_15);
const __VLS_17 = __VLS_16({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_16));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_15, typeof __VLS_17> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_18 = __VLS_pickFunctionalComponentCtx(__VLS_15, __VLS_17)!;
let __VLS_19!: __VLS_NormalizeEmits<typeof __VLS_18.emit>;
{
const __VLS_20 = __VLS_intrinsicElements["table"];
const __VLS_21 = __VLS_elementAsFunctionalComponent(__VLS_20);
const __VLS_22 = __VLS_21({ ...{}, class: ("user-table"), }, ...__VLS_functionalComponentArgsRest(__VLS_21));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_20, typeof __VLS_22> & Record<string, unknown>) => void)({ ...{}, class: ("user-table"), });
const __VLS_23 = __VLS_pickFunctionalComponentCtx(__VLS_20, __VLS_22)!;
let __VLS_24!: __VLS_NormalizeEmits<typeof __VLS_23.emit>;
{
const __VLS_25 = __VLS_intrinsicElements["thead"];
const __VLS_26 = __VLS_elementAsFunctionalComponent(__VLS_25);
const __VLS_27 = __VLS_26({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_26));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_25, typeof __VLS_27> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_28 = __VLS_pickFunctionalComponentCtx(__VLS_25, __VLS_27)!;
let __VLS_29!: __VLS_NormalizeEmits<typeof __VLS_28.emit>;
{
const __VLS_30 = __VLS_intrinsicElements["tr"];
const __VLS_31 = __VLS_elementAsFunctionalComponent(__VLS_30);
const __VLS_32 = __VLS_31({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_31));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_30, typeof __VLS_32> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_33 = __VLS_pickFunctionalComponentCtx(__VLS_30, __VLS_32)!;
let __VLS_34!: __VLS_NormalizeEmits<typeof __VLS_33.emit>;
{
const __VLS_35 = __VLS_intrinsicElements["th"];
const __VLS_36 = __VLS_elementAsFunctionalComponent(__VLS_35);
const __VLS_37 = __VLS_36({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_36));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_35, typeof __VLS_37> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_38 = __VLS_pickFunctionalComponentCtx(__VLS_35, __VLS_37)!;
let __VLS_39!: __VLS_NormalizeEmits<typeof __VLS_38.emit>;
(__VLS_38.slots!).default;
}
{
const __VLS_40 = __VLS_intrinsicElements["th"];
const __VLS_41 = __VLS_elementAsFunctionalComponent(__VLS_40);
const __VLS_42 = __VLS_41({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_41));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_40, typeof __VLS_42> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_43 = __VLS_pickFunctionalComponentCtx(__VLS_40, __VLS_42)!;
let __VLS_44!: __VLS_NormalizeEmits<typeof __VLS_43.emit>;
(__VLS_43.slots!).default;
}
{
const __VLS_45 = __VLS_intrinsicElements["th"];
const __VLS_46 = __VLS_elementAsFunctionalComponent(__VLS_45);
const __VLS_47 = __VLS_46({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_46));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_45, typeof __VLS_47> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_48 = __VLS_pickFunctionalComponentCtx(__VLS_45, __VLS_47)!;
let __VLS_49!: __VLS_NormalizeEmits<typeof __VLS_48.emit>;
(__VLS_48.slots!).default;
}
{
const __VLS_50 = __VLS_intrinsicElements["th"];
const __VLS_51 = __VLS_elementAsFunctionalComponent(__VLS_50);
const __VLS_52 = __VLS_51({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_51));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_50, typeof __VLS_52> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_53 = __VLS_pickFunctionalComponentCtx(__VLS_50, __VLS_52)!;
let __VLS_54!: __VLS_NormalizeEmits<typeof __VLS_53.emit>;
(__VLS_53.slots!).default;
}
{
const __VLS_55 = __VLS_intrinsicElements["th"];
const __VLS_56 = __VLS_elementAsFunctionalComponent(__VLS_55);
const __VLS_57 = __VLS_56({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_56));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_55, typeof __VLS_57> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_58 = __VLS_pickFunctionalComponentCtx(__VLS_55, __VLS_57)!;
let __VLS_59!: __VLS_NormalizeEmits<typeof __VLS_58.emit>;
(__VLS_58.slots!).default;
}
{
const __VLS_60 = __VLS_intrinsicElements["th"];
const __VLS_61 = __VLS_elementAsFunctionalComponent(__VLS_60);
const __VLS_62 = __VLS_61({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_61));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_60, typeof __VLS_62> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_63 = __VLS_pickFunctionalComponentCtx(__VLS_60, __VLS_62)!;
let __VLS_64!: __VLS_NormalizeEmits<typeof __VLS_63.emit>;
(__VLS_63.slots!).default;
}
{
const __VLS_65 = __VLS_intrinsicElements["th"];
const __VLS_66 = __VLS_elementAsFunctionalComponent(__VLS_65);
const __VLS_67 = __VLS_66({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_66));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_65, typeof __VLS_67> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_68 = __VLS_pickFunctionalComponentCtx(__VLS_65, __VLS_67)!;
let __VLS_69!: __VLS_NormalizeEmits<typeof __VLS_68.emit>;
(__VLS_68.slots!).default;
}
(__VLS_33.slots!).default;
}
(__VLS_28.slots!).default;
}
{
const __VLS_70 = __VLS_intrinsicElements["tbody"];
const __VLS_71 = __VLS_elementAsFunctionalComponent(__VLS_70);
const __VLS_72 = __VLS_71({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_71));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_70, typeof __VLS_72> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_73 = __VLS_pickFunctionalComponentCtx(__VLS_70, __VLS_72)!;
let __VLS_74!: __VLS_NormalizeEmits<typeof __VLS_73.emit>;
for (const [user] of __VLS_getVForSourceType((__VLS_ctx.userList)!)) {
{
const __VLS_75 = __VLS_intrinsicElements["tr"];
const __VLS_76 = __VLS_elementAsFunctionalComponent(__VLS_75);
const __VLS_77 = __VLS_76({ ...{}, key: ((user.user_id)), }, ...__VLS_functionalComponentArgsRest(__VLS_76));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_75, typeof __VLS_77> & Record<string, unknown>) => void)({ ...{}, key: ((user.user_id)), });
const __VLS_78 = __VLS_pickFunctionalComponentCtx(__VLS_75, __VLS_77)!;
let __VLS_79!: __VLS_NormalizeEmits<typeof __VLS_78.emit>;
{
const __VLS_80 = __VLS_intrinsicElements["td"];
const __VLS_81 = __VLS_elementAsFunctionalComponent(__VLS_80);
const __VLS_82 = __VLS_81({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_81));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_80, typeof __VLS_82> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_83 = __VLS_pickFunctionalComponentCtx(__VLS_80, __VLS_82)!;
let __VLS_84!: __VLS_NormalizeEmits<typeof __VLS_83.emit>;
(user.username);
(__VLS_83.slots!).default;
}
{
const __VLS_85 = __VLS_intrinsicElements["td"];
const __VLS_86 = __VLS_elementAsFunctionalComponent(__VLS_85);
const __VLS_87 = __VLS_86({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_86));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_85, typeof __VLS_87> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_88 = __VLS_pickFunctionalComponentCtx(__VLS_85, __VLS_87)!;
let __VLS_89!: __VLS_NormalizeEmits<typeof __VLS_88.emit>;
(user.real_name);
(__VLS_88.slots!).default;
}
{
const __VLS_90 = __VLS_intrinsicElements["td"];
const __VLS_91 = __VLS_elementAsFunctionalComponent(__VLS_90);
const __VLS_92 = __VLS_91({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_91));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_90, typeof __VLS_92> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_93 = __VLS_pickFunctionalComponentCtx(__VLS_90, __VLS_92)!;
let __VLS_94!: __VLS_NormalizeEmits<typeof __VLS_93.emit>;
(user.email);
(__VLS_93.slots!).default;
}
{
const __VLS_95 = __VLS_intrinsicElements["td"];
const __VLS_96 = __VLS_elementAsFunctionalComponent(__VLS_95);
const __VLS_97 = __VLS_96({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_96));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_95, typeof __VLS_97> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_98 = __VLS_pickFunctionalComponentCtx(__VLS_95, __VLS_97)!;
let __VLS_99!: __VLS_NormalizeEmits<typeof __VLS_98.emit>;
(user.phone);
(__VLS_98.slots!).default;
}
{
const __VLS_100 = __VLS_intrinsicElements["td"];
const __VLS_101 = __VLS_elementAsFunctionalComponent(__VLS_100);
const __VLS_102 = __VLS_101({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_101));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_100, typeof __VLS_102> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_103 = __VLS_pickFunctionalComponentCtx(__VLS_100, __VLS_102)!;
let __VLS_104!: __VLS_NormalizeEmits<typeof __VLS_103.emit>;
(__VLS_ctx.roleLabel(user.role_type));
(__VLS_103.slots!).default;
}
{
const __VLS_105 = __VLS_intrinsicElements["td"];
const __VLS_106 = __VLS_elementAsFunctionalComponent(__VLS_105);
const __VLS_107 = __VLS_106({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_106));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_105, typeof __VLS_107> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_108 = __VLS_pickFunctionalComponentCtx(__VLS_105, __VLS_107)!;
let __VLS_109!: __VLS_NormalizeEmits<typeof __VLS_108.emit>;
(user.create_time);
(__VLS_108.slots!).default;
}
{
const __VLS_110 = __VLS_intrinsicElements["td"];
const __VLS_111 = __VLS_elementAsFunctionalComponent(__VLS_110);
const __VLS_112 = __VLS_111({ ...{}, }, ...__VLS_functionalComponentArgsRest(__VLS_111));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_110, typeof __VLS_112> & Record<string, unknown>) => void)({ ...{}, });
const __VLS_113 = __VLS_pickFunctionalComponentCtx(__VLS_110, __VLS_112)!;
let __VLS_114!: __VLS_NormalizeEmits<typeof __VLS_113.emit>;
{
const __VLS_115 = __VLS_intrinsicElements["button"];
const __VLS_116 = __VLS_elementAsFunctionalComponent(__VLS_115);
const __VLS_117 = __VLS_116({ ...{ onClick: {} as any, }, }, ...__VLS_functionalComponentArgsRest(__VLS_116));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_115, typeof __VLS_117> & Record<string, unknown>) => void)({ ...{ onClick: {} as any, }, });
const __VLS_118 = __VLS_pickFunctionalComponentCtx(__VLS_115, __VLS_117)!;
let __VLS_119!: __VLS_NormalizeEmits<typeof __VLS_118.emit>;
let __VLS_120 = { 'click': __VLS_pickEvent(__VLS_119['click'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_116, typeof __VLS_117>).onClick) };
__VLS_120 = {
click: $event => {
if (!(!((__VLS_ctx.currentUser?.role_type !== 1)))) return;
__VLS_ctx.openEdit(user);
// @ts-ignore
[userList, roleLabel, openEdit,];
}
};
(__VLS_118.slots!).default;
}
(__VLS_113.slots!).default;
}
(__VLS_78.slots!).default;
}
}
(__VLS_73.slots!).default;
}
(__VLS_23.slots!).default;
}
(__VLS_18.slots!).default;
}
}
if (__VLS_ctx.showDialog) {
{
const __VLS_121 = ({} as 'UserEditDialog' extends keyof typeof __VLS_ctx ? { 'UserEditDialog': typeof __VLS_ctx.UserEditDialog; } : typeof __VLS_resolvedLocalAndGlobalComponents).UserEditDialog;
const __VLS_122 = __VLS_asFunctionalComponent(__VLS_121, new __VLS_121({ ...{ onClose: {} as any, onUpdate: {} as any, }, user: ((__VLS_ctx.selectedUser)), }));
({} as { UserEditDialog: typeof __VLS_121; }).UserEditDialog;
const __VLS_123 = __VLS_122({ ...{ onClose: {} as any, onUpdate: {} as any, }, user: ((__VLS_ctx.selectedUser)), }, ...__VLS_functionalComponentArgsRest(__VLS_122));
({} as (props: __VLS_FunctionalComponentProps<typeof __VLS_121, typeof __VLS_123> & Record<string, unknown>) => void)({ ...{ onClose: {} as any, onUpdate: {} as any, }, user: ((__VLS_ctx.selectedUser)), });
const __VLS_124 = __VLS_pickFunctionalComponentCtx(__VLS_121, __VLS_123)!;
let __VLS_125!: __VLS_NormalizeEmits<typeof __VLS_124.emit>;
let __VLS_126 = { 'close': __VLS_pickEvent(__VLS_125['close'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_122, typeof __VLS_123>).onClose) };
__VLS_126 = {
close: $event => {
if (!((__VLS_ctx.showDialog))) return;
__VLS_ctx.showDialog = false;
// @ts-ignore
[showDialog, selectedUser, selectedUser, selectedUser, showDialog,];
}
};
let __VLS_127 = { 'update': __VLS_pickEvent(__VLS_125['update'], ({} as __VLS_FunctionalComponentProps<typeof __VLS_122, typeof __VLS_123>).onUpdate) };
__VLS_127 = { update: (__VLS_ctx.handleUpdate) };
}
// @ts-ignore
[handleUpdate,];
}
(__VLS_3.slots!).default;
}
if (typeof __VLS_styleScopedClasses === 'object' && !Array.isArray(__VLS_styleScopedClasses)) {
__VLS_styleScopedClasses["user-admin"];
__VLS_styleScopedClasses["user-table"];
}
var __VLS_slots!: {};
return __VLS_slots;
}
