<script setup lang="ts">
// Импорт иконок
import reels from "../../assets/reels.svg";
import fire from "../../assets/fire.svg";
import sub from "../../assets/sub.svg";
import play from "../../assets/play.svg";
import share from "../../assets/share.svg";
import X from "../../assets/X.svg";
import music from "../../assets/music.svg";
import en from "../../assets/en.svg";
import lang from "../../assets/lang.svg";
import copy from "../../assets/copy.svg";
import arrow from "../../assets/arrow.svg";
import adapt from "../../assets/adapt.svg";

import { computed, ref, watch } from "vue";
import { getPost, type PostData } from "../../features/api/posts";
import { formatierStringDate, formatierText, formatierUserId } from "../../features/utils/formatiers";
import Tag from "./Tag.vue";
import Stat from "./Stat.vue";

const MAX_TEXT_LENGTH = 60;

const props = defineProps<{
    modelValue: boolean;
    postId: number | null;
    userId: string;
}>();

const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();

const post = ref<PostData | null>(null);
const isTextExpanded = ref(false);

watch(
    () => props.postId,
    async (id) => {
        if (!id) return;
        isTextExpanded.value = false;
        const data = await getPost(props.userId, id);
        if (data) {
            post.value = data;
        }
    },
);

function close() {
    emit("update:modelValue", false);
}

// Форматируем дату
const formattedDate = computed(() => {
    if (!post.value?.created_at) return "";
    return formatierStringDate(post.value.created_at);
});

// Форматируем id пользователя
const truncatedUserId = computed(() => {
    if (!post.value?.user_id) return "";
    return formatierUserId(post.value.user_id);
});

// Форматируем текст поста
const truncatedText = computed(() => {
    if (!post.value?.text) return "";
    if (isTextExpanded.value || post.value.text.length <= MAX_TEXT_LENGTH) {
        return post.value.text;
    } else {
        return formatierText(post.value.text, MAX_TEXT_LENGTH);
    }
});

const hasLongText = computed(
    () => (post.value?.text?.length ?? 0) > MAX_TEXT_LENGTH,
);
</script>

<template>
    <Transition name="modal">
        <div v-if="modelValue" class="wrapper" @click.self="close">
            <aside class="modal">
                <div class="videocard videocard_modal">
                    <div class="videocard__top videocard_modal__top">
                        <div class="videocard__video-header">
                            <div class="video-header__left">
                                <div class="video-header__badage blur">
                                    <img
                                        class="video-header__badage-img"
                                        :src="reels"
                                        alt=""
                                    />
                                    <p class="video-header__badage-value">
                                        Reels
                                    </p>
                                </div>
                                <div class="video-header__badage blur">
                                    <img
                                        class="video-header__badage-img"
                                        :src="fire"
                                        alt=""
                                    />
                                    <p class="video-header__badage-value">
                                        X10
                                    </p>
                                </div>
                            </div>
                        </div>
                        <img
                            class="videocard__video-play"
                            :src="play"
                            alt="play"
                        />
                        <img
                            class="videocard__video videocard_modal__video"
                            src="/video.png"
                        />
                    </div>
                    <div class="videocard__bottom videocard_modal__bottom">
                        <div class="videocard__bottom-header">
                            <p class="videocard__date">{{ formattedDate }}</p>
                            <a href="#" class="share">
                                <img :src="share" alt="share" />
                            </a>
                        </div>
                        <div class="videocard__bottom-header">
                            <div class="videocard__user">
                                <img
                                    src="/avatar.png"
                                    alt=""
                                    class="videocard__user-img"
                                />
                                <div class="videocard__user-info">
                                    <a
                                        :href="`/u/${post?.user_id}`"
                                        class="videocard__user-name"
                                        >@{{ truncatedUserId }}</a
                                    >
                                    <p class="videocard__user-subscribes">
                                        384.5K
                                    </p>
                                </div>
                            </div>
                            <button class="videocard__subscribe">
                                <img :src="sub" alt="sub" />
                            </button>
                        </div>
                        <div
                            class="videocard__bottom-text videocard_modal__bottom-text"
                        >
                            <p>{{ truncatedText }}</p>
                            <button
                                v-if="hasLongText"
                                class="text-toggle"
                                @click="isTextExpanded = !isTextExpanded"
                            >
                                {{ isTextExpanded ? "Скрыть" : "Ещё" }}
                            </button>
                        </div>
                    </div>
                    <Stat :value="1.2" type="view"/>
                    <Stat :value="1.2" type="like"/>
                    <Stat :value="1.2" type="comment"/>
                    <Stat :value="1.2" type="repost"/>
                    <Stat :value="1.2" type="er"/>
                </div>
                <div class="video-info">
                    <div class="info">
                        <div class="info__header">
                            <div class="info__header-title">
                                <div class="title">
                                    <p class="title__name">Тема видео</p>
                                    <p class="title__text">{{ post?.title }}</p>
                                    <div class="music-lang">
                                        <div class="music">
                                            <img :src="music" alt="music" />
                                            Tyga – Pop it off
                                        </div>
                                        <div class="lang">
                                            <p class="lang__title">Язык:</p>
                                            <div class="lang__name">
                                                <img :src="en" alt="en" />
                                                Английский
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button class="modal-close icon" @click="close">
                                    <img :src="X" alt="x" />
                                </button>
                            </div>
                        </div>
                        <div class="info__tags">
                            <Tag value="Туториал"/>
                            <Tag value="Энергичное видео" type="green"/>
                            <Tag value="Изи монтаж" type="yellow"/>
                            <Tag value="Трендовый звук" type="red"/>
                            <Tag value="Лид магнит" type="yellow"/>
                            <Tag value="Красота и здоровье"/>
                        </div>
                    </div>
                    <div class="hooks">
                        <div class="hooks__header">
                            <p class="hooks__title">Транскрибация</p>
                            <div class="hooks__button-group">
                                <button class="translate">
                                    <img :src="lang" alt="lang" />
                                    Переведено
                                </button>
                                <button class="copy icon">
                                    <img :src="copy" alt="copy" />
                                </button>
                            </div>
                        </div>
                        <div class="hooks__content">
                            <div class="hooks__text">
                                <p>
                                    SPF скатывается? Смотри — вот эти катышки. И
                                    нет, это не всегда “плохой SPF”.
                                </p>
                                <br />
                                <p>Скатывается по трём причинам.</p>
                                <br />
                                <p>
                                    Первая — ты намазал под SPF слишком много
                                    всего: сыворотка, крем, база… сверху SPF — и
                                    оно начинает конфликтовать. Чем больше
                                    слоёв, тем выше шанс, что всё свернётся в
                                    катышки.
                                </p>
                            </div>
                            <button class="more">
                                <img :src="arrow" alt="arrow" /> Ещё
                            </button>
                        </div>
                    </div>
                    <button class="button button_primary button_adapt">
                        <img :src="adapt" alt="adapt" /> Адаптировать
                    </button>
                </div>
            </aside>
        </div>
    </Transition>
