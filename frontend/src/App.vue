<script setup lang="ts">
import VideoCard from "./shared/ui/VideoCard.vue";
import { onMounted, onUnmounted, ref } from "vue";
import { getPosts, type PostData } from "./features/api/posts";
import Modal from "./shared/ui/Modal.vue";

const USER_ID = "5c25e132-5066-4686-9a72-2e37e2e2250b"; // TODO: поменять на сущетсвующий id пользователя
const SCROLL_THRESHOLD = 500;

const posts = ref<PostData[]>([]);
const isLoading = ref(false);

const fetchPosts = async () => {
    if (isLoading.value) return;

    isLoading.value = true;
    try {
        const data = await getPosts(USER_ID);
        if (!data) throw new Error("Ошибка при запросе");

        const existingIds = new Set(posts.value.map((p) => p.id));
        const newPosts = data.filter((p) => !existingIds.has(p.id));

        if (newPosts.length > 0) {
            posts.value.push(...newPosts);
        }
    } catch (e) {
        console.error(e);
    } finally {
        isLoading.value = false;
    }
};

const handleScroll = () => {
    const scrolledTo = window.scrollY + window.innerHeight;
    const threshold = document.documentElement.scrollHeight - SCROLL_THRESHOLD;

    if (scrolledTo >= threshold) {
        fetchPosts();
    }
};

onMounted(() => {
    fetchPosts();
    window.addEventListener("scroll", handleScroll, { passive: true });
});

onUnmounted(() => {
    window.removeEventListener("scroll", handleScroll);
});

const isModalOpen = ref(false);
const selectedPostId = ref<number | null>(null);

function openModal(id: number) {
    selectedPostId.value = id;
    isModalOpen.value = true;
}
</script>

<template>
    <Modal v-model="isModalOpen" :post-id="selectedPostId" :user-id="USER_ID" />

    <div class="list">
        <VideoCard
            v-for="post in posts"
            :key="post.id"
            :id="post.id"
            :text="post.text"
            :date="post.created_at"
            :user_id="post.user_id"
            @open-modal="openModal"
        />
    </div>

    <div v-if="isLoading" class="loader">Загрузка...</div>
</template>

<style scoped>
.list {
    display: flex;
    width: 1040px;
    margin: 0 auto;
    margin-top: 8px;
    flex-wrap: wrap;
    gap: 8px;
}

.loader {
    text-align: center;
    padding: 24px;
    color: #888;
}
</style>
