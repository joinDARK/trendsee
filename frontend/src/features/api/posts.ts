import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:8000" });

export interface PostData {
    id: number
    text: string
    title: string
    created_at: string
    user_id: string
    updated_at: string
}

export const getPosts = async (userId: string) => {
    try {
        const res = await api.get<PostData[]>(`/u/${userId}/p/`);
        return res.data;
    } catch (e) {
        console.log(e);
    }
};

export const getPost = async (userId: string, postId: number) => {
    try {
        const res = await api.get<PostData>(`/u/${userId}/p/${postId}`);
        return res.data;
    } catch (e) {
        console.log(e);
    }
}