</template>

<style scoped lang="css">
.button_adapt {
    display: flex;
    align-items: center;
    gap: 12px;
    border-radius: 12px;
    padding: 16px 28px 16px 16px;
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;
    letter-spacing: 0.25px;
}

.more {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    line-height: 16px;
    letter-spacing: 0.4px;
    font-weight: 600;
    padding: 8px;
}

.hooks__content {
    margin-top: 8px;
    border-radius: 6px;
    background-color: #f4f5f6;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 12px;
}

.hooks__content p {
    color: #4e616b;
    font-size: 14px;
    line-height: 21px;
    letter-spacing: 0.25px;
}

.hooks {
    margin-top: 24px;
    margin-bottom: 32px;
}

.hooks__title {
    font-size: 16px;
    line-height: 24px;
    font-weight: 600;
    letter-spacing: 0.15px;
}

.hooks__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.hooks__button-group {
    display: flex;
    gap: 10px;
}

.copy {
    width: 32px;
    height: 32px;
}

.translate {
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 600;
    font-size: 12px;
    line-height: 16px;
    color: #2b31b3;
    padding: 8px 12px 8px 8px;
    border-radius: 12px;
}

.text-toggle {
    background: none;
    border: none;
    padding: 0;
    font-size: inherit;
    font-weight: 600;
    color: #343a40;
    cursor: pointer;
}

.info {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.info__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.music-lang {
    display: flex;
    align-items: center;
    gap: 16px;
}

.music {
    border-radius: 24px;
    background-color: #f1f3f5;
    padding: 4px 12px 4px 8px;
    display: flex;
    align-items: center;
    width: fit-content;
    gap: 10px;
    font-size: 12px;
    line-height: 16px;
    letter-spacing: 0.4px;
    font-weight: 500;
    color: #343a40;
}

.lang {
    display: flex;
    align-items: center;
}

.lang__name {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: 12px;
}

.lang__name,
.lang__title {
    font-size: 14px;
    line-height: 21px;
    letter-spacing: 0.25px;
    color: #4e616b;
}

.title {
    flex: 2;
}

.info__header-title {
    display: flex;
    gap: 10px;
}

.title__name {
    font-size: 14px;
    font-weight: 500;
    color: #4e616b;
    letter-spacing: 0.25px;
    line-height: 21px;
    margin-bottom: 8px;
}

.title__text {
    font-weight: 600;
    font-size: 24px;
    line-height: 29px;
    margin-bottom: 16px;
}

.wrapper {
    width: 100%;
    height: 100svh;
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
    display: flex;
    justify-content: flex-end;
}

.modal {
    background-color: white;
    border-top-left-radius: 24px;
    border-bottom-left-radius: 24px;
    padding: 24px;
    display: flex;
    gap: 32px;
}

.videocard_modal {
    width: 216px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.videocard_modal__top {
    margin: 0;
}

.videocard_modal__video {
    height: 340.16px;
    object-fit: cover;
}

.videocard__video-play {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.share {
    display: flex;
    height: fit-content;
}

.videocard_modal__bottom {
    gap: 8px;
    padding: 0;
}

.videocard_modal__bottom-text {
    color: #343a40;
    transition: height 300ms ease-in-out;
    height: fit-content;
    overflow: unset;
}

.video-info {
    width: 624px;
}

.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}
.modal-enter-active .modal,
.modal-leave-active .modal {
    transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
.modal-enter-from .modal,
.modal-leave-to .modal {
    transform: translateX(100%);
}
</style>
