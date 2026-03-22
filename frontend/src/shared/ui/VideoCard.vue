<script setup lang="ts">
import sub from "../../assets/sub.svg";
import view from "../../assets/view.svg";
import like from "../../assets/like.svg";
import comment from "../../assets/comment.svg";
import reply from "../../assets/reply.svg";
import reels from "../../assets/reels.svg";
import fire from "../../assets/fire.svg";
import repost from "../../assets/repost.svg";

import { computed } from 'vue';
import { formatierStringDate, formatierText, formatierUserId } from '../../features/utils/formatiers';

interface Props {
    id: number
    user_id: string;
    text: string
    date: string
};
const props = defineProps<Props>();

const emit = defineEmits<{ openModal: [id: number] }>();

// Форматируем дату
const formattedDate = computed(() => {
  return formatierStringDate(props.date);
});

// Форматируем текст
const truncatedText = computed(() => {
  return formatierText(props.text)
});

// Форматируем id пользователя
const truncatedUserId = computed(() => {
  return formatierUserId(props.user_id)
});
</script>

<template>
    <div class="videocard">
        <div class="videocard__top">
            <div class="videocard__video-header">
                <div class="video-header__left">
                    <div class="video-header__badage blur">
                        <img
                            class="video-header__badage-img"
                            :src="reels"
                            alt=""
                        />
                        <p class="video-header__badage-value">Reels</p>
                    </div>
                    <div class="video-header__badage blur">
                        <img
                            class="video-header__badage-img"
                            :src="fire"
                            alt=""
                        />
                        <p class="video-header__badage-value">X10</p>
                    </div>
                </div>
                <div class="video-header__right">
                    <button class="button icon blur">
                        <img :src="like" alt="favorite" />
                    </button>
                    <button class="button icon blur">
                        <img :src="reply" alt="reply" />
                    </button>
                </div>
            </div>
            <img class="videocard__video" src="/video.png">
            <div class="videocard__video-footer">
                <div class="videocard__video-stats blur">
                    <div class="videocard__video-stat">
                        <img :src="view" alt="view" class="video-stat__icon" />
                        <p class="video-stat__value">105k</p>
                    </div>
                    <div class="videocard__video-stat">
                        <img :src="like" alt="like" class="video-stat__icon" />
                        <p class="video-stat__value">85k</p>
                    </div>
                    <div class="videocard__video-stat">
                        <img
                            :src="comment"
                            alt="comment"
                            class="video-stat__icon"
                        />
                        <p class="video-stat__value">15k</p>
                    </div>
                    <div class="videocard__video-stat">
                        <img
                            :src="repost"
                            alt="repost"
                            class="video-stat__icon"
                        />
                        <p class="video-stat__value">485</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="videocard__bottom">
            <div class="videocard__bottom-header">
                <div class="videocard__user">
                    <img src="/avatar.png" alt="" class="videocard__user-img" />
                    <div class="videocard__user-info">
                        <a :href="`/u/${props.user_id}`" class="videocard__user-name">@{{ truncatedUserId }}</a>
                        <p class="videocard__user-subscribes">384.5K</p>
                    </div>
                </div>
                <button class="videocard__subscribe">
                    <img :src="sub" alt="sub" />
                </button>
            </div>
            <div class="videocard__bottom-text">
                {{ truncatedText }}
            </div>
            <p class="videocard__date">{{ formattedDate }}</p>
            <button class="videocard__analysis button_primary" @click="emit('openModal', props.id)">Анализ</button>
        </div>
    </div>
</template>

<style scoped>
.video-header__right {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.video-stat__value {
    font-size: 12px;
    font-weight: 500;
    line-height: 15px;
}

.videocard__video-header {
    display: flex;
    justify-content: space-between;
}

.videocard__video-footer {
    position: absolute;
    padding: 12px;
    bottom: 0;
}

.videocard__video-stats {
    display: flex;
    padding: 8px 4px;
    width: fit-content;
    border-radius: 12px;
}

.videocard__video-stat {
    display: flex;
    width: 55.5px;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    color: white;
}

.videocard__analysis {
    padding: 12px 0;
    width: 100%;
    border-radius: 12px;
    line-height: 16px;
    font-weight: 600;
    font-size: 12px;
}
</style>